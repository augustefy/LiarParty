import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game
from channels.db import database_sync_to_async

class LobbyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.game_code = self.scope["url_route"]["kwargs"]["code"]
        self.group_name = f"lobby_{self.game_code}"

        # Rejoindre le groupe
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def player_update(self, event):   # ici il manquait event !!
        game = await database_sync_to_async(Game.objects.get)(code=self.game_code)
        players = await database_sync_to_async(lambda: list(game.players.all()))()
        players_list = [
            p.pseudo + (" (Hôte)" if p.id == game.host_id else "")
            for p in players
        ]

        await self.send(text_data=json.dumps({
            "action": "player_update",
            "players": players_list,
        }))

    async def game_started(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_started',
        }))
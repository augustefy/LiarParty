import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Game, Player, Round

class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.code = self.scope['url_route']['kwargs']['code']
        self.group_name = f"lobby_{self.code}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Pas besoin ici pour l'instant
        pass

    async def player_update(self, event):
        game = await sync_to_async(Game.objects.get)(code=self.code)
        players = await sync_to_async(list)(game.players.values_list('pseudo', flat=True))

        await self.send(text_data=json.dumps({
            'action': 'player_update',
            'players': list(players)
        }))

    async def game_started(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_started'
        }))

    async def statement_submitted(self, event):
        await self.send(text_data=json.dumps({
            'action': 'statement_submitted',
            'round_id': event['round_id']
        }))
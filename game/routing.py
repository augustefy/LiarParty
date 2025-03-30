from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/lobby/(?P<code>\w{5})/$', consumers.LobbyConsumer.as_asgi()),
    re_path(r'ws/round/(?P<round_id>\d+)/$', consumers.RoundConsumer.as_asgi()),
]
from django.urls import path

from matchmaking import views
from matchmaking.consumers import MatchmakingConsumer

urlpatterns = [
    path('', views.matchmaking, name='matchmaking')
]
websocket_matchmaking_urls = [
    path('ws/matchmaking/', MatchmakingConsumer.as_asgi())
]

from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from api import views
from api.consumers import SessionConsumer

router = DefaultRouter()
router.register('history', views.HistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
    path('game/', views.PendingSessionRetrieveView.as_view(), name='session-pending'),
]

websocket_urlpatterns = [
    re_path("ws/games/(?P<game_id>[^/]+)/$", SessionConsumer.as_asgi()),
]

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from api.urls import websocket_urlpatterns
from matchmaking.urls import websocket_matchmaking_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chess.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            JWTAuthMiddlewareStack((
                URLRouter(
                    websocket_urlpatterns +
                    websocket_matchmaking_urls
                )
            ))
        )
    }
)

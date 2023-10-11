import os

import django

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

import websockets.routing
import features.routing

application = ProtocolTypeRouter(
    {
    "http":
    get_asgi_application(),
    "websocket":
    AllowedHostsOriginValidator(
    AuthMiddlewareStack(URLRouter(websockets.routing.websocket_urlpatterns + features.routing.websocket_urlpatterns))
    ),},)

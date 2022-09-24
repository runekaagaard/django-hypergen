import os

import django

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

import websockets.routing

application = ProtocolTypeRouter({
    "http":
    AsgiHandler(),
    "websocket":
    AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websockets.routing.websocket_urlpatterns))),})

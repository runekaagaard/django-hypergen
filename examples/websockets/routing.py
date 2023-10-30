from hypergen.imports import NO_PERM_REQUIRED
from django.urls import path
from websockets import consumers

websocket_urlpatterns = [path(r'ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi(perm=NO_PERM_REQUIRED))]

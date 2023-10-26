from hypergen.imports import NO_PERM_REQUIRED
from django.urls import path
from features import consumers

websocket_urlpatterns = [path(r'ws/features/snake-consumer/', consumers.SnakeConsumer.as_asgi(perm=NO_PERM_REQUIRED))]

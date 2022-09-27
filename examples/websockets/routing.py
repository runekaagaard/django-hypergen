from hypergen.hypergen import autoconsumers
from django.urls import path

from . import consumers
from . import views

websocket_urlpatterns = [path(r'ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi())]

websocket_urlpatterns += autoconsumers(views, prefix="ws/websocketsx/")

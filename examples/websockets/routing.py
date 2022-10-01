from hypergen.hypergen import autoconsumers
from django.urls import path

from . import consumers
from . import views

# Manually set routes for consumers.
websocket_urlpatterns = [path(r'ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi())]

# Automatically create routes for functions decorated with @consumer.
websocket_urlpatterns += autoconsumers(views, prefix="ws/websockets/")

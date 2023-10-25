from hypergen.hypergen import autoconsumers
from hypergen.imports import NO_PERM_REQUIRED
from django.urls import path

from . import consumers
from . import views

# Manually set routes for consumers.
websocket_urlpatterns = [path(r'ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi(perm=NO_PERM_REQUIRED))]

# Automatically create routes for functions decorated with @consumer.
websocket_urlpatterns += autoconsumers(views, prefix="ws/websockets/")

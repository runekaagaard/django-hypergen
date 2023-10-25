from hypergen.hypergen import autoconsumers
from django.urls import path

from anteams import consumers

# Manually set routes for consumers.
websocket_urlpatterns = [path(r'ws/anteams', consumers.AnteamsConsumer.as_asgi())]

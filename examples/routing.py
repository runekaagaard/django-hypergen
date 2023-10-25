import websockets.routing
import features.routing
import anteams.routing

websocket_urlpatterns = (websockets.routing.websocket_urlpatterns + features.routing.websocket_urlpatterns +
    anteams.routing.websocket_urlpatterns)

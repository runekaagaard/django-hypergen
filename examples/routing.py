import websockets.routing
import features.routing

websocket_urlpatterns = websockets.routing.websocket_urlpatterns + features.routing.websocket_urlpatterns

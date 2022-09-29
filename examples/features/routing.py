from hypergen.hypergen import autoconsumers

from . import views

websocket_urlpatterns = autoconsumers(views, prefix="ws/features/")

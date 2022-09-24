from hypergen.hypergen import autourls
from websockets import views

app_name = 'websockets'
urlpatterns = autourls(views, app_name)

from hypergen.hypergen import autourls
from notifications import views

app_name = 'notifications'
urlpatterns = autourls(views, app_name)

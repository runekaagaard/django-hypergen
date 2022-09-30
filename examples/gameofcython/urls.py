from hypergen.hypergen import autourls
from gameofcython import views

app_name = 'gameofcython'
urlpatterns = autourls(views, app_name)

from hypergen.hypergen import autourls
from todomvc import views

app_name = 'todomvc'
urlpatterns = autourls(views)

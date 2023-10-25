from hypergen.hypergen import autourls
from anteams import views

app_name = 'anteams'
urlpatterns = autourls(views, app_name)

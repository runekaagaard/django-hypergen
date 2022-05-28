from hypergen.hypergen import autourls
from commands import views, actions

app_name = 'commands'

urlpatterns = autourls(views, app_name)
urlpatterns += autourls(actions, app_name)

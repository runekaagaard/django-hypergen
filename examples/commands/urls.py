from hypergen.hypergen import autourls
from commands import views, callbacks

app_name = 'commands'

urlpatterns = autourls(views, app_name)
urlpatterns += autourls(callbacks, app_name)

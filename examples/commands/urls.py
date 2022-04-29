from hypergen.contrib import hypergen_urls
from commands import views, callbacks

app_name = 'commands'

urlpatterns = hypergen_urls(views, app_name)
urlpatterns += hypergen_urls(callbacks, app_name)

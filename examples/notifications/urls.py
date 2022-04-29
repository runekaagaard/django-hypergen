from hypergen.contrib import hypergen_urls
from notifications import views

app_name = 'notifications'
urlpatterns = hypergen_urls(views, app_name)

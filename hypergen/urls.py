from hypergen.contrib import hypergen_urls
from hypergen import views

app_name = 'hypergen'
urlpatterns = hypergen_urls(views, app_name)

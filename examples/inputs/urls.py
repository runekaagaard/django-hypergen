from hypergen.contrib import hypergen_urls
from inputs import views

app_name = 'inputs'
urlpatterns = hypergen_urls(views, app_name)

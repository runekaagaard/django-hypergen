from hypergen.contrib import hypergen_urls
from hellohypergen import views

app_name = 'hellohypergen'
urlpatterns = hypergen_urls(views)

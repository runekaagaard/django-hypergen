from hypergen.contrib import hypergen_urls
from gameofcython import views

app_name = 'gameofcython'
urlpatterns = hypergen_urls(views)

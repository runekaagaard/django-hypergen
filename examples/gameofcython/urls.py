from hypergen.contrib import hypergen_urls
from . import views  # py2 compat

app_name = 'gameofcython'
urlpatterns = hypergen_urls(views)

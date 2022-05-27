from hypergen.contrib import hypergen_urls
from coredocs import views

app_name = 'coredocs'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or
# @hypergen_callback.
urlpatterns = hypergen_urls(views, namespace="coredocs")
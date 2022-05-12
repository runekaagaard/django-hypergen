from hypergen.contrib import hypergen_urls
from apptemplate import views

app_name = 'apptemplate'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or
# @hypergen_callback.
urlpatterns = hypergen_urls(views, namespace="apptemplate")

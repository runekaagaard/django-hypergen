from hypergen.contrib import hypergen_urls
from hellomagic import views

app_name = 'hellomagic'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or @action.
# If that's not your thing, normal urlpatterns works as well.
urlpatterns = hypergen_urls(views, namespace="hellomagic")

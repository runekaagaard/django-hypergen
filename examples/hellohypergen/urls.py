from hypergen.hypergen import autourls
from hellohypergen import views

app_name = 'hellohypergen'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or @hypergen_callback.
# If that's not your thing, normal urlpatterns works as well.
urlpatterns = autourls(views, namespace="hellohypergen")

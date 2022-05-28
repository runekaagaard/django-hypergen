from hypergen.hypergen import autourls
from partialload import views

app_name = 'partialload'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or @hypergen_callback.
# If that's not your thing, normal urlpatterns works as well.
urlpatterns = autourls(views, namespace="partialload")

from hypergen.hypergen import autourls
from coredocs import views

app_name = 'coredocs'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or
# @hypergen_callback.
urlpatterns = autourls(views, namespace="coredocs")

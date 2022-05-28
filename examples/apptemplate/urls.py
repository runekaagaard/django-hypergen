from hypergen.hypergen import autourls
from apptemplate import views

app_name = 'apptemplate'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or
# @hypergen_callback.
urlpatterns = autourls(views, namespace="apptemplate")

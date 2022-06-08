from hypergen.hypergen import autourls
from apptemplate import views

app_name = 'apptemplate'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or
# @action.
urlpatterns = autourls(views, namespace="apptemplate")

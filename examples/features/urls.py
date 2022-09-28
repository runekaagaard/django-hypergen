from hypergen.hypergen import autourls
from features import views

app_name = 'features'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or
# @action.
urlpatterns = autourls(views, namespace=app_name)

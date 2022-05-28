from hypergen.hypergen import autourls
from globalcontext import views

app_name = 'globalcontext'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or @action.
# If that's not your thing, normal urlpatterns works as well.
urlpatterns = autourls(views, namespace="globalcontext")

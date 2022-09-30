from hypergen.hypergen import autourls
from motherofall import views

app_name = 'motherofall'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or @action.
# If that's not your thing, normal urlpatterns works as well.
urlpatterns = autourls(views, app_name)

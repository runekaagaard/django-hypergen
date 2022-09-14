from hypergen.hypergen import autourls
from booking import views

app_name = 'booking'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or
# @action.
urlpatterns = autourls(views, namespace="booking")

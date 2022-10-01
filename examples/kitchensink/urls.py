from hypergen.hypergen import autourls
from kitchensink import views

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

app_name = 'kitchensink'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or
# @hypergen_callback.
urlpatterns = autourls(views, app_name)

urlpatterns += [
    url("my_view", views.my_view, name="my_view"),
    url("v2", views.v2, name="v2"),
    url("c2", views.c2, name="c2"),]

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from devpluginstest import views

app_name = '                  '

urlpatterns = [
    url("^v1/$", views.v1, name="v1"),
    url("^v2/$", views.v2, name="v2"),]

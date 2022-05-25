from hypergen.hypergen import autourls

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from devpluginstest import views

app_name = 'devpluginstest'

urlpatterns = [
    url("^v1/$", views.v1, name="v1"),
    url("^v2/$", views.v2, name="v2"),
    url("^v3/$", views.v3, name="v3"),
    url("^c3/$", views.c3, name="c3"),
    url("^c4/$", views.c4, name="c4"),
    url("^c5/$", views.c5, name="c5"),
    url("^v4/$", views.v4, name="v4"),
    url("^c6/$", views.c6, name="c6"),
    url("^v5/$", views.v5, name="v5"),
    url("^c7/$", views.c7, name="c7"),
    url("^v6/$", views.v6, name="v6"),
    url("^c8/$", views.c8, name="c8"),
    url("^v7/$", views.v7, name="v7"),]

urlpatterns.extend(autourls(views, app_name))

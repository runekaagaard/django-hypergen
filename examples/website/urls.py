try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from website import views

app_name = 'website'

urlpatterns = [
    url("^$", views.home, name="home"),
    url("^documentation/$", views.documentation, name="documentation"),]

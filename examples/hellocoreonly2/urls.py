try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from hellocoreonly2 import views

app_name = 'hellocoreonly2'

urlpatterns = [
    url("^counter/$", views.counter, name="counter"),
    url("^increment/$", views.increment, name="increment"),]

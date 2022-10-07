from djangotemplates import views
from hypergen.hypergen import autourls
try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

app_name = 'djangotemplates'

urlpatterns = [
    url('^$', views.djangotemplates, name="djangotemplates"),] + autourls(views, app_name)

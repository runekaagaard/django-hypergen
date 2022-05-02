from djangotemplates import views
try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

app_name = 'djangotemplates'

urlpatterns = [
    url('^$', views.djangotemplates, name="djangotemplates"),
    url('^add/$', views.add, name="add"),
    url('^reset/$', views.reset, name="reset"),
    url('^subtract/$', views.subtract, name="subtract"),
    url('^divide/$', views.divide, name="divide"),
    url('^multiply/$', views.multiply, name="multiply"),
    url('^push/$', views.push, name="push"),]

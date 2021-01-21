from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^callback/([a-z.0-9_]+)/$', views.callback, name='callback'),
]

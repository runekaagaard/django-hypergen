from djangotemplates import views
from django.urls import path

app_name = 'djangotemplates'

urlpatterns = [
    path('', views.djangotemplates, name="djangotemplates"),
    path('plus/', views.plus, name="plus"),
    path('minus/', views.minus, name="minus"),
    path('divide/', views.divide, name="divide"),
    path('multiply/', views.multiply, name="multiply"),
    path('push/', views.push, name="push"),]

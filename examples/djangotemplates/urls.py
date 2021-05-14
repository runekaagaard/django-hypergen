from djangotemplates import views
from django.urls import path

app_name = 'djangotemplates'

urlpatterns = [
    path('', views.djangotemplates, name="djangotemplates"),
    path('add/', views.add, name="add"),
    path('reset/', views.reset, name="reset"),
    path('subtract/', views.subtract, name="subtract"),
    path('divide/', views.divide, name="divide"),
    path('multiply/', views.multiply, name="multiply"),
    path('push/', views.push, name="push"),]

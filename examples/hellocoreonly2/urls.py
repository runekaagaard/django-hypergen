from django.urls import path

from hellocoreonly2 import views

app_name = 'hellocoreonly2'

urlpatterns = [
    path("counter", views.counter, name="counter"),
    path("increment", views.increment, name="increment"),]

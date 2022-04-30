from django.urls import path, include

from hellocoreonly import views

app_name = 'hellocoreonly'

urlpatterns = [
    path("counter", views.counter, name="counter"),
    path("increment", views.increment, name="increment"),]

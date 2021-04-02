from freedom.contrib import hypergen_urls
from todomvc import views

app_name = 'todomvc'
urlpatterns = hypergen_urls(views)

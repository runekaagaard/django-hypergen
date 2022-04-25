from hypergen.contrib import hypergen_urls
from t9n import views

app_name = 't9n'
urlpatterns = hypergen_urls(views, app_name)

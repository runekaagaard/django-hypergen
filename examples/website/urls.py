from hypergen.contrib import hypergen_urls
from website import views

app_name = 'website'

urlpatterns = hypergen_urls(views, namespace="website")

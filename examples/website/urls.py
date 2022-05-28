from hypergen.hypergen import autourls
from website import views

app_name = 'website'

urlpatterns = autourls(views, namespace="website")

from hypergen.hypergen import autourls
from inputs import views

app_name = 'inputs'
urlpatterns = autourls(views, app_name)

from hypergen.hypergen import autourls
from website import views
from website.minidemoes import shoot_em_up

app_name = 'website'

urlpatterns = autourls(views, namespace="website") + autourls(shoot_em_up, namespace="website")

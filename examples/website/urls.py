from hypergen.hypergen import autourls
from website import views
from website.minidemoes import shoot_em_up, shoot_em_up_alt

app_name = 'website'

urlpatterns = autourls(views, namespace="website") + autourls(shoot_em_up, namespace="website") + autourls(
    shoot_em_up_alt, namespace="website")

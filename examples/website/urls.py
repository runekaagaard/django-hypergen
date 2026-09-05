from hypergen.hypergen import autourls
from website import views
from website.minidemoes import shoot_em_up, shoot_em_up_alt, memory_match

app_name = 'website'

urlpatterns = autourls(views, namespace="website") + autourls(shoot_em_up, namespace="website") + autourls(
    shoot_em_up_alt, namespace="website") + autourls(memory_match, namespace="website")

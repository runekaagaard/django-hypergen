from django.contrib import messages
from hypergen.plugins.alertify import AlertifyPlugin

from hypergen.imports import *

d = dict

from features import templates

@action(perm=NO_PERM_REQUIRED, target_id="features")
def feature(request, n):
    l = len(templates.FEATURES) - 1
    if n < 0:
        n = l
    elif n > l:
        n = 0

    templates.feature(n)

@action(perm=NO_PERM_REQUIRED, target_id="f3")
def reverser(request, text):
    templates.f3_template(text)

# plugins
@action(perm=NO_PERM_REQUIRED, user_plugins=[AlertifyPlugin()])
def alert(request):
    messages.warning(request, "Uh-oh!")

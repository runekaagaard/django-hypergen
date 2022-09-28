from hypergen.imports import *
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

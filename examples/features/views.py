from hypergen.imports import *
from features import templates

@action(perm=NO_PERM_REQUIRED, target_id="features")
def feature(request, n):
    try:
        templates.feature(n)
    except IndexError:
        n = len(templates.FEATURES) - 1 if n < 0 else 0
        templates.feature(n)

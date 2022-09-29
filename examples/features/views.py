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

@consumer(perm=NO_PERM_REQUIRED, target_id="snake-game")
def snake(consumer, request):
    from random import randint
    state = [[randint(0, 1) for _ in range(0, 20)] for _ in range(0, 20)]
    # state[10][9] = 1
    # state[10][10] = 1
    templates.snake(state)

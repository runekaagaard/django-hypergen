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
def snake(consumer, request, key):
    def limit(n):
        if n > 19:
            return 0
        elif n < 0:
            return 19
        else:
            return n

    if not hasattr(consumer, "state"):
        consumer.state = {(10, 10)}
        consumer.direction = (0, 1)
    else:
        # print("GOT STATE!")
        ...

    if key is not None:
        print(repr(key))

    if key is None:
        state2 = set()
        for x, y in consumer.state:
            state2.add((limit(x + consumer.direction[0]), limit(y + consumer.direction[1])))
        consumer.state = state2
    elif key == "a":
        print("LEFT")
        consumer.direction = (-1, 0)
    elif key == "d":
        consumer.direction = (1, 0)
        print("RIGHT")
    elif key == "w":
        consumer.direction = (0, -1)
        print("UP")
    elif key == "s":
        consumer.direction = (0, 1)
        print("DOWN")

    templates.snake(consumer.state)

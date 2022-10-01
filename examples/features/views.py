from collections import deque
from random import randint

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

# Snake
DIRECTIONS = d(a=(-1, 0), d=(1, 0), w=(0, -1), s=(0, 1))
INIT_STATE = [(10, 10), (10, 11)]

@consumer(perm=NO_PERM_REQUIRED, target_id="snake-game")
def snake(consumer, request, key):
    def limit(pair):
        def _(n):
            if n > 19:
                return 0
            elif n < 0:
                return 19
            else:
                return n

        return _(pair[0]), _(pair[1])

    def init_state():
        consumer.direction = DIRECTIONS["s"]
        consumer.state = deque(INIT_STATE)
        consumer.fruit = set()
        place_fruit()

    def place_fruit():
        x, y = randint(0, 19), randint(0, 19)
        while (x, y) in consumer.state:
            x, y = randint(0, 19), randint(0, 19)
        consumer.fruit.add((x, y))

    def mv(pair, d):
        return (pair[0] + d[0], pair[1] + d[1])

    if not hasattr(consumer, "state"):
        init_state()

    if key:
        consumer.direction = DIRECTIONS.get(key, consumer.direction)
        return

    head1 = consumer.state[-1]
    if head1 in consumer.fruit:
        consumer.fruit.remove(head1)
        place_fruit()
    else:
        consumer.state.popleft()

    head2 = mv(head1, consumer.direction)
    if head2 in consumer.state:
        init_state()
    else:
        consumer.state.append(limit(head2))

    templates.snake(consumer)

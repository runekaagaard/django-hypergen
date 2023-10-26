d = dict
from hypergen.imports import *

from collections import deque
from random import randint

from features import templates

class SnakeConsumer(HypergenWebsocketConsumer):
    # Receives pressed key if any.
    def receive_callback(self, key):
        # Run the snake game logic
        commands = hypergen(snake_game, self, key, settings=dict(action=True, returns=COMMANDS,
            target_id="snake-game"))

        # Send commands to frontend.
        self.channel_send_hypergen_commands(commands)

# Snake game logic

DIRECTIONS = d(a=(-1, 0), d=(1, 0), w=(0, -1), s=(0, 1))
INIT_STATE = [(10, 10), (10, 11)]

def snake_game(consumer, key):
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
    head2 = mv(head1, consumer.direction)
    if head2 in consumer.state:
        init_state()
    else:
        consumer.state.append(limit(head2))

        # fruit
        if head1 in consumer.fruit:
            consumer.fruit.remove(head1)
            place_fruit()
        else:
            # dont grow
            consumer.state.popleft()

    templates.snake(consumer)

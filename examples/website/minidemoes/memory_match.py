from hypergen.imports import *

from random import shuffle
from time import time

from django.urls.base import reverse
from django.views.decorators.cache import never_cache

from website.templates2 import base_example_template

EMOJIS = ("🦆", "🐍", "🐸", "🦉", "🐢", "🦊", "🐙", "🦋")

def new_deck():
    deck = list(EMOJIS) * 2
    shuffle(deck)
    return deck

@never_cache
@liveview(perm=NO_PERM_REQUIRED)
def memory_match(request):
    with base_example_template(__file__):
        style("""
            #memory-match .memory-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }
            #memory-match .memory-card {
                width: 108px;
                height: 108px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 48px;
                background-color: #74b9e7;
                border-radius: 8px;
                cursor: pointer;
                user-select: none;
            }
            #memory-match .memory-card.revealed {
                background-color: #fff3b0;
            }
            #memory-match .memory-card.matched {
                background-color: #c8f7c5;
                cursor: default;
            }
        """)

        template(new_deck(), [], [], 0, time(), None)

@action(perm=NO_PERM_REQUIRED, target_id="memory-match")
def flip(request, deck, revealed, matched, moves, start_time, end_time, index):
    if end_time is None and index not in revealed and index not in matched:
        if len(revealed) == 2:
            # Mismatched cards stay revealed until the next pick.
            revealed = []

        revealed.append(index)

        if len(revealed) == 2:
            moves += 1
            first, second = revealed
            if deck[first] == deck[second]:
                matched = matched + revealed
                revealed = []

        if len(matched) == len(deck):
            end_time = time()

    template(deck, revealed, matched, moves, start_time, end_time)

def template(deck, revealed, matched, moves, start_time, end_time):
    with div(id="memory-match"):
        h2("Memory Match")
        p('Flip the cards and find all the pairs. ', "A mismatched pair stays revealed until your next pick.",
            sep=" ")

        with div(class_="memory-grid"):
            for i, emoji in enumerate(deck):
                if i in matched:
                    div(emoji, id_="card-{}".format(i), class_="memory-card matched")
                elif i in revealed:
                    div(emoji, id_="card-{}".format(i), class_="memory-card revealed",
                        onmousedown=callback(flip, deck, revealed, matched, moves, start_time, end_time, i))
                else:
                    div("?", id_="card-{}".format(i), class_="memory-card",
                        onmousedown=callback(flip, deck, revealed, matched, moves, start_time, end_time, i))

        seconds = round((end_time if end_time is not None else time()) - start_time, 1)
        div(b("moves: "), moves)
        div(b("time: "), seconds, " s")
        div(b("pairs: "), "{}/{}".format(len(matched) // 2, len(EMOJIS)))

        if end_time is not None:
            div(b("🎉 You win!"), sep=" ")
            a("Play again", href=reverse("website:memory_match"))

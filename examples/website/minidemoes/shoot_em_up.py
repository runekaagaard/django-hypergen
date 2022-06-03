from hypergen.imports import *

from random import choice
from time import time

from django.templatetags.static import static
from django.views.decorators.cache import never_cache

from website.templates2 import base_example_template

@never_cache
@liveview(perm=NO_PERM_REQUIRED)
def shoot_em_up(request):
    with base_example_template(__file__):
        script("""
            function play(url) {
                new Audio(url).play()
            }
        """)

        template(start_time=time())

@action(perm=NO_PERM_REQUIRED, target_id="shoot-em-up")
def fire(request, start_time, hits, target_num):
    template(start_time, hits=hits + 1, target_num=target_num)
    command("play", static("website/gun.mp3"))

def template(start_time=None, hits=0, target_num=-1):
    target_num = choice(list(set(range(0, 5)) - {target_num}))

    with div(id="shoot-em-up"):
        for i in range(0, 5):
            if i == target_num:
                img(
                    id="fire",
                    src=static("website/target.svg"),
                    onmousedown=callback(fire, start_time, hits, target_num),
                )
            else:
                img(src=static("website/duck.svg"))

        if hits:
            rate = round(hits / (time() - start_time), 2)
            div(b("hits: "), hits)
            div(b("rate: "), rate, "/s")
        else:
            div(b("warning:"), "🔊", sep=" ")

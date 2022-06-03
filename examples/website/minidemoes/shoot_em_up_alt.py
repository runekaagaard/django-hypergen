from hypergen.imports import *

from random import choice
from time import time

from django.templatetags.static import static
from django.views.decorators.cache import never_cache

from website.templates2 import doc_base_template

def init_appstate():
    return {"target_num": -1, "hits": 0, "start_time": time()}

settings = dict(
    perm=NO_PERM_REQUIRED,
    base_template=doc_base_template(__file__, "shoot-em-up"),
    appstate=init_appstate,
)

@never_cache
@liveview(**settings)
def shoot_em_up_alt(request):
    if request.method == "GET":
        script("""
            function play(url) {
                new Audio(url).play()
            }
        """)
        context.appstate = init_appstate()

    context.appstate["target_num"] = choice(list(set(range(0, 5)) - {context.appstate["target_num"]}))

    for i in range(0, 5):
        if i == context.appstate["target_num"]:
            img(id="fire_alt", src=static("website/target.svg"), onmousedown=callback(fire_alt))
        else:
            img(src=static("website/duck.svg"))

    if context.appstate["hits"]:
        rate = round(context.appstate["hits"] / (time() - context.appstate["start_time"]), 2)
        div(b("hits: "), context.appstate["hits"])
        div(b("rate: "), rate, "/s")
    else:
        div(b("warning:"), "🔊", sep=" ")

@action(base_view=shoot_em_up_alt, **settings)
def fire_alt(request):
    context.appstate["hits"] += 1
    command("play", static("website/gun.mp3"))

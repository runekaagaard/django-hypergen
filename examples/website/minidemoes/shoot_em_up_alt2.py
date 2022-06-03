from hypergen.imports import *
from hypergen.incubation import SessionStore

from random import choice
from time import time

from django.templatetags.static import static
from django.views.decorators.cache import never_cache

from website.templates2 import doc_base_template

settings = dict(perm=NO_PERM_REQUIRED, base_template=doc_base_template(__file__, "shoot-em-up"))

class State(SessionStore):
    def reset(self):
        self.target_num = -1
        self.hits = 0
        self.start_time = time()

state = State()

@never_cache
@liveview(**settings)
def shoot_em_up_alt(request):
    if request.method == "GET":
        script("""
            function play(url) {
                new Audio(url).play()
            }
        """)
        state.reset()

    state.target_num = choice(list(set(range(0, 5)) - {state.target_num}))

    for i in range(0, 5):
        if i == state.target_num:
            img(id="fire_alt", src=static("website/target.svg"), onmousedown=callback(fire_alt))
        else:
            img(src=static("website/duck.svg"))

    if state.hits:
        rate = round(state.hits / (time() - state.start_time), 2)
        div(b("hits: "), state.hits)
        div(b("rate: "), rate, "/s")
    else:
        div(b("warning:"), "🔊", sep=" ")

@action(base_view=shoot_em_up_alt, **settings)
def fire_alt(request):
    state.hits += 1
    command("play", static("website/gun.mp3"))

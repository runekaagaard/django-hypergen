from contextlib import contextmanager
import math
from django.templatetags.static import static
from hypergen.core import *
from hypergen.contrib import hypergen_view, NO_PERM_REQUIRED, hypergen_callback


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
            script("""
            window.addEventListener("mousemove", e => {
            hypergen.callback("/motherofall/mouse_move/", [e.clientX, e.clientY], {})
            })
            """)

        with body():
            h1("Mother of all demos")
            button("reset", id_="reset", onclick=callback(reset), focus=False)
            with div(id_="content"):
                yield



mouse_html = """
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 28 28" enable-background="new 0 0 28 28" xml:space="preserve">
<polygon fill="#FFFFFF" points="8.2,20.9 8.2,4.9 19.8,16.5 13,16.5 12.6,16.6 "/>
<polygon fill="#FFFFFF" points="17.3,21.6 13.7,23.1 9,12 12.7,10.5 "/>
<rect x="12.5" y="13.6" transform="matrix(0.9221 -0.3871 0.3871 0.9221 -5.7605 6.5909)" width="2" height="8"/>
<polygon points="9.2,7.3 9.2,18.5 12.2,15.6 12.6,15.5 17.4,15.5 "/>
</svg>
"""

state = {}

def get_own_state(request):
    key = request.session.session_key
    global state
    if key not in state:
        state[key] = {}
    return state[key]

def set_own_state(request, new_state):
    key = request.session.session_key
    global state
    state[key] = {**get_own_state(request), **new_state}


def mouse(item):
    with div(style={'position': 'fixed', 'width': '40px',
                    'left': f'{item.get("x", 0)}px', 'top': f'{item.get("y", 0)}px'}):
        raw(mouse_html)
        div(item.get("name", "No name"))

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_template)
def motherofall(request):
    global state
    localkey = request.session.session_key

    h2("There are currently ", len(state.keys()), " on this site")
    if 'name' not in get_own_state(request):
        with label("Whats your screen name?"):
              el = input_(id_="name")
              button("Submit & Start", id_="submit", onclick=callback(submit_name, el))
    else:
        script("""
        document.activeElement.blur();
        setTimeout(() => hypergen.callback('/motherofall/update/', [], {}), 20)""")
        for key in state:
            item = state[key]
            if key != localkey:
                mouse(item)



@hypergen_callback(perm=NO_PERM_REQUIRED, view=motherofall, target_id="content")
def update(request):
    pass

@hypergen_callback(perm=NO_PERM_REQUIRED, view=motherofall, target_id="content")
def submit_name(request, name):
    set_own_state(request, {'name': name, 'x': 0, 'y': 0})

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def reset(request):
    global state
    state = {}


@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def mouse_move(request, x, y):
    set_own_state(request, {'x': x, 'y': y})




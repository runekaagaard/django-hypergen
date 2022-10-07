from contextlib import contextmanager
import math
from django.templatetags.static import static

from djangolander.templates import lander_base_template
from hypergen.imports import *


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def _reset(request):
    request.session['state'] = dict(
        x=500,
        y=0,
        r=0,
        dx=0,
        dy=0,
        pressed=[]
    )

@action(perm=NO_PERM_REQUIRED, target_id=OMIT)
def reset(request):
    _reset(request)

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
            script("""
                   document.addEventListener('keydown', e => hypergen.callback('/djangolander/keydown/', [e.key], {}))
                   document.addEventListener('keyup', e => hypergen.callback('/djangolander/keyup/', [e.key], {}))
            """)
            style("""
            footer {
              height: 100px;
            }
            """)

        with body():
            h1("Django lander")
            p(strong("Made with hypergen"))
            p("Really stupid way to use hypergen, only here because its fun")
            p(i("Use space and arrows"))
            # button("reset", id_="reset", onclick=callback(reset), focus=False)
            with div(id_="content"):
                yield



rocket_html = """
<svg class="figure" viewBox="0 0 508 268" aria-hidden="true">
          <path d="M305.2 156.6c0 4.6-.5 9-1.6 13.2-2.5-4.4-5.6-8.4-9.2-12-4.6-4.6-10-8.4-16-11.2 2.8-11.2 4.5-22.9 5-34.6 1.8 1.4 3.5 2.9 5 4.5 10.5 10.3 16.8 24.5 16.8 40.1zm-75-10c-6 2.8-11.4 6.6-16 11.2-3.5 3.6-6.6 7.6-9.1 12-1-4.3-1.6-8.7-1.6-13.2 0-15.7 6.3-29.9 16.6-40.1 1.6-1.6 3.3-3.1 5.1-4.5.6 11.8 2.2 23.4 5 34.6z" fill="#2E3B39" fill-rule="nonzero"/>
          <path d="M282.981 152.6c16.125-48.1 6.375-104-29.25-142.6-35.625 38.5-45.25 94.5-29.25 142.6h58.5z" stroke="#FFF" stroke-width="3.396" fill="#6DDCBD"/>
          <path d="M271 29.7c-4.4-10.6-9.9-20.6-16.6-29.7-6.7 9-12.2 19-16.6 29.7H271z" stroke="#FFF" stroke-width="3" fill="#2E3B39"/>
          <circle fill="#FFF" cx="254.3" cy="76.8" r="15.5"/>
          <circle stroke="#FFF" stroke-width="7" fill="#6DDCBD" cx="254.3" cy="76.8" r="12.2"/>
          <path fill="#6DDCBD" d="M239 152h30v8h-30z"/>
          <path class="exhaust__line" fill="#E6E9EE" d="M250 172h7v90h-7z"/>
          <path class="flame" d="M250.27 178.834l-5.32-8.93s-2.47-5.7 3.458-6.118h10.26s6.232.266 3.306 6.194l-5.244 8.93s-3.23 4.37-6.46 0v-.076z" fill="#AA2247"/>
</svg>
"""


def rocket(x, y, r):
    with div(style={'position': 'fixed', 'width': '150px', 'transform': f'translate(-50%, -50%) rotate({r}deg)',
                    'left': f'{x}px', 'top': f'{y}px'}):
        raw(rocket_html)


g = 0.02
thrust = 0.2


def get_state(request):
    state = request.session.get('state', dict(
        x=500,
        y=0,
        r=0,
        dx=0,
        dy=0,
        pressed=[]
    ))
    return dotdict(state)


def set_state(request, state):
    request.session['state'] = state


# @liveview(perm=NO_PERM_REQUIRED, base_template=base_template, user_plugins=[WebsocketPlugin()])
# def lander2(request):
#     from channels.http import AsgiRequest
#     # @consumer decorated functions are reversible with the ".reverse()" helper.
#     websocket_url = receive_message.reverse()
#
#     # Open a websocket on the client. Can be closed at any point with: command("hypergen_websockets.close", url)
#     command("hypergen_websockets.open", websocket_url)
#
#     # Some custom styling.
#     style(""" input, textarea {width: 100%} """)
#
#     # The consumer will write here.
#     with p(id="counter"):
#         raw("&nbsp;")
#
#     # The input field where the user types the chat message.
#     input_(
#         id_="message",
#         type_="text",
#         placeholder="Write your message here and press enter.",
#         autofocus=True,
#         # This callbacks goes to the ChatConsumer in websockets.consumers, because the url starts with "ws://"
#         # or "wss://".
#         # Will only trigger when the user presses Enter.
#         onkeyup=callback(websocket_url, THIS, when=["hypergen.when.keycode", "Enter"], clear=True),
#     )
#
#     # Chat messages are shown here.
#     ul(id_="messages")
#
# # Automatically creates a consumer and creates a url route for it. Works with autoconsumers() in the routing.py
# # file. No other setup needed. It takes the same arguments as @action.
# @consumer(perm=NO_PERM_REQUIRED, target_id="counter")
# def receive_message(consumer, request, message):
#     # Automatically receives the channels consumer class instance and the request first.
#     # Then it takes the arguments from the callback.
#
#     # Ignore empty messages.
#     if not message:
#         return
#
#     # Writes into the "counter" id.
#     span("Length of last message is: ", len(message))
#
#     # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
#     command("hypergen.append", "messages", hypergen(lambda: li(message)))

@liveview(perm=NO_PERM_REQUIRED, base_template=lander_base_template, target_id="content")
def lander(request):
    state = get_state(request)
    style(f"""
    .exhaust__line {
    "{display: none;}" if not ' ' in state.pressed else ""
    }
    """
          )
    rocket(state.x, state.y, state.r)
    script("""
    document.activeElement.blur();
    setTimeout(() => hypergen.callback('/djangolander/update/', [], {}), 20)""")


@action(perm=NO_PERM_REQUIRED, target_id="content")
def update(request):
    state = get_state(request)
    if 'ArrowLeft' in state.pressed:
        state.r -= 1
    if 'ArrowRight' in state.pressed:
        state.r += 1

    state.dy += g - (math.cos(math.radians(state.r)) * thrust if ' ' in state.pressed else 0)
    state.dx += math.sin(math.radians(state.r)) * thrust if ' ' in state.pressed else 0
    state.x += state.dx
    state.y += state.dy
    set_state(request, state)

@action(perm=NO_PERM_REQUIRED, target_id=OMIT)
def keydown(request, keycode):
    state = get_state(request)
    if keycode not in state.pressed:
        state.pressed.append(keycode)
        set_state(request, state)

@action(perm=NO_PERM_REQUIRED, target_id=OMIT)
def keyup(request, keycode):
    state = get_state(request)
    if keycode in state.pressed:
        state.pressed.remove(keycode)
        set_state(request, state)

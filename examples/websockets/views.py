from hypergen.imports import *
from django.templatetags.static import static
from website.templates2 import base_example_template

WS_URL = "ws://127.0.0.1:8002/ws/chat/hypergen/"

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def chat(request):
    script(src=static("hypergen/v2/websockets.min.js"))
    command("hypergen_websockets.open", WS_URL)
    style(""" input, textarea {width: 100%} """)
    input_(
        id_="message",
        type_="text",
        placeholder="Write your message here and press enter.",
        autofocus=True,
        onkeyup=callback(WS_URL, THIS, when=["hypergen.when.keycode", "Enter"], clear=True),
    )
    ul(id_="messages")

def websocket(group_name=None, channel_name=None, target_id=None):
    return lambda *a, **kw: None

N = 0

@websocket(group_name="chat", channel_name="message", target_id="num-messages")
def chat_message(msg):
    global N

    N += 1
    p("You have", N, "messages in total.", sep=" ")
    command("hypergen.append", "messages", hypergen(lambda: li(msg)))
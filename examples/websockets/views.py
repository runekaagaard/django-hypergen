from hypergen.imports import *
from website.templates2 import base_example_template, show_sources
### chat ###

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def chat(request):
    # Channels urls are not reversible the same as vanilla urls. Little helper to add protocol and port.
    url = ws_url("/ws/chat/hypergen/")

    # Open a websocket on the client. Can be closed at any point with: command("hypergen.websocket.close", url)
    command("hypergen.websocket.open", url)

    # Some custom styling.
    style(""" input, textarea {width: 100%} """)

    # The consumer will write here.
    with p(id="counter"):
        raw("&nbsp;")

    # The input field where the user types the chat message.
    input_(
        id_="message",
        type_="text",
        placeholder="Write your message here and press enter.",
        autofocus=True,
        # This callbacks goes to the ChatConsumer in websockets.consumers, because the url starts with "ws://"
        # or "wss://".
        # Will only trigger when the user presses Enter.
        onkeyup=callback(url, "chat__message", THIS, when=["hypergen.when.keycode", "Enter"], clear=True),
    )

    # Chat messages are shown here.
    ul(id_="messages")

    # Backend send.
    p("Visit", a("this page", href=send_message_from_backend.reverse(), target="_blank"),
        "to try sending a chat message from the backend.", sep=" ", end=".")

    show_sources(__file__)

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def send_message_from_backend(request):
    group_send(receive_message.group_name(), ["alert", "YO"])

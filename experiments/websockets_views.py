from hypergen.imports import *
from website.templates2 import base_example_template

#                                                                     ↓ Remember to add the plugin
@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template, user_plugins=[WebsocketPlugin()])
def chat(request):
    # Open a websocket on the client. Can be closed at any point with: command("hypergen_websockets.close", url)
    command("hypergen_websockets.open", submit_chat_message.reverse())

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
        onkeyup=callback(submit_chat_message.reverse(), THIS, when=["hypergen.when.keycode", "Enter"], clear=True),
    )

    # Chat messages are shown here.
    ul(id_="messages")

@websocket(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def submit_chat_message(request, message):
    # Writes into the "counter" id.
    span("Length of last message is: ", len(message))

    # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
    command("hypergen.append", "messages", hypergen(lambda: li(message)))

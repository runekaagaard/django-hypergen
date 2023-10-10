from hypergen.imports import *
from website.templates2 import base_example_template, show_sources
"""
This file has two examples of using websockets in Hypergen:

chat: Using a consumer in normal channels fashion.
chat2: Using the @consumer decorator to avoid all the boilerplate.
"""

### chat ###

#                                                                     ↓ Remember to add the plugin
@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template, user_plugins=[WebsocketPlugin()])
def chat(request):
    # Channels urls are not reversible the same as vanilla urls. Little helper to add protocol and port.
    url = ws_url("/ws/chat/hypergen/")

    # Open a websocket on the client. Can be closed at any point with: command("hypergen_websockets.close", url)
    command("hypergen_websockets.open", url)

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
        onkeyup=callback(url, THIS, when=["hypergen.when.keycode", "Enter"], clear=True),
    )

    # Chat messages are shown here.
    ul(id_="messages")

### chat2 ###

#                                                                     ↓ Remember to add the plugin
@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template, user_plugins=[WebsocketPlugin()])
def chat2(request):
    # @consumer decorated functions are reversible with the ".reverse()" helper.
    websocket_url = receive_message.reverse()

    # Open a websocket on the client. Can be closed at any point with: command("hypergen_websockets.close", url)
    command("hypergen_websockets.open", websocket_url)

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
        onkeyup=callback(websocket_url, THIS, when=["hypergen.when.keycode", "Enter"], clear=True),
    )

    # Chat messages are shown here.
    ul(id_="messages")

    show_sources(__file__)

# Automatically creates a consumer and creates a url route for it. Works with autoconsumers() in the routing.py
# file. No other setup needed. It takes the same arguments as @action.
@consumer(perm=NO_PERM_REQUIRED, target_id="counter")
def receive_message(consumer, request, message):
    # Automatically receives the channels consumer class instance and the request first.
    # Then it takes the arguments from the callback.

    # Ignore empty messages.
    if not message:
        return

    # Writes into the "counter" id.
    span("Length of last message is: ", len(message))

    # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
    command("hypergen.append", "messages", hypergen(lambda: li(message)))

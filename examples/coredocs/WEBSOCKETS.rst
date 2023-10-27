Websockets
==========

Websockets in Hypergen provide a mechanism for real-time, bidirectional communication between the server and the browser. Unlike the traditional HTTP protocol, where the client always initiates the request, Websockets allow both the client and the server to transmit data independently. 

All websocket functionality are built on top of `Django Channels <https://channels.readthedocs.io/en/stable/>`_ and live in the ``hypergen.websocket`` module. Import everything like this::

    from hypergen.websocket import *

or truly everything::

    from hypergen.imports import *

You might want to read up on `liveviews </coredocs/liveviews/>`_ and `channels <https://channels.readthedocs.io/en/stable/>`_ before moving along.

Prerequisites
=============

You need at least the following:

- Pip install ``channels >= 4`` and ``daphne >= 4``.
- Add ``"daphne"`` to the beginning of your INSTALLED_APPS. Daphe takes over the runserver command with its own async version.
- Create ``routing.py`` files in each app mirroring the app ``urls.py`` files defining websocket urlpatterns for you app, which looks something like below. The ``as_asgi`` method takes a required ``perm`` parameter and an optional ``any_perm`` like ``@liveview``s do::

    from hypergen.imports import NO_PERM_REQUIRED
    from django.urls import path
    from websockets import consumers

    websocket_urlpatterns = [path(r'ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi(
        perm=NO_PERM_REQUIRED))]
- Create a project wide ``routing.py`` mirroring the project ``urls.py`` file collecting websocket urlpatterns from all your apps::

    import app1.routing
    import app2.routing

    websocket_urlpatterns = app1.routing.websocket_urlpatterns + app2.routing.websocket_urlpatterns
- Create a asgi.py file. It should setup both web and websockets, and include the routings to your consumers. It should look something like this::

    import os
    
    import django
    from django.core.asgi import get_asgi_application
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.security.websocket import AllowedHostsOriginValidator

    # Initialize Django.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings') # adjust to your setup.
    django.setup()

    # Import project-wide routing file.
    import routing # adjust to your setup.

    # Run both web and websocket protocols.
    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        # Add the projects websocket consumers.
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)))})

Basics
======

The cornerstone of hypergen websockets is the ``HypergenWebsocketConsumer`` class. A HypergenWebsocketConsumer has all the capabilities of a standard Django Channels consumer but adds hypergen integration. It checks permissions and like an ``@action``, it can update HTML on the page and issue other client side commands.

A very simple consumer could look like this::

    class IncrementConsumer(HypergenWebsocketConsumer):
        def receive_hypergen_callback(self, n):
            # Render the self.template method into the DOM element with an id of "counter".
            # First we get the client side commands ...
            commands = hypergen(self.template, message, settings=dict(action=True, returns=COMMANDS,
                target_id="counter"))
            # And then we ship them to the frontend.
            self.channel_send_hypergen_commands(commands)

        def template(n):
            span("The number is", n + 1)

When the consumer receives as message, it directs the frontend page listening to the websocket channel to increment the number.

A consumers url, can't (yet) be reversed like a Django view, but you can use the ``ws_url`` helper that makes the url work both when developing and in production based on the value of ``settings.DEBUG``::

    consumer_url = ws_url("ws/chat/jokes")

A consumer should be opened on the liveview where it is needed::

    @liveview(perm="chat.can_chat", path="<slug:chatroom_name>")
    def chatroom(request, chatroom_name)
        consumer_url = ws_url(f"ws/chat/{chatroom_name}")
        command("hypergen.websocket.open", consumer_url)

From the frontend side issuing a command to a consumer, is similar to using an @action::

    message = textarea(id_="message")
    button(id_="send", onclick=callback(consumer_url, {"type": "chat__client_chatroom_message", "message": message}))

Use the ``receive_callback()`` method on your consumer class to receive events from the client::

    class ChatConsumer(HypergenWebsocketConsumer):
        def receive_hypergen_callback(self, event):
            # Remember! Trust nothing from the client.
            if event["type"] == "chat__client_chatroom_message":
                # Handle event.

From the backend side you can use the ``group_send`` function provided by hypergen::

    from hypergen.imports import group_send
    group_send("my_consumer_group_name", {"type": "chat__server_chatroom_message", "message": "Hi!"})

Which would then magically (by the ``dispatch()`` method) be available in a ``chat__server_chatroom_message(self, event)`` method.

Get commands to update HTML on the page and other client side commands, by first using the ``action=True`` and ``returns=COMMANDS`` settings to the ``hypergen`` function::

    commands = hypergen(template, message, settings=dict(action=True, returns=COMMANDS, target_id="counter"))

Then create standard templates like you would in an action::

    def template(message)::
        # Writes into the "counter" id.
        span("Length of last message is: ", len(message))

        # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
        command("hypergen.append", "messages", hypergen(lambda: li(message)))
        
Finally send the commands to either the consumer channel itself or an entire group::

    # Only the websocket itself:
    self.channel_send_hypergen_commands(commands)
    # The entire group:
    self.group_send_hypergen_commands(self.group_name, commands)
    
Full example
============
        
Consumer class::

    from hypergen.imports import *

    class ChatConsumer(HypergenWebsocketConsumer):
        group_name = "websockets__consumers__ChatConsumer"

        # django-channels will automatically subscribe the consumer to these groups.
        groups = [group_name]

        # Receives the data sent from the onkeyup callback in views.py.
        def receive_hypergen_callback(self, event_type, *args):
            if event_type == "chat__message_from_frontend":
                message, = args
                assert type(message) is str
                message = message.strip()[:1000]
                if message:
                    commands = self.update_page(message)
                    # Send commands to entire group.
                    self.group_send_hypergen_commands(self.group_name, commands)

            # ... More event types goes here.

        def chat__message_from_backend(self, event):
            commands = self.update_page(event["message"])
            # Send commands to individual channel.
            self.channel_send_hypergen_commands(commands)

        def update_page(self, message):
            return hypergen(self.template, message, settings=dict(action=True, returns=COMMANDS, target_id="counter"))

        # Render the HTML and issue custom commands.
        def template(self, message):
            # Writes into the "counter" id.
            span("Length of last message is: ", len(message))

            # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
            command("hypergen.append", "messages", hypergen(lambda: li(message)))

@liveview::

    # Channels urls are not (yet) reversible the same as vanilla urls. Little helper to add protocol and port.
    chat_ws_url = lambda: ws_url("/ws/chat/hypergen/")

    @liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
    def chat(request):
        h3("Websockets chat")
        p("Open multiple tabs to see messages pushed out to all listening consumers.")
        # Open a websocket on the client. Can be closed at any point with: command("hypergen.websocket.close", url)
        command("hypergen.websocket.open", chat_ws_url())

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
            onkeyup=callback(chat_ws_url(), "chat__message_from_frontend", THIS, when=["hypergen.when.keycode", "Enter"],
            clear=True),
        )

        # Chat messages are shown here.
        ul(id_="messages")

        # Backend send.
        p("Visit", a("this page", href=send_message_from_backend.reverse(), target="_blank"),
            "to try sending a chat message from the backend.", sep=" ", end=".")

Server side event::

    @liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
    def send_message_from_backend(request):
        from websockets.consumers import ChatConsumer
        group_send(ChatConsumer.group_name, {"type": "chat__message_from_backend", "message": "Server message!"})
        command("alert", "Message will appear in the chatroom!")

Opening and closing a websocket
===============================

You can open auto-reconnecting websockets courtesy of the Sockety project by doing::

    command("hypergen.websocket.open", my_consumer.reverse())

and to undo the damage::

    command("hypergen.websocket.close", my_consumer.reverse())

Hypergen automatically reconnects websockets connections sensibly, for instance after being offline.

Details
=======

The full signature for the ``HypergenWebsocketConsumer`` class is:

*class HypergenWebsocketConsumer()*
    *as_asgi(perm=None, any_perm=False)*
        Static method that returns the ASGI application. ``perm`` is required.
        
        *perm (None)*
            Accepts one or a list of permissions, all of which the user must have. See Djangos `has_perm() <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`_
        *any_perm (False)*
            The user is only required to have one of the given perms. Check which he has in ``context.hypergen.matched_perms``.

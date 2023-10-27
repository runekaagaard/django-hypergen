Websocket
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
- Create ``routing.py`` files in each app mirroring the app ``urls.py`` files defining websocket urlpatterns for you app, which looks something like this::

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

The cornerstone of hypergen websockets is the ``@consumer`` decorator. When used in conjunction with ``@autoconsumers`` in the ``routing.py`` file, hypergen automatically generates url paths and `group names <https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups>`_ for each consumer.

A consumer has all the capabilities of an ``@action``, it can update HTML on the page and issue client side commands.

A very simple consumer could look like this::

    @consumer(perm="chat.group_message", path="<chatgroup_name:slug>", target_id="counter")
    def message_chatgroup(request, consumer, chatgroup_name, message):
        span("Number of messages: ", increment_counter())
        command("hypergen.append", "mychat", message)

When the consumer receives as message, it directs all frontend pages listening to the websocket channel to append the message to DOM element with the ``"mychat"`` id.

Get consumer can be accessed from the frontend via its url::

    url = message_chatgroup.reverse(chatgroup_name="VIP")

and from the backend via its group name::

    group_name = message_chatgroup.group_name(chatgroup_name="VIP")

A consumer should be opened on the view where it is needed::

    @liveview(perm="chat.group_message")
    def show_chats(consumer, request)
        command("hypergen.websocket.open", message_chatgroup.reverse(chatgroup_name="VIP"))

From the frontend side issuing a command to a @consumer, is similar to using an @action::

    button(onclick=callback(message_chatgroup.reverse(chatgroup_name="VIP"), "WUSSUP!"))


From the backend side you can use the `group_send` function provided by hypergen::

    from hypergen.channels import group_send

    group_send(message_chatgroup.group_name(chatgroup_name="VIP"), "YO!")
    
Full example
============
        
::

    @contextmanager
    def base_template():
        docblock()
        with html():
            with body():
                with div(id="content"):
                    yield

    base_template.target_id = "content"
    
    def template(n):
        count = input(id="count", value=N, disabled=True)
        button("Increment", onclick=callback(increment, count))
    
    @liveview(perm=NO_PERM_REQUIRED, base_example=base_example)
    def counter(request, count):
        command("hypergen.websocket.open", increment.reverse())
        template(1)

    @consumer(perm=NO_PERM_REQUIRED, base_example=base_example)
    def increment(consumer, request, count):
        template(count+1)

``@consumer`` takes all the same keyword arguments as ``@action`` as well as a couple of websocket specific ones.

Instead of taking the request like an action function does, a consumer function takes the `consumer <https://channels.readthedocs.io/en/stable/topics/consumers.html>`_ instance as it's first argument, then a django `ASGIRequest <https://github.com/django/django/blob/8adc7c86ab85ed91e512bc49056e301cbe1715d0/django/core/handlers/asgi.py#L38>`_ instance that works mostly like a regular Django request.

Among other things, that mean you can keep your app state by setting properties on the consumer instance::

    @consumer(perm=NO_PERM_REQUIRED, target_id="content")
    def my_consumer(consumer, request):
        if not hasattr(consumer, "my_app_state"):
            consumer.my_app_state = [1, 2, 3]

        my_template(consumer.my_app_state)

Hypergen automatically reconnects websockets connections sensibly, for instance after being offline.

Opening and closing a websocket
===============================

You can open auto-reconnecting websockets courtesy of the Sockety project by doing::

    command("hypergen.websocket.open", my_consumer.reverse())

and to undo the damage::

    command("hypergen.websocket.close", my_consumer.reverse())
    
Groups
------

Hypergen automatically creates `groups <https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups>`_ based on the url to the consumer, i.e. websockets connecting to the same url, can speak to each other.

To get the group name of a consumer, symmetrically to reverse you would do::

    my_consumer.group_name("42", bar="hello")

So to have multiple chatrooms where all connected the same chatroom receives the same messages you would do::

    from hypergen.imports import *
    from hypergen import js
    
    @consumer(perm="chat.can_chat", path="chat/<slug:room_name>")
    def send_message(consumer, message):
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

And to send messages to the chat room, just use ``callback`` normally::

    @liveview(perm="chat.can_chat")
    def chat(request):
        message = input(id="message")
        button("Send", onclick=callback(send_message.reverse(room_name="nice_people_only_room"), message))
        
Custom group names can be defined by using the ``group_name`` keyword argument to the ``@consumer`` decorator. It
expects a callback that takes the consumer as it's only argument and returns the group name as a string::

    @consumer(perm=NO_PERM_REQUIRED, group_name=lambda consumer: "vip_group")
    def send_message(consumer, request, message):
        ...

Programatically sending messages
--------------------------------

To communicate to a consumer, from the backend you use the consumer_command function::

    from hypergen.imports import consumer_command

    consumer_command(my_consumer.group_name("my_arg", my_kwargs=42), [["alert", 42]])

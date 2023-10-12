Websockets
==========

Hypergen supports realtime 2-way communication with the server via the websocket protocol.

You might want to read up on `liveviews </coredocs/liveviews/>`_ and `channels <https://channels.readthedocs.io/en/stable/>`_ before continuing.

As we would use the ``@action`` decorator for normal request/response communication we can use the very similar ``@consumer`` decorator for websockets::

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

So to have multiple chatrooms where all connected the same chatroom receives the same messages you would do::

    from hypergen.imports import *
    from hypergen import js
    
    @consumer(perm="chat.can_chat", path="chat/<slug:room_name>")
    def send_message(consumer, message):
        js.append("messages", hypergen(lambda: li(message)))

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

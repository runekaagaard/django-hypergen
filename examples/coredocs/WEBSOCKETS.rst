Websockets
==========

Hypergen supports realtime 2-way communication with the server via the websocket protocol. As we would use the ``@action`` decorator for normal request/response communication we can use the very similar ``@consumer`` decorator for websockets::

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
        template(1)

    @consumer(perm=NO_PERM_REQUIRED, base_example=base_example)
    def increment(consumer, count):
        template(count+1)

If that looks confusing to you, we recommend you read about `liveviews </coredocs/liveviews/>`_ first.

``@consumer`` takes all the same keyword arguments as ``@action`` as well as a couple of websocket specific ones.

Instead of taking the request like an action function does, a consumer function takes the `consumer <https://channels.readthedocs.io/en/stable/topics/consumers.html>`_ instance as it's first argument. Among other things, that mean you can keep your app state by setting properties on the consumer instance::

    @consumer(perm=NO_PERM_REQUIRED, target_id="content")
    def my_consumer(consumer):
        if not hasattr(consumer, "my_app_state"):
            consumer.my_app_state = [1, 2, 3]

        my_template(consumer.my_app_state)

You don't have to worry about opening and closing websocket connections - Hypergen takes care of that for you. It also
reconnects connections sensibly, for instance after being offline.

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
    def my_consumer(consumer):
        ...
        
Multiplexing
------------

A common issue with django channels is that you have either too complex consumers or too many open websockets at the
same time.

Hypergen transparently supports multiplexing with help from the `channelsmultiplexer <https://github.com/hishnash/channelsmultiplexer>`_ project. Simply use the ``multiplexer`` keyword argument to the ``@consumer`` decorator and
consumers with the same value will share a websocket connection::

    @consumer(perm=NO_PERM_REQUIRED, multiplexer="myapp")
    def my_consumer1(consumer):
        ...
        
    @consumer(perm=NO_PERM_REQUIRED, multiplexer="myapp")
    def my_consumer2(consumer):
        ...

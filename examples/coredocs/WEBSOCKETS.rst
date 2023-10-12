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

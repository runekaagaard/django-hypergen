import json
from functools import wraps

d = dict

from hypergen.imports import *
from hypergen.hypergen import check_perms

from django.conf import settings

try:
    from asgiref.sync import async_to_sync
    from django.core.handlers.asgi import ASGIRequest
    from channels.generic.websocket import JsonWebsocketConsumer
    from channels.layers import get_channel_layer
    from channels.consumer import database_sync_to_async, get_handler_name

    def assert_channels():
        pass
except ImportError:

    def assert_channels():
        if getattr(settings, "HYPERGEN_INTERNAL_ONLY_ENFORCE_ASSERT_CHANNELS", True):
            raise Exception(
                "To use channels you must do 'pip install daphne >= 4.0.0, channels daphne >= 4.0.0 and channels-redis >= 4.1.0'. Notice channels requires Django >= 3.2."
            )

    class JsonWebsocketConsumer(object):
        def __init__(*args, **kwargs):
            pass

        def as_asgi(*args, **kwargs):
            return JsonWebsocketConsumer

    def database_sync_to_async(*args, **kwargs):
        pass

__all__ = ["HypergenWebsocketConsumer", "ws_url", "group_send"]

class HypergenWebsocketConsumer(JsonWebsocketConsumer):

    groups = None

    def __init__(self, perm=None, any_perm=False):
        self.perm = perm
        self.any_perm = perm

        super(HypergenWebsocketConsumer, self).__init__()

    def connect(self):
        assert_channels()
        super(JsonWebsocketConsumer, self).connect()

    def receive_json(self, content):
        perms_ok, _, matched_perms = check_perms(self.get_request(), self.perm, any_perm=self.any_perm)
        if perms_ok is not True:
            self.send_permission_denied()
            return

        # TODO: Check for a custom header too.
        if type(content) is dict and "args" in content and "meta" in content:
            with context(request=self.get_request()), context(at="hypergen", matched_perms=matched_perms):
                self.receive_hypergen_callback(*content["args"])

    def receive_hypergen_callback(self, *args, **kwargs):
        raise NotImplementedError("Please implement your own receive_hypergen_callback() method.")

    def get_request(self):
        self.scope["method"] = "WS"
        request = ASGIRequest(self.scope, None)
        request.user = self.scope["user"]

        return request

    def send_permission_denied(self):
        self.channel_send_hypergen_commands([["console.error", "Permission denied"]])

    def channel_send(self, event):
        async_to_sync(self.channel_layer.send)(self.channel_name, event)

    def group_send(self, group_name, event):
        async_to_sync(self.channel_layer.group_send)(group_name, event)

    def group_send_hypergen_commands(self, group_name, commands):
        self.group_send(group_name,
            {'type': 'hypergen__send_hypergen_commands', 'commands': json.loads(self.encode_json(commands))})

    def channel_send_hypergen_commands(self, commands):
        self.channel_send({
            'type': 'hypergen__send_hypergen_commands', 'commands': json.loads(self.encode_json(commands))})

    def hypergen__send_hypergen_commands(self, event):
        self.send_json(event['commands'])

    @database_sync_to_async
    def dispatch(self, message):
        """
        Dispatches incoming messages to type-based handlers asynchronously.
        """
        # Get and execute the handler
        handler = getattr(self, get_handler_name(message), None)
        if handler:
            with context(request=self.get_request()), context(at="hypergen", matched_perms=[]):
                handler(message)
        else:
            raise ValueError("No handler for message type %s" % message["type"])

    @classmethod
    def decode_json(cls, text_data):
        return loads(text_data)

    @classmethod
    def encode_json(cls, content):
        return dumps(content)

def ws_url(url):
    absolute_url = context.request.build_absolute_uri(url)
    if settings.DEBUG:
        return absolute_url.replace("http://", "ws://").replace("https://", "wss://")
    else:
        return context.request.build_absolute_uri(url).replace("http://", "wss://").replace("https://", "wss://")

def group_send(group_name, event):
    channel_layer = get_channel_layer()  #
    async_to_sync(channel_layer.group_send)(group_name, event)

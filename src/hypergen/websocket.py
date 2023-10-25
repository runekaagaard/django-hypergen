import json
from functools import wraps

d = dict

from hypergen.imports import *
from hypergen.hypergen import check_perms
from hypergen.hypergen import wrap2, check_perms, autourl_register

from django.core.exceptions import PermissionDenied
from django.templatetags.static import static
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings

try:
    from asgiref.sync import async_to_sync
    from django.core.handlers.asgi import ASGIRequest
    from channels.generic.websocket import JsonWebsocketConsumer
    from channels.layers import get_channel_layer

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

__all__ = ["HypergenWebsocketConsumer"]

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

        with context(request=self.get_request()), context(at="hypergen", matched_perms=matched_perms):
            self.receive_callback(*content["args"])

    def receive_callback(*args, **kwargs):
        raise NotImplementedError("Please implement your own receive_callback() method.")

    def get_request(self):
        self.scope["method"] = "WS"
        request = ASGIRequest(self.scope, None)
        request.user = self.scope["user"]

        return request

    def send_permission_denied(self):
        self.send_json([["console.error", "Permission denied"]])

    def group_send(self, group_name, event):
        async_to_sync(self.channel_layer.group_send)(group_name, event)

    def group_send_hypergen_commands(self, group_name, commands):
        self.group_send(group_name,
            {'type': 'hypergen__send_hypergen_commands', 'commands': json.loads(self.encode_json(commands))})

    def hypergen__send_hypergen_commands(self, event):
        self.send_json(event['commands'])

    @classmethod
    def decode_json(cls, text_data):
        return loads(text_data)

    @classmethod
    def encode_json(cls, content):
        return dumps(content)

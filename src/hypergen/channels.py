import json
from functools import wraps

d = dict

from hypergen.imports import *
from hypergen.hypergen import check_perms
from hypergen.liveview import LiveviewPluginBase
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

__all__ = ["HypergenWebsocketConsumer", "ws_url", "consumer", "group_name", "group_send"]

def get(o, k, d="__DEFAULT__"):
    value = getattr(o.Hypergen, k, "__NA__")
    if d != "__DEFAULT__":
        return value if value != "__NA__" else d
    else:
        assert value != "__NA__", f"Please set the property '{k}' on instance {o.__class__}.Hypergen"
        return value

class HypergenWebsocketConsumer(JsonWebsocketConsumer):
    def get_request(self):
        self.scope["method"] = "WS"
        request = ASGIRequest(self.scope, None)
        request.user = self.scope["user"]

        return request

    def check_perms(self, content):
        return check_perms(self.get_request(), get(self, "perm"), any_perm=get(self, "any_perm", d=False),
            raise_exception=True)

    def group_name(self):
        return ".".join([self.__class__.__module__, self.__class__.__name__] + list(self.scope['url_route']['args']) +
            [f"{k}__{v}" for k, v in self.scope['url_route']['kwargs'].items()])

    def connect(self):
        assert_channels()
        async_to_sync(self.channel_layer.group_add)(self.group_name(), self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name(), self.channel_name)

    def receive_json(self, content):
        try:
            ok, __, matched_perms = self.check_perms(content)
        except PermissionDenied:
            async_to_sync(self.channel_layer.group_send)(self.group_name(),
                {'type': 'send_hypergen', 'commands': [["console.error", "Permission denied"]]})
            return

        base_template = get(self, "base_template", None)
        if base_template is not None and hasattr(base_template, "target_id"):
            target_id = getattr(base_template, "target_id")
        else:
            target_id = get(self, "target_id")

        with context(request=self.get_request()), context(at="hypergen", matched_perms=matched_perms):
            commands = hypergen(
                self.receive_hypergen, *content['args'], settings=d(action=True, returns=COMMANDS,
                target_id=target_id, user_plugins=get(self, "user_plugins", [])))

            # The data send to group_send() needs to be somehing that can be msgpacked. Therefore we change
            # nonserializable types like dates to hypergen custom datatypes like {"_": ["date", ["2022-01-01"]]}
            # before sending it to msgpack. Is there a better way?
            async_to_sync(self.channel_layer.group_send)(self.group_name(),
                {'type': 'send_hypergen', 'commands': json.loads(dumps(commands))})

    def receive_hypergen(*args, **kwargs):
        raise NotImplementedError("Please implement your own receive_hypergen() method.")

    def send_hypergen(self, event):
        self.send(dumps(event['commands']))

    @classmethod
    def decode_json(cls, text_data):
        return loads(text_data)

    @classmethod
    def encode_json(cls, content):
        return dumps(content)

class HypergenWebsocketAutoConsumer(HypergenWebsocketConsumer):
    def group_name(self):
        return ".".join([self.hypergen_func.__module__, self.hypergen_func.__name__] +
            list(self.scope['url_route']['args']) +
            [f"{k}__{v}" for k, v in self.scope['url_route']['kwargs'].items()])

    def receive_json(self, content):
        try:
            request = self.get_request()
            with context(request=request):
                commands = self.hypergen_func(request, *content['args'])

            async_to_sync(self.channel_layer.group_send)(self.group_name(),
                {'type': 'send_hypergen', 'commands': json.loads(dumps(commands))})
        except Exception as e:
            # TODO: Why are errors here hidden in daphnes output?
            import traceback
            traceback.print_exc()
            raise

def ws_url(url):
    absolute_url = context.request.build_absolute_uri(url)
    if settings.DEBUG:
        return absolute_url.replace("http://", "ws://").replace("https://", "wss://")
    else:
        return context.request.build_absolute_uri(url).replace("http://", "wss://").replace("https://", "wss://")

def group_name(consumer_func, *view_args, **view_kwargs):
    return ".".join([consumer_func.__module__, consumer_func.__name__] + list(view_args) +
        [f"{k}__{v}" for k, v in view_kwargs.items()])

def group_send(group_name, command):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {
        "type": "send_hypergen",
        "commands": [command],})

@wrap2
def consumer(func, path=None, re_path=None, base_template=None, target_id=None, perm=None, any_perm=False,
    autourl=True, partial=True, base_view=None, appstate=None, user_plugins=[]):
    assert_channels()
    if perm != NO_PERM_REQUIRED:
        assert perm, "perm is a required keyword argument"
    if target_id is None:
        target_id = getattr(base_template, "target_id", None)
    if base_template and partial and not target_id:
        raise Exception("{}: Partial loading requires a target_id. Either as a kwarg or"
            " an attribute on the base_template function.".format(func))
    partial_base_template = base_template if partial else None
    if user_plugins is None:
        user_plugins = []

    @wraps(func)
    def _(consumer, request, *args, **kwargs):
        # Ensure correct permissions
        try:
            ok, __, matched_perms = check_perms(request, perm, any_perm=any_perm, raise_exception=True)
        except PermissionDenied:
            return [["console.error", "PermissionDenied."]]

        if ok is not True:
            raise Exception("Should not happen!")

        with context(
                at="hypergen",
                matched_perms=matched_perms,
                partial_base_template=partial_base_template,
                #liveview_resolver_match=liveview_resolver_match(for_action=True)
        ):
            full = hypergen(
                func, consumer, request, *args, **kwargs, settings=d(action=True, returns=FULL, target_id=target_id,
                appstate=appstate, base_view=base_view, user_plugins=user_plugins))
            if isinstance(full["template_result"], HttpResponseRedirect):
                # Allow to return a redirect response directly from an action.
                return [["hypergen.redirect", full["template_result"]["Location"]]]
            elif isinstance(full["template_result"], HttpResponse):
                raise Exception("Consumers cannot return HttpResponse objects.")
            elif type(full["template_result"]) is list:
                return full["template_result"]
            else:
                return full["context"]["hypergen"]["commands"]

    def group_name_(*view_args, **view_kwargs):
        return group_name(func, *view_kwargs, **view_kwargs)

    _.group_name = group_name_

    if autourl:
        assert not all((path, re_path)), "Only one of path= or re_path= must be set when autourl=True"
        autourl_register(_, base_template=base_template, path=path, re_path=re_path, channels=True)

    _.supports_hypergen_callback = True

    return _

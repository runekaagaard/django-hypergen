import json

d = dict

from hypergen.imports import *
from hypergen.hypergen import check_perms
from hypergen.liveview import LiveviewPluginBase

from django.core.exceptions import PermissionDenied
from django.templatetags.static import static

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

__all__ = ["HypergenWebsocketConsumer", "ws_url", "WebsocketPlugin"]

class WebsocketPlugin(LiveviewPluginBase):
    def process_html(self, html):
        def template():
            raw("<!--hypergen_websocket_media-->")
            script(src=static("hypergen/v2/websockets.min.js"))

        # Inject media.
        if "<head>" in html:
            assert html.count("<head>") == 1, "Ooops, multiple <head> tags found. There can be only one!"
            return html.replace("<head>", "<head>" + hypergen(template))
        elif "<html>" in html:
            assert html.count("<html>") == 1, "Ooops, multiple <html> tags found. There can be only one!"
            return html.replace("<html>", "<html><head>" + hypergen(template) + "</head>")
        else:
            return hypergen(template) + html

class WebsocketRequest():
    def __init__(self, consumer):
        self.user = consumer.scope["user"]

def get(o, k, d="__DEFAULT__"):
    value = getattr(o.Hypergen, k, "__NA__")
    if d != "__DEFAULT__":
        return value if value != "__NA__" else d
    else:
        assert value != "__NA__", f"Please set the property '{k}' on instance {o.__class__}.Hypergen"
        return value

class HypergenWebsocketConsumer(JsonWebsocketConsumer):
    def get_request(self):
        return WebsocketRequest(self)

    def check_perms(self, content):
        return check_perms(self.get_request(), get(self, "perm"), any_perm=get(self, "any_perm", d=False),
            raise_exception=True)

    def group_name(self):
        return ".".join([self.__class__.__module__, self.__class__.__name__] + list(self.scope['url_route']['args']) +
            [f"{k}__{v}" for k, v in self.scope['url_route']['kwargs'].items()])

    def connect(self):
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

            # TODO: Figure out how to use a custom json_decoder here.
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

def ws_url(url):
    return context.request.build_absolute_uri(url).replace("https://", "wss://").replace("http://", "ws://")

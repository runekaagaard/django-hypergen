from hypergen.imports import *
from hypergen.liveview import encoder

d = dict

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

class WebsocketRequest():
    def __init__(self, consumer):
        self.user = consumer.scope["user"]

def get(o, k):
    value = getattr(o, k, "__NA__")
    assert value != "__NA__", f"Please set the property '{k}' on instance {o}"

    return value

class HypergenWebsocketConsumer(JsonWebsocketConsumer):
    def group_name(self):
        return ".".join([self.__class__.__module__, self.__class__.__name__] + list(self.scope['url_route']['args']) +
            [f"{k}__{v}" for k, v in self.scope['url_route']['kwargs'].items()])

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name(), self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name(), self.channel_name)

    def receive_json(self, content):
        target_id = get(self, "target_id")
        with context(request=WebsocketRequest(self)):
            commands = hypergen(self.receive_hypergen, *content['args'],
                settings=d(action=True, returns=COMMANDS, target_id=target_id))

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

class ChatConsumer(HypergenWebsocketConsumer):
    target_id = "counter"

    def receive_hypergen(self, message):
        raw(len(message))
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

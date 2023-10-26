from asgiref.sync import async_to_sync
from hypergen.imports import *
from hypergen.hypergen import check_perms
from hypergen.websocket import HypergenWebsocketConsumer

class ChatConsumer(HypergenWebsocketConsumer):
    group_name = "websockets__consumers__ChatConsumer"

    # django-channels will automatically subscribe the consumer to these groups.
    groups = [group_name]

    # Receives the data sent from the onkeyup callback in views.py.
    def receive_callback(self, event_type, *args):
        if event_type == "chat__message":
            message, = args
            assert type(message) is str
            message = message.strip()[:1000]
            if message:
                self.update_page(message)

        # ... More event types goes here.

    def chat__message_from_backend(self, event):
        self.update_page(event["message"])

    def update_page(self, message):
        commands = hypergen(self.template, message, settings=dict(action=True, returns=COMMANDS, target_id="counter"))

        # Send commands to frontend.
        self.group_send_hypergen_commands(self.group_name, commands)

    # Render the HTML and issue custom commands.
    def template(self, message):
        # Writes into the "counter" id.
        span("Length of last message is: ", len(message))

        # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

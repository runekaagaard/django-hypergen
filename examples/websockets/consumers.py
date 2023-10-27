from asgiref.sync import async_to_sync
from hypergen.imports import *
from hypergen.hypergen import check_perms
from hypergen.websocket import HypergenWebsocketConsumer

class ChatConsumer(HypergenWebsocketConsumer):
    group_name = "websockets__consumers__ChatConsumer"

    # django-channels will automatically subscribe the consumer to these groups.
    groups = [group_name]

    # Receives the data sent from the onkeyup callback in views.py.
    def receive_hypergen_callback(self, event_type, *args):
        if event_type == "chat__message_from_frontend":
            message, = args
            assert type(message) is str
            message = message.strip()[:1000]
            if message:
                commands = self.update_page(message)
                # Send commands to entire group.
                self.group_send_hypergen_commands(self.group_name, commands)

        # ... More event types goes here.

    def chat__message_from_backend(self, event):
        commands = self.update_page(event["message"])
        # Send commands to individual channel.
        self.channel_send_hypergen_commands(commands)

    def update_page(self, message):
        return hypergen(self.template, message, settings=dict(action=True, returns=COMMANDS, target_id="counter"))

    # Render the HTML and issue custom commands.
    def template(self, message):
        # Writes into the "counter" id.
        span("Length of last message is: ", len(message))

        # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

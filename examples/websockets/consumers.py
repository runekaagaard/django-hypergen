from hypergen.imports import *
from hypergen.websocket import HypergenWebsocketConsumer

class ChatConsumer(HypergenWebsocketConsumer):
    group_name = "websockets__consumers__ChatConsumer"
    groups = [group_name]

    def receive_hypergen(self, event_type, *args):
        if event_type == "chat__message":
            message, = args
            assert type(message) is str
            message = message.strip()[:1000]
            if message:
                commands = hypergen(self.update_page, message, settings=dict(action=True, returns=COMMANDS,
                    target_id="counter"))

                self.group_send_hypergen_commands(self.group_name, commands)

    # Render the HTML and send custom commands.
    def update_page(self, message):
        # Writes into the "counter" id.
        span("Length of last message is: ", len(message))

        # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

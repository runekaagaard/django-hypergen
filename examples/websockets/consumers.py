from hypergen.imports import *
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
                # Run the update_page method similar to an @action and collect commands to send to the frontend.
                commands = hypergen(self.update_page, message, settings=dict(action=True, returns=COMMANDS,
                    target_id="counter"))

                # Send commands to frontend.
                self.group_send_hypergen_commands(self.group_name, commands)
        # ... More event types goes here.

    # Render the HTML and send custom commands.
    def update_page(self, message):
        # Writes into the "counter" id.
        span("Length of last message is: ", len(message))

        # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

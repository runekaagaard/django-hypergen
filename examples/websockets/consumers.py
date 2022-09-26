from hypergen.imports import *

class ChatConsumer(HypergenWebsocketConsumer):
    # Custom group name can be set here. Defaults to the module, classname and url.
    # def group_name(self):
    #     pass

    # Custom permission checks can be done here.
    # def check_perms(self, content):
    #     pass

    # Similar settings that you would have to the @action decorator is defined here.
    class Hypergen:
        user_plugins = []  # Optional, default: []
        any_perm = False  # Optional, default: False

        # One of these two is required.
        base_template = None  # Read target_id from base_template.target_id
        target_id = "counter"

        perm = NO_PERM_REQUIRED  # Required

    # Render the HTML and send custom commands.
    def receive_hypergen(self, message):
        # Writes into the "counter" id.
        span("Length of last message is: ", len(message))

        # Appends the message to the list of messages. Uses hypergen() directly to render into a string of HTML.
        command("hypergen.append", "messages", hypergen(lambda: li(message)))

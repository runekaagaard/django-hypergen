import json

from functools import wraps

def event(perm=None, group=None):
    assert perm, "perm is required"
    assert group, "group is required"

    def _(f):
        @wraps(f)
        def __(*args, **kwargs):
            data = f(*args, **kwargs)
            data["type"] = func_path(f)

            return data

        if not hasattr(group, "events"):
            group.events = []

        group.events.append(__)

        return __

    return _

def group(perm=None):
    assert perm, "perm is required"

    def _(f):
        @wraps(f)
        def __(*args, **kwargs):
            data = f(*args, **kwargs)
            data["type"] = func_path(f)

            return data

        return __

    return _

def func_path(func):
    return f"{func.__module__}.{func.__name__}"

@group(perm="chat.can_chat")
def chatroom(chatroom_name):
    return {"chatroom_name": chatroom_name}

@event(perm="chat.can_chat", group=group)
def message(txt):
    return {"txt": txt}

class HypergenConsumer:
    def __init__(self, initial_state, *args, **kwargs):
        self.state = initial_state

    def connect(self):
        for group in self.groups:
            print("group_add", repr(json.dumps(group)))

def liveview(**kwargs):
    def _(f):
        return f

    return _

@liveview(perm="chat.can_chat", path="<slug:chatroom_name")
def chat_room(request, chatroom_name):
    # Starts websocket on the client. It will be opened to a url like:
    # wss://ws/hypergenconsumer/{groups: [{"type": "chat.websockets.group", "chatroom_name": "jokes"}]}
    consumer_url = init_consumer(HypergenConsumer, initial_state={"chatroom_name": chatroom_name})
    txt = textarea(id_="txt")
    button("Send", onclick(message.emit(consumer_url, txt)))

# testing:
print(message("I can do it!"))
print(chatroom("general"))

consumer = HypergenConsumer(groups=[chatroom("jokes")])
consumer.connect()

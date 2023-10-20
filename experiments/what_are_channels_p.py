"""
AsyncConsumer or SyncConsumer:
    channel_layer_alias = "echo_alias"
    self.scope[path, headers, method, user, url_route, etc.]
    groups = ["broadcast"]

    [async] def websocket_connect(self, event):
        [await] self.send({
            "type": "websocket.accept",
        })

    [async] def websocket_receive(self, event):
        [await] self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    websocket_disconnect
        channels.exceptions.StopConsumer

Groups?
"""

## Idea 0 ##

class ChatAppConsumer(HypergenConsumer):
    pass

@event
def user_joined_chatroom(chatroom_slug, user_id):
    return {"event_type": "user_joined_chatroom", "user_id": user_id, "chatroom_slug": chatroom_slug}

@event
def user_left_chatroom(chatroom_slug, user_id):
    return {"event_type": "user_left_chatroom", "user_id": user_id, "chatroom_slug": chatroom_slug}

@event
def message(chatroom_slug, user_id, message):
    return {"event_type": "message", "user_id": user_id, "chatroom_slug": chatroom_slug, "message": message}

@event
def notification(user_id, notification):
    return {"event_type": "notification", "user_id": user_id, "notification": notification}

@group(events=[user_joined_chatroom, user_left_chatroom, message])
def chatroom(chatroom_slug):
    """This group is for transmitting events about a single chatroom"""
    return {"group_title": "chatroom", "chatroom_slug": chatroom_slug}

@group(events=[notification])
def notifications(user_id):
    """This group is for transmitting notifications specific to the user"""
    return {"group_title": "notifications", "user_id": user_id}

@liveview(path="<slug:chatroom_slug>", perm="chat.access_chat")
def index(request, chatroom_slug):
    start_consumer(
        consumer=ChatAppConsumer, groups=[
        chatroom(chatroom_slug),
        user_joined(request.user.pk),
        user_left(request.user.pk),
        notifications(request.user.pk)])
    message_txt = textarea(id_="message_txt", placeholder="Write message here")
    button("Send", onclick=send_event(chatroom(chatroom_slug), message(message_txt)))

f

@action(listen_to_groups=[chatroom], receive_events=[message])
def receive_message(request, event):
    user = User.objects.get(pk=event["user_id"])
    command("hypergen.append", "messages_id", f"{user.username}: {event['message']}")

## Idea 1 ##

class ChatRoomConsumer(HypergenConsumer):
    path = "<slug:chatroom>"

@liveview(path="<slug:chatroom>")
def index(request, chatroom):
    message = textarea(id_="message", placeholder="Write message here")
    button("Send", onclick=callback(ChatRoomConsumer.reverse("vip"), message))

@action(consumer=ChatConsumer)
def send_message(request, message):
    command("hypergen.append", "messages_id", message)

## Idea 2 ##

@liveview(path="<slug:name>")
def chatroom(request, name):
    message = textarea(id_="message", placeholder="Write message here")
    button("Send", onclick=event("chat.add_message", message, group=dict(chatroom=chatroom)))

@action(event="chat.add_message")
def append_message(request, message):
    command("hypergen.append", "messages_id", message)

## Idea 3 ##

chat_consumer = HypergenConsumer(path="chatroom/<slug:name>")

@liveview()
def chatroom(request, name):
    for name in ChatRoom.objects.all().values_list("name", flat=True):
        with section():
            label("Write message in", name, ":")
            message = textarea(id_="message")
            button("Send", onclick=callback(chat_consumer.reverse(name=name), send_message, message))
            label("Messages:")
            div(id_=f"messages_{name}_id")

@action(consumer=chat_consumer)
def send_message(request, name, message):
    command("hypergen.append", f"messages_{name}_id", message)

## Idea 4 ##

chat_consumer = HypergenConsumer(path="chatroom/<slug:name>")

@liveview()
def chatroom(request, name):
    for name in ChatRoom.objects.all().values_list("name", flat=True):
        with section():
            label("Write message in", name, ":")
            message = textarea(id_="message")
            button("Send", onclick=callback(send_message.reverse(name=name), message))
            label("Messages:")
            div(id_=f"messages_{name}_id")

@action(consumer=chat_consumer)
def send_message(request, name, message):
    command("hypergen.append", f"messages_{name}_id", message)

# Idea 5

class MyConsumer(HypergenConsumer):
    @action(perm="foo.bar")
    def send_message(self, message):
        command("hypergen.append", f"messages_{self.group_name()}_id", message)

@liveview()
def template():
    button("Send", onclick=callback(send_message.reverse(name=name)))

# Idea 6
@liveview(listeners=[
    "user_logins", "user_logouts", "rooms_latest_message", lambda: f"room/{get_current_chatroom_id}/messages"])
def my_liveview(request):
    pass
    # template goes here.

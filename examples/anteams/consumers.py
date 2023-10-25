# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

if False:

    def group_add(consumer, group_name):
        print("group_add: ", group_name)
        async_to_sync(consumer.channel_layer.group_add)(group_name, consumer.channel_name)

    def group_discard(consumer, group_name):
        async_to_sync(consumer.channel_layer.group_discard)(group_name, consumer.channel_name)

    def group_send(consumer, group_name, data):
        async_to_sync(consumer.channel_layer.group_send)(group_name, data)

    (message_added, message_edited, message_deleted, message_read, file_added, user_joined, user_left,
        chatroom_deleted) = [None] * 8

    def message_added(user_id, message):
        return {
            "data": {"user_id", "message"},}

    class Group:
        pass

    class ChatroomGroup(Group):
        permission = "chat.app"
        events = {
            message_added, message_edited, message_deleted, message_read, file_added, user_joined, user_left,
            chatroom_deleted}

        def __init__(self, group_id):
            self.group_id = group_id

        def name(self):
            return f"anteams__ChatroomGroup__group_id.{self.group_id}"

        def access_check(self, consumer):
            return ChatRoom.objects.filter(pk=self.group_id, users__contains=consumer.scope.user.pk).exists()

    class MessageAddedEventForm(Form):
        txt = forms.CharField(min_length=3, max_length=2000)

    @event(allow_frontend=True, validate=MessageAddedEventForm)
    def message_added(user_id, txt):
        return {"txt": txt}

    @group(
        permission="chat.app",
        access_check=lambda consumer: ChatRoom.objects.filter(pk=group_id, users__contains=consumer.scope.user.pk),
        events={
        message_added, message_edited, message_deleted, message_read, file_added, user_joined, user_left,
        chatroom_deleted})
    def chatroom_group(group_id):
        return f"anteams__chatroom_group__group_id.{group_id}"

    def chatroom_group(group_id):
        # assert user.has_perm("chat.access_app") and ChatRoom.objects.filter(pk=group_id, users__contains=user.pk)
        # return f"anteams__chatroom_group__group_id.{group_id}"

        return {
            "name":
                f"anteams__chatroom_group__group_id.{group_id}",
            "permission":
                "chat.app",
            "access_check":
            lambda consumer: ChatRoom.objects.filter(pk=group_id, users__contains=consumer.scope.user.pk),
            "events": {
            message_added,
            message_edited,
            message_deleted,
            message_read,
            file_added,
            user_joined,
            user_left,
            chatroom_deleted,},}

    # group_send(chatroom_group(92), message_added(user_id=19, txt="This is good!"))

    class MyFancyConsumer(HypergenFancyConsumer):
        class Meta:
            events = [
                "message_added", "message_edited", "message_deleted", "message_read", "file_added", "user_joined",
                "user_left", "chatroom_deleted"]

class AnteamsConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'AnteamsConsumer'
        group_add(self, self.group_name)
        super(AnteamsConsumer, self).connect()

    def receive(self, text_data):
        # print()
        event = json.loads(text_data)
        if event["type"] == "group_add":
            group_add(self, event["group_name"])
        if event["type"] == "group_send":
            group_send(self, event["group_name"], event)
        # self.send(text_data=json.dumps({"type": "anteams_message", "message": "Got it!"}))
        # group_send(self, self.group_name, {"type": "anteams_group", "message": "I got group"})
        pass

    def anteams_group(self, event):
        print("_________________________-", repr(event))
        self.send(text_data=json.dumps(event))
        return {"foo": "bar"}

    def group_send(self, event):
        self.send(text_data=json.dumps(event))

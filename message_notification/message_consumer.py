from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from accounts.models import User
from cache.message import MessageCache


class MessageConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            'message', self.channel_name)

        author = User.objects.get(id=2)
        target = User.objects.get(id=9)
        message_cache = MessageCache(author, target)
        messages_list = message_cache.get_messages_list()

        self.send_json({'messages': messages_list})

    def disconnect(self, close_node):
        pass

    def reload_messages(self, event):
        # a.k.a: reload.messages
        print('got into reload_messages.')
        self.send_json({
            'message': event['message'],
        })
        print('passed through the whole thing, end of story.')

import channels

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from accounts.models import User
from cache.message import MessageCache
from rest_framework.authtoken.models import Token


class MessageConsumer(JsonWebsocketConsumer):
    def get_messages(self):
        messages = {}
        token_query = self.scope['query_string'].decode().split('=')[1]
        token = Token.objects.get(key=token_query)
        user = token.user
        friends = user.get_friends()['friends']

        for friend in friends:
            messages_cache = MessageCache(user, friend)
            friend_chat = messages_cache.get_messages_list()
            messages[f'{friend.username}'] = friend_chat

        return messages

    def connect(self):
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            'message', self.channel_name)

        messages = self.get_messages()
        self.send_json({'messages': messages})

    def disconnect(self, close_node):
        pass

    def reload_messages(self, event):
        # a.k.a: reload.messages
        self.send_json({
            'message': event['message'],
        })

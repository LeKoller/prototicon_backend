from django.core.cache import cache
import json


class MessageCache():
    def __init__(self, author, target):
        self.key = f'author,target:{author},{target}:messages'
        messages_list = cache.get(self.key)

        if messages_list == 'null' or messages_list == None:
            empty_array = json.dumps([])
            cache.set(self.key, empty_array, timeout=None)

            self.messages_list = []
        else:
            self.messages_list = json.loads(messages_list)

    def set_messages_list(self, messages_list):
        json_messages_list = json.dumps(messages_list)
        cache.set(self.key, json_messages_list, timeout=None)

    def get_messages_list(self):
        return self.messages_list

    def clear(self):
        self.messages_list = []
        empty_array = json.dumps([])
        cache.set(self.key, empty_array, timeout=None)

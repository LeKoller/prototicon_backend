from django.core.cache import cache
import json


class ContentCache():
    def __init__(self, user):
        self.key = f'user:{user}:contents'
        contents_list = cache.get(self.key)

        if contents_list == 'null' or contents_list == None:
            empty_array = json.dumps([])
            cache.set(self.key, empty_array, timeout=None)

            self.contents_list = []
        else:
            self.contents_list = json.loads(contents_list)

    def set_contents_list(self, contents_list):
        json_contents_list = json.dumps(contents_list)
        cache.set(self.key, json_contents_list, timeout=None)

    def get_contents_list(self):
        return self.contents_list

    def clear(self):
        self.product_list = []
        empty_array = json.dumps([])
        cache.set(self.key, empty_array, timeout=None)

    def add_content(self, content):
        contents_list = self.contents_list.append(content)
        json_contents_list = json.dumps(contents_list)
        cache.set(self.key, json_contents_list, timeout=None)

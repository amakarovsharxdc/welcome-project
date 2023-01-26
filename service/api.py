import re

from .models import Item
from .models import Items
from .storage import Storage


class VerbAlreadyExists(Exception):
    pass


class API:
    def __init__(self, storage: Storage):
        self.storage = storage

    def add_item(self, item: Item):
        _, *keys, key = re.sub(r'/\{[^/]*|/api/v1', '', item.path).split('/')
        tree = self.storage.tree
        for i in keys:
            tree = tree.setdefault(i, {})
        match isinstance(tree, dict) and tree.get(key):
            case None:
                tree[key] = item.verb
            case item.verb:
                pass
            case _:
                raise VerbAlreadyExists(item.path)

    def add_items(self, items: Items):
        for item in items:
            self.add_item(item)

    def get_tree(self):
        return self.storage.tree

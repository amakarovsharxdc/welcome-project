from .models import ItemsTree


class Storage:
    def __init__(self):
        self.tree: ItemsTree = {}

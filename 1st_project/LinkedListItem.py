from Composition import Composition

class LinkedListItem:
    def __init__(self, data: Composition):
        self.data = data
        self._next_item = None
        self._previous_item = None

    @property
    def next_item(self):
        return self._next_item

    @next_item.setter
    def next_item(self, item):
        self._next_item = item

    @property
    def previous_item(self):
        return self._previous_item

    @previous_item.setter
    def previous_item(self, item):
        self._previous_item = item

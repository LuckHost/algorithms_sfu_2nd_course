"""Doubly Linked Ring List"""

from typing import Self


class Node:
    """Node class."""

    def __init__(self, data=None):
        self.data = data
        self._next = None
        self._prev = None

    @property
    def next(self) -> Self:
        """Next property."""
        return self._next

    @next.setter
    def next(self, value: Self) -> None:
        if value:
            value._prev = self

        self._next = value

    @property
    def prev(self) -> Self:
        """Previous property."""
        return self._prev

    @prev.setter
    def prev(self, value: Self) -> None:
        if value:
            value._next = self

        self._prev = value

    def __repr__(self):
        return f"Linked List Node, data: {self.data}"


class DoublyLinkedList:
    """Doubly Linked List"""

    def __init__(self, first_node: Node):
        self.first_node = first_node

    @property
    def last(self) -> Node:
        """Get last Node."""
        if len(self) == 0:
            return None

        return self.first_node.prev

    def append_left(self, item):
        """Append from left."""
        if len(self) == 0:
            self.first_node = Node(item)
            self.first_node.next = self.first_node
            self.first_node.prev = self.first_node
            return

        new_item = Node(item)
        new_item.prev = self.first_node.prev
        new_item.next = self.first_node
        self.first_node = new_item

    def append_right(self, item):
        """Append from right."""
        if len(self) == 0:
            self.first_node = Node(item)
            self.first_node.next = self.first_node
            self.first_node.prev = self.first_node
            return

        new_item = Node(item)
        self.first_node.prev.next = new_item
        self.first_node.prev = new_item

    def append(self, item):
        """Append from right."""
        return self.append_right(item)

    def remove(self, item):
        """Remove by data."""
        if item not in self:
            raise ValueError("Item not found")

        cur = self.first_node
        while True:
            if cur.data == item:
                if len(self) == 1:
                    self.first_node = None
                    return

                cur.next.prev = cur.prev
                cur.prev.next = cur.next
                if cur == self.first_node:
                    self.first_node = cur.next
                break
            cur = cur.next

    def insert(self, previous_data, item):
        """Append from right."""
        new = Node(item)
        cur = self.first_node
        for _ in range(0, len(self)):
            if cur.data == previous_data:
                new.next = cur.next
                new.prev = cur
                cur.next = new
                return
            cur = cur.next
        raise ValueError(f"Item {previous_data} not found in the list")

    def __len__(self):
        if not self.first_node:
            return 0

        cnt = 0
        cur = self.first_node
        while True:
            cnt += 1
            cur = cur.next
            if cur == self.first_node:
                break

        return cnt

    def __next__(self):
        if self._cnt >= len(self):
            raise StopIteration

        self._cnt += 1
        cur_item = self._cur
        self._cur = self._cur.next

        return cur_item

    def __iter__(self):
        self._cur = self.first_node
        self._cnt = 0

        return self

    def __getitem__(self, index):
        if index < 0:
            index = len(self) + index
        if index < 0 or index >= len(self):
            raise IndexError("Linked List index out of range")
        cur = self.first_node
        for _ in range(0, index):
            cur = cur.next

        return cur.data

    def __contains__(self, item):
        if not self.first_node:
            return False

        cur = self.first_node
        while True:
            if cur.data == item:
                return True
            cur = cur.next
            if cur == self.first_node:
                return False

    def __reversed__(self):
        if len(self) == 0:
            return []

        reversed_list = []
        last_node = self.last
        cur = last_node
        while True:
            reversed_list.append(cur.data)
            if cur == self.first_node:
                break

            cur = cur.prev

        return reversed_list

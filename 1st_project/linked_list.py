"""Linked Ring List"""

from linked_list_item import LinkedListItem

class LinkedList:
    """Class representing a circular doubly linked list."""

    def __init__(self, first_node: LinkedListItem):
        """Initializes the doubly linked list with the first item.
        
        Args:
            first_node (LinkedListItem): The first item in the list.
        """
        self.first_node = first_node

    @property
    def last(self) -> LinkedListItem:
        """Gets the last item in the list.
        
        Returns:
            LinkedListItem: The last item in the list.
        """
        if len(self) == 0:
            return None
        return self.first_node.prev

    def append(self, item):
        """Appends an item to the right of the list.
        
        This method is a shortcut for `append_right(item)`.
        
        Args:
            item: The data to be stored in the new item.
        """
        return self.append_right(item)

    def append_left(self, item):
        """Appends an item to the left (beginning) of the list.
        
        Args:
            item: The data to be stored in the new item.
        """
        if len(self) == 0:
            # If the list is empty, the first item points to itself
            self.first_node = LinkedListItem(item)
            self.first_node.next = self.first_node
            self.first_node.prev = self.first_node
            return

        # Create a new item and link it to the left of the current first item
        new_item = LinkedListItem(item)
        new_item.prev = self.first_node.prev
        new_item.next = self.first_node
        self.first_node = new_item

    def append_right(self, item):
        """Appends an item to the right (end) of the list.
        
        Args:
            item: The data to be stored in the new item.
        """
        if len(self) == 0:
            # If the list is empty, the first item points to itself
            self.first_node = LinkedListItem(item)
            self.first_node.next = self.first_node
            self.first_node.prev = self.first_node
            return

        # Create a new item and link it to the right of the last item
        new_item = LinkedListItem(item)
        self.first_node.prev.next = new_item
        self.first_node.prev = new_item

    def remove(self, item):
        """Removes an item by its data from the list.
        
        Args:
            item: The data to be removed from the list.
        
        Raises:
            ValueError: If the item is not found in the list.
        """
        if item not in self:
            raise ValueError("Item not found")

        cur = self.first_node
        while True:
            if cur.data == item:
                if len(self) == 1:
                    # If there's only one item, the list becomes empty
                    self.first_node = None
                    return

                # Remove the item by linking its previous and next items
                cur.next.prev = cur.prev
                cur.prev.next = cur.next
                if cur == self.first_node:
                    self.first_node = cur.next
                break
            cur = cur.next

    def insert(self, previous_data, item):
        """Inserts a new item after the item with the specified data.
        
        Args:
            previous_data: The data of the item after which to insert the new item.
            item: The data to be stored in the new item.
        
        Raises:
            ValueError: If the item with `previous_data` is not found.
        """
        new = LinkedListItem(item)
        cur = self.first_node
        for _ in range(len(self)):
            if cur.data == previous_data:
                # Insert the new item after the current one
                new.next = cur.next
                new.prev = cur
                cur.next = new
                return
            cur = cur.next
        raise ValueError(f"Item {previous_data} not found in the list")

    def __len__(self):
        """Returns the number of items in the list.
        
        Returns:
            int: The length of the list.
        """
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
        """Returns the next item during iteration.
        
        Returns:
            LinkedListItem: The next item in the iteration.
        
        Raises:
            StopIteration: If there are no more items.
        """
        if self._cnt >= len(self):
            raise StopIteration

        self._cnt += 1
        cur_item = self._cur
        self._cur = self._cur.next
        return cur_item

    def __iter__(self):
        """Initializes the iterator and returns itself.
        
        Returns:
            DoublyLinkedList: The list itself for iteration.
        """
        self._cur = self.first_node
        self._cnt = 0
        return self

    def __getitem__(self, index):
        """Gets the item by its index.
        
        Args:
            index (int): The index of the item to retrieve.
        
        Returns:
            data: The data stored in the item at the specified index.
        
        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0:
            index = len(self) + index
        if index < 0 or index >= len(self):
            raise IndexError("Linked List index out of range")
        cur = self.first_node
        for _ in range(index):
            cur = cur.next
        return cur.data

    def __contains__(self, item):
        """Checks if the list contains the specified item by data.
        
        Args:
            item: The data to check for in the list.
        
        Returns:
            bool: True if the item is in the list, False otherwise.
        """
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
        """Returns the reversed list as a list of data.
        
        Returns:
            list: A list containing the data in reverse order.
        """
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

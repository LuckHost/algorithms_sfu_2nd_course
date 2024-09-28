from typing import Self

class LinkedListItem:
    """Class representing an item in a doubly linked list."""

    def __init__(self, data=None):
        """Initializes a LinkedListItem with optional data.
        
        Args:
            data: The value or object to store in the item. 
            Can be of any data type.
        """
        self.data = data
        self._next = None
        self._prev = None

    @property
    def next(self) -> Self:
        """Gets the next item in the list.
        
        Returns:
            LinkedListItem: The next item in the linked list.
        """
        return self._next

    @next.setter
    def next(self, value: Self) -> None:
        """Sets the next item in the list and adjusts the 
        previous pointer of the next item.
        
        Args:
            value (LinkedListItem): The item to be set as the next item.
        """
        if value:
            value._prev = self
        self._next = value

    @property
    def prev(self) -> Self:
        """Gets the previous item in the list.
        
        Returns:
            LinkedListItem: The previous item in the linked list.
        """
        return self._prev

    @prev.setter
    def prev(self, value: Self) -> None:
        """Sets the previous item in the list and adjusts the next 
        pointer of the previous item.
        
        Args:
            value (LinkedListItem): The item to be set as the previous item.
        """
        if value:
            value._next = self
        self._prev = value

    def __repr__(self):
        """Returns a string representation of the item.
        
        Returns:
            str: A string showing the item's data.
        """
        return f"Linked List Item, data: {self.data}"

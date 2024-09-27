from Composition import Composition
from LinkedListItem import LinkedListItem

class LinkedList:
    def __init__(self):
        self.first_item = None
        self.last_item = None  # Добавляем ссылку на последний элемент
        self.length = 0

    def __len__(self):
        return self.length

    def append_left(self, item: Composition):
        new_item = LinkedListItem(item)
        if self.first_item is None:
            # Если список пустой, новый элемент становится первым и последним
            self.first_item = new_item
            self.last_item = new_item
        else:
            # Добавляем элемент слева
            new_item.next_item = self.first_item
            self.first_item.previous_item = new_item
            self.first_item = new_item
        self.length += 1

    def append_right(self, item: Composition):
        new_item = LinkedListItem(item)
        if self.first_item is None:
            # Если список пустой, новый элемент становится первым и последним
            self.first_item = new_item
            self.last_item = new_item
        else:
            # Добавляем элемент справа
            self.last_item.next_item = new_item
            new_item.previous_item = self.last_item
            self.last_item = new_item  # Обновляем последний элемент
        self.length += 1

    append = append_right

    def remove(self, item: Composition):
        if self.first_item is None:
            raise ValueError("Список пуст")
        
        current = self.first_item
        while current is not None:
            if current.data == item:
                # Удаление элемента
                if current == self.first_item:
                    self.first_item = current.next_item
                    if self.first_item is not None:
                        self.first_item.previous_item = None
                elif current == self.last_item:
                    self.last_item = current.previous_item
                    if self.last_item is not None:
                        self.last_item.next_item = None
                else:
                    current.previous_item.next_item = current.next_item
                    current.next_item.previous_item = current.previous_item
                self.length -= 1
                return
            current = current.next_item

        raise ValueError(f"{item} не найден в списке")

    def __iter__(self):
        self._current = self.first_item
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        current = self._current
        self._current = self._current.next_item
        return current

    def __getitem__(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Индекс вне диапазона")
        current = self.first_item
        for _ in range(index):
            current = current.next_item
        return current

    def __contains__(self, item: Composition):
        current = self.first_item
        while current is not None:
            if current.data == item:
                return True
            current = current.next_item
        return False

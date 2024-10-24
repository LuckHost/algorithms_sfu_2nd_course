from typing import Callable, Optional, List

# Вспомогательная функция для обмена элементов
def swap(array: List, i: int, j: int):
    array[i], array[j] = array[j], array[i]

# Реализация шейкерной сортировки (Shaker sort)
def shaker_sort(array: List, reverse: bool = False) -> List:
    n = len(array)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        # Проход слева направо
        for i in range(start, end):
            if (array[i] > array[i + 1]) if not reverse else (array[i] < array[i + 1]):
                swap(array, i, i + 1)
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        # Проход справа налево
        for i in range(end - 1, start - 1, -1):
            if (array[i] > array[i + 1]) if not reverse else (array[i] < array[i + 1]):
                swap(array, i, i + 1)
                swapped = True
        start += 1
    return array

def insertion_sort(array: List[int], left: int, right: int, reverse: bool) -> None:
    """Сортировка вставками с учётом направления."""
    for i in range(left + 1, right + 1):
        key = array[i]
        j = i - 1
        while j >= left and ((key < array[j] and not reverse) or (key > array[j] and reverse)):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key

# Слияние двух отсортированных подмассивов
def merge(left_part: List[int], right_part: List[int], reverse: bool = False) -> List[int]:
    if reverse:
        left_part, right_part = left_part[::-1], right_part[::-1]

    merged = []
    i = j = 0
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            merged.append(left_part[i])
            i += 1
        else:
            merged.append(right_part[j])
            j += 1

    merged.extend(left_part[i:])
    merged.extend(right_part[j:])
    
    if reverse:
        merged = merged[::-1]
    return merged

# Основная функция Timsort
def tim_sort(array: List[int], run_size: int = 32, reverse: bool = False) -> List[int]:
    n = len(array)

    # Сортируем каждый подмассив вставками
    for i in range(0, n, run_size):
        insertion_sort(array, i, min(i + run_size - 1, n - 1), reverse)

    # Объединяем отсортированные подмассивы
    size = run_size
    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(start + size - 1, n - 1)
            end = min((start + 2 * size - 1), n - 1)
            if mid < end:
                merged_array = merge(array[start:mid + 1], array[mid + 1:end + 1], reverse)
                array[start:start + len(merged_array)] = merged_array
        size *= 2

    return array

# Сортировка слиянием
def merge_sort(array: List, reverse: bool = False) -> List:
    if len(array) > 1:
        mid = len(array) // 2
        left = merge_sort(array[:mid], reverse)
        right = merge_sort(array[mid:], reverse)
        return merge(left, right, reverse)
    else:
        return array

def merge(left: List, right: List, reverse: bool) -> List:
    result = []
    while left and right:
        if (left[0] <= right[0]) if not reverse else (left[0] > right[0]):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result

# Быстрая сортировка (Quick Sort)
def quick_sort(array: List, reverse: bool = False) -> List:
    if len(array) <= 1:
        return array
    pivot = array[len(array) // 2]
    left = [x for x in array if (x < pivot) if not reverse]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if (x > pivot) if not reverse]
    return quick_sort(left, reverse) + middle + quick_sort(right, reverse)

# Функция для выбора и выполнения алгоритма сортировки
def my_sort(array: List, reverse: bool = False,
            key: Optional[Callable] = None, cmp: Optional[Callable] = None, algorithm: str = 'timsort') -> List:
    # Если передан ключ, применяем его ко всем элементам
    if key:
        array = [key(x) for x in array]

    # Выбор алгоритма сортировки
    if algorithm == 'timsort':
        return tim_sort(array, 32, reverse)
    elif algorithm == 'mergesort':
        return merge_sort(array, reverse)
    elif algorithm == 'quicksort':
        return quick_sort(array, reverse)
    elif algorithm == 'shaker':
        return shaker_sort(array, reverse)
    else:
        raise ValueError(f"Неизвестный алгоритм сортировки: {algorithm}")

# Пример использования:
if __name__ == '__main__':
    sample_array = [2, -3, 5, 0, 5]
    sorted_array = my_sort(sample_array, reverse=False, algorithm='quicksort')
    print("Отсортированный массив:", sorted_array)

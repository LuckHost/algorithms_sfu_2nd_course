# merge_sort_visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def merge_sort(array, reverse=False):
    """Функция сортировки слиянием, которая записывает состояния массива на каждом шаге."""
    states = []
    _merge_sort_recursive(array, 0, len(array) - 1, reverse, states)
    return states

def _merge_sort_recursive(array, left, right, reverse, states):
    if left < right:
        mid = (left + right) // 2
        _merge_sort_recursive(array, left, mid, reverse, states)
        _merge_sort_recursive(array, mid + 1, right, reverse, states)
        merge(array, left, mid, right, reverse, states)

def merge(array, left, mid, right, reverse, states):
    left_part = array[left:mid + 1]
    right_part = array[mid + 1:right + 1]

    if reverse:
        left_part.sort(reverse=True)
        right_part.sort(reverse=True)
    else:
        left_part.sort()
        right_part.sort()

    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if (left_part[i] < right_part[j]) if not reverse else (left_part[i] > right_part[j]):
            array[k] = left_part[i]
            i += 1
        else:
            array[k] = right_part[j]
            j += 1
        k += 1
        states.append(array.copy())

    while i < len(left_part):
        array[k] = left_part[i]
        i += 1
        k += 1
        states.append(array.copy())

    while j < len(right_part):
        array[k] = right_part[j]
        j += 1
        k += 1
        states.append(array.copy())

def visualize_merge_sort(array, reverse=False):
    # Получаем состояния для анимации
    states = merge_sort(array, reverse)

    # Настройка графика
    fig, ax = plt.subplots()
    ax.set_title("Визуализация Сортировки Слиянием")
    bar_rects = ax.bar(range(len(array)), array, align="edge")

    # Обновление столбцов на графике на каждом кадре
    def update(frame):
        for rect, val in zip(bar_rects, states[frame]):
            rect.set_height(val)

    # Анимация
    anim = animation.FuncAnimation(fig, update, frames=range(len(states)), repeat=False)
    plt.show()

# Пример использования
if __name__ == "__main__":
    sample_array = [random.randint(-10, 10) for _ in range(20)]
    visualize_merge_sort(sample_array)

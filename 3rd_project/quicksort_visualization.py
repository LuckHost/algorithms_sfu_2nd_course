# quicksort_visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def quick_sort(array, reverse=False):
    """Функция быстрой сортировки, которая также записывает состояние массива на каждом шаге."""
    states = []  # для записи состояния массива
    _quick_sort_recursive(array, 0, len(array) - 1, reverse, states)
    return states

def _quick_sort_recursive(array, low, high, reverse, states):
    if low < high:
        pivot_index = partition(array, low, high, reverse, states)
        _quick_sort_recursive(array, low, pivot_index - 1, reverse, states)
        _quick_sort_recursive(array, pivot_index + 1, high, reverse, states)

def partition(array, low, high, reverse, states):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if (array[j] < pivot) if not reverse else (array[j] > pivot):
            i += 1
            array[i], array[j] = array[j], array[i]
            states.append(array.copy())  # сохраняем текущее состояние массива
    array[i + 1], array[high] = array[high], array[i + 1]
    states.append(array.copy())  # сохраняем текущее состояние массива
    return i + 1

def visualize_quick_sort(array, reverse=False):
    # Генерируем состояния для анимации
    states = quick_sort(array, reverse)

    # Настройка графика
    fig, ax = plt.subplots()
    ax.set_title("Визуализация Быстрой Сортировки")
    bar_rects = ax.bar(range(len(array)), array, align="edge")

    # Обновление столбцов графика на каждом кадре
    def update(frame):
        for rect, val in zip(bar_rects, states[frame]):
            rect.set_height(val)

    # Анимация
    anim = animation.FuncAnimation(fig, update, frames=range(len(states)), repeat=False)
    plt.show()

# Пример использования
if __name__ == "__main__":
    sample_array = [2, -3, 5, 0, 5, 4, 311, 53, 134, 53, 55]
    visualize_quick_sort(sample_array)

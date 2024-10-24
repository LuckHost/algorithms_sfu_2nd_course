import argparse
import os
import csv
import pathlib
import threading
import heapq
from typing import Union, Optional, Callable, List
import tempfile
from pathlib import Path


PathType = Union[str, pathlib.Path]

def try_convert(value: str, type_data: str):
    """Преобразование строки в нужный тип данных."""
    if type_data == 'i':
        return int(value)
    elif type_data == 'f':
        return float(value)
    return value  # Для строковых данных

def natural_merge_sort(src: PathType, output: Optional[PathType] = None, 
                       reverse: bool = False,
                       key: Optional[Callable] = None, nflows: int = 1, bsize: Optional[int] = None, type_data: str = 's') -> None:
    """Естественное слияние"""
    key = key or (lambda x: x)

    # Разбиение файла на серии
    def split_into_runs(input_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            current_run = []
            prev_value = None
            for line in file:
                value = try_convert(line.strip(), type_data)
                if prev_value is not None and (value < prev_value if not reverse else value > prev_value):
                    # Завершаем текущую серию
                    yield current_run
                    current_run = []
                current_run.append(value)
                prev_value = value
            if current_run:
                yield current_run

    # Слияние серий
    def merge_runs(runs: List[List], reverse: bool):
        heap = [(key(run[0]), i, 0) for i, run in enumerate(runs) if run]
        heapq.heapify(heap)
        result = []
        while heap:
            value, run_idx, pos = heapq.heappop(heap)
            result.append(runs[run_idx][pos])
            if pos + 1 < len(runs[run_idx]):
                heapq.heappush(heap, (key(runs[run_idx][pos + 1]), run_idx, pos + 1))
        return result if not reverse else result[::-1]

    # Запись данных
    def write_sorted_data(output_file, sorted_data):
        with open(output_file, 'w', encoding='utf-8') as file:
            for item in sorted_data:
                file.write(str(item) + '\n')

    # Разбиение на серии и слияние
    runs = list(split_into_runs(src))
    sorted_data = merge_runs(runs, reverse)

    output_file = output or src
    write_sorted_data(output_file, sorted_data)


# Реализация других алгоритмов, например, N-путевое слияние, каскадное слияние и т.д.


def handle_csv_file(src: PathType, output: PathType, key: str, reverse: bool, type_data: str, 
                    nflows: int, bsize: int):
    """Обработка CSV файла"""
    with open(src, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        rows.sort(key=lambda x: try_convert(x[key], type_data), reverse=reverse)
    
    with open(output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def mixed_type_key(value, type_data: str):
    """
    Возвращает ключ для сортировки с учётом типа данных.
    Поддерживаются строки, числа и вещественные числа.
    """
    try:
        if type_data == 'i':  # Целые числа
            return int(value)
        elif type_data == 'f':  # Вещественные числа
            return float(value)
    except ValueError:
        # Если не удается преобразовать к числу, вернем строковое значение
        return value
    return value

def my_sort(src: List[PathType], output: Optional[PathType] = None, reverse: bool = False,
            key: Optional[Union[Callable, str]] = None, nflows: int = 1, bsize: Optional[int] = None, type_data: str = 's') -> None:
    """
    Основная функция сортировки с поддержкой нескольких файлов и разных типов данных.
    """
    if isinstance(src, (str, Path)):
        src = [src]  # Преобразуем в список, если строка

    # Обработка CSV-файлов отдельно
    if src[0].endswith('.csv') and isinstance(key, str):
        handle_csv_file(src[0], output or src[0], key, reverse, type_data, nflows, bsize)
        return

    # Определение ключа сортировки на основе типа данных
    if key is None or key == "":
        if type_data == 'i':  # Сортировка целых чисел
            key = lambda x: int(x.strip())  # Преобразование строки в целое число
        elif type_data == 'f':  # Сортировка чисел с плавающей точкой
            key = lambda x: float(x.strip())  # Преобразование строки в float
        else:
            key = lambda x: x.strip()  # Для строк

    all_lines = []  # Собираем все строки из всех файлов

    for file_path in src:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        all_lines.extend(lines)  # Добавляем строки в общий список

    # Сортировка всех строк сразу с использованием ключа и направления сортировки
    all_sorted_lines = sorted(all_lines, reverse=reverse, key=key)

    # Запись отсортированных данных в выходной файл или исходный файл
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.writelines(all_sorted_lines)
    else:
        for file_path in src:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(all_sorted_lines)

def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='External sorting utility')
    parser.add_argument('src', type=str, help='Input file (txt or csv)')
    parser.add_argument('-o', '--output', type=str, help='Output file', default=None)
    parser.add_argument('-r', '--reverse', action='store_true', help='Sort in descending order')
    parser.add_argument('-k', '--key', type=str, help='Sorting key for CSV files (column name)')
    parser.add_argument('-n', '--nflows', type=int, default=1, help='Number of threads')
    parser.add_argument('-b', '--bsize', type=int, default=1024, help='Block size (bytes)')
    parser.add_argument('-t', '--type', type=str, choices=['s', 'i', 'f'], default='s',
                        help='Type of data: s - string, i - integer, f - float')
    return parser.parse_args()


def main():
    """Запуск программы с командной строки"""
    args = parse_args()
    my_sort(src=args.src, output=args.output, reverse=args.reverse, key=args.key, nflows=args.nflows, bsize=args.bsize, type_data=args.type)


if __name__ == '__main__':
    main()

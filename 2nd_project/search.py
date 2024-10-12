import argparse
import time
from typing import Union, Optional, Tuple, Dict, List
from algorithms import *


avalible_algoritms = ['kmp', 'bm','rk', 'bmh']

# Декоратор для логирования времени выполнения
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Функция поиска
@log_time
def search(string: str, sub_strings: Union[str, List[str]],
           case_sensitivity: bool = False, method: str = 'first',
           count: Optional[int] = None, algorithm: str = 'kmp') -> Optional[Union[Tuple[int, ...], Dict[str, Tuple[int, ...]]]]:
    if algorithm not in avalible_algoritms:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    
    # Приведение строки и подстрок к нижнему регистру, если чувствительность отключена
    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_strings, str):
            sub_strings = [sub_strings.lower()]
        else:
            sub_strings = [sub.lower() for sub in sub_strings]
    
    # Если передана одна подстрока, приводим ее в список
    if isinstance(sub_strings, str):
        sub_strings = [sub_strings]

    is_all_none = True
    result = {}

    for sub_string in sub_strings:
        if method == 'first':
            match algorithm:
                case 'kmp':
                    indices = kmp_search(string, sub_string)
                case 'bm':
                    indices = boyer_moore_search(string, sub_string)
                case 'rk':
                    indices = rabin_karp_search(string, sub_string)
                case 'bmh':
                    indices = boyer_moore_horspool_search(string, sub_string)
            if indices == None:
                result[sub_string] = None
                continue
            is_all_none = False
        elif method == 'last':
            match algorithm:
                case 'kmp':
                    indices = kmp_search(string[::-1], sub_string[::-1])
                case 'bm':
                    indices = boyer_moore_search(string[::-1], sub_string[::-1])
                case 'rk':
                    indices = rabin_karp_search(string[::-1], sub_string[::-1])
                case 'bmh':
                    indices = boyer_moore_horspool_search(string[::-1], sub_string[::-1])
            if indices == None:
                result[sub_string] = None 
                continue
            is_all_none = False
            indices = tuple(len(string) - i - len(sub_string) for i in indices)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if count:
            if indices != None:
                indices = indices[:count]
        
        if indices:
            result[sub_string] = indices

    if is_all_none:
        return None
    elif len(sub_strings) == 1:

        return next(iter(result.values()))

    return result if result else None

# Функция для чтения файла
def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

# Парсер аргументов командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Substring search utility.")
    parser.add_argument('--string', type=str, help="String to search in.")
    parser.add_argument('--file', type=str, help="Path to the file to search in.")
    parser.add_argument('--substring', type=str, nargs='+', required=True, help="Substring(s) to search for.")
    parser.add_argument('--case-sensitive', action='store_true', help="Enable case-sensitive search.")
    parser.add_argument('--method', type=str, choices=['first', 'last'], default='first', help="Search method: 'first' (default) or 'last'.")
    parser.add_argument('--count', type=int, help="Find the first k occurrences.")
    parser.add_argument('--algorithm', type=str, default='kmp', help=f"Algorithm to use. One of {avalible_algoritms}")
    
    return parser.parse_args()

# Основная логика выполнения
if __name__ == "__main__":
    args = parse_args()

    # Чтение строки либо из аргумента, либо из файла
    if args.file:
        string = read_file(args.file)
    elif args.string:
        string = args.string
    else:
        raise ValueError("Either --string or --file must be provided.")

    # Выполнение поиска
    result = search(string, args.substring, case_sensitivity=args.case_sensitive,
                    method=args.method, count=args.count, algorithm=args.algorithm)
    
    # Вывод результата
    if result:
        print("Found occurrences:")
        for sub, indices in result.items():
            print(f"Substring '{sub}' found at positions: {indices}")
    else:
        print("No occurrences found.")

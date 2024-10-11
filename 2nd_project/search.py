import argparse
import time
from typing import Union, Optional, Tuple, Dict, List


# Декоратор для логирования времени выполнения
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Алгоритм Кнута-Морриса-Пратта
def kmp_search(string: str, substring: str):
    string_len, substring_len = len(string), len(substring)
    lps = [0] * substring_len
    j = 0  # Индекс для substring[]
    
    # Препроцессинг паттерна для вычисления lps[]
    compute_lps_array(substring, substring_len, lps)

    indices = []
    i = 0  # Индекс для string[]
    while i < string_len:
        if substring[j] == string[i]:
            i += 1
            j += 1
        
        if j == substring_len:
            indices.append(i - j)
            j = lps[j - 1]
        elif i < string_len and substring[j] != string[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    if len(indices) == 0:
        return None
    return tuple(indices)

def compute_lps_array(substring: str, m: int, lps: List[int]):
    length = 0  # длина предыдущей самой длинной префиксной суффиксной подстроки
    lps[0] = 0  # lps[0] всегда 0
    i = 1
    
    while i < m:
        if substring[i] == substring[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

# Функция поиска
@log_time
def search(string: str, sub_strings: Union[str, List[str]],
           case_sensitivity: bool = False, method: str = 'first',
           count: Optional[int] = None) -> Optional[Union[Tuple[int, ...], Dict[str, Tuple[int, ...]]]]:
    
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
            indices = kmp_search(string, sub_string)
            if indices == None:
                result[sub_string] = None
                continue
            is_all_none = False
        elif method == 'last':
            indices = kmp_search(string[::-1], sub_string[::-1])
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
                    method=args.method, count=args.count)
    
    # Вывод результата
    if result:
        print("Found occurrences:")
        for sub, indices in result.items():
            print(f"Substring '{sub}' found at positions: {indices}")
    else:
        print("No occurrences found.")

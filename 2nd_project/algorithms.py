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

def compute_lps_array(substring: str, m: int, lps: list[int]):
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

def boyer_moore_search(text: str, pattern: str) -> tuple[int, ...]:
    m, n = len(pattern), len(text)
    if m == 0 or n == 0:
        return tuple()

    # Таблица "плохих символов"
    bad_char_table = [-1] * 256
    for i in range(m):
        bad_char_table[ord(pattern[i])] = i

    indices = []
    shift = 0

    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        
        if j < 0:
            indices.append(shift)
            shift += (m - bad_char_table[ord(text[shift + m])] if shift + m < n else 1)
        else:
            shift += max(1, j - bad_char_table[ord(text[shift + j])])

    return tuple(indices)

def rabin_karp_search(text: str, pattern: str, prime: int = 101) -> tuple[int, ...]:
    m, n = len(pattern), len(text)
    if m > n:
        return tuple()

    base = 256
    h_pattern = 0  # хеш паттерна
    h_text = 0     # хеш текущего окна в тексте
    h = 1  # base^(m-1)

    for i in range(m - 1):
        h = (h * base) % prime

    # вычисляем начальный хеш для паттерна и первого окна текста
    for i in range(m):
        h_pattern = (base * h_pattern + ord(pattern[i])) % prime
        h_text = (base * h_text + ord(text[i])) % prime

    indices = []

    for i in range(n - m + 1):
        if h_pattern == h_text:
            if text[i:i + m] == pattern:
                indices.append(i)

        if i < n - m:
            h_text = (base * (h_text - ord(text[i]) * h) + ord(text[i + m])) % prime
            if h_text < 0:
                h_text += prime

    return tuple(indices)

def boyer_moore_horspool_search(text: str, pattern: str) -> tuple[int, ...]:
    m, n = len(pattern), len(text)
    if m > n:
        return tuple()

    # Таблица сдвигов
    bad_char_shift = {char: m for char in set(text)}
    for i in range(m - 1):
        bad_char_shift[pattern[i]] = m - i - 1

    indices = []
    shift = 0

    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            indices.append(shift)
            shift += bad_char_shift.get(text[shift + m], m) if shift + m < n else 1
        else:
            shift += bad_char_shift.get(text[shift + j], m)

    return tuple(indices)

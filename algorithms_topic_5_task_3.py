import timeit

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Testing

# KMP
print('тестування статті1 методом кмп')
text_from_article1 = load_text('article1.txt')

pattern1 = "алг"
print('пошук реального паттерна')
time_pattern1 = timeit.timeit(lambda: kmp_search(text_from_article1, pattern1), number=100)
print(time_pattern1)
print(kmp_search(text_from_article1, pattern1))

pattern2 = "blabla"
print('пошук нереального паттерна')
time_pattern2 = timeit.timeit(lambda: kmp_search(text_from_article1, pattern2), number=100)
print(time_pattern2)
print(kmp_search(text_from_article1, pattern2))

print('тестування статті2 методом кмп')
text_from_article2 = load_text('article2.txt')

pattern3 = "Відповідно"
print('пошук реального паттерна')
time_pattern3 = timeit.timeit(lambda: kmp_search(text_from_article2, pattern3), number=100)
print(time_pattern3)
print(kmp_search(text_from_article2, pattern3))

pattern4 = "blabla"
print('пошук нереального паттерна')
time_pattern4 = timeit.timeit(lambda: kmp_search(text_from_article2, pattern4), number=100)
print(time_pattern4)
print(kmp_search(text_from_article2, pattern4))

# Boyer Moore
print('тестування статті1 методом BM')

print('пошук реального паттерна')
time_pattern1 = timeit.timeit(lambda: boyer_moore_search(text_from_article1, pattern1), number=100)
print(time_pattern1)
print(boyer_moore_search(text_from_article1, pattern1))

print('пошук нереального паттерна')
time_pattern2 = timeit.timeit(lambda: boyer_moore_search(text_from_article1, pattern2), number=100)
print(time_pattern2)
print(boyer_moore_search(text_from_article1, pattern2))

print('тестування статті2 методом BM')

print('пошук реального паттерна')
time_pattern3 = timeit.timeit(lambda: boyer_moore_search(text_from_article2, pattern3), number=100)
print(time_pattern3)
print(boyer_moore_search(text_from_article2, pattern3))

print('пошук нереального паттерна')
time_pattern4 = timeit.timeit(lambda: boyer_moore_search(text_from_article2, pattern4), number=100)
print(time_pattern4)
print(boyer_moore_search(text_from_article2, pattern4))

# Rabin Karp
print('тестування статті1 методом RK')

print('пошук реального паттерна')
time_pattern1 = timeit.timeit(lambda: rabin_karp_search(text_from_article1, pattern1), number=100)
print(time_pattern1)
print(rabin_karp_search(text_from_article1, pattern1))

print('пошук нереального паттерна')
time_pattern2 = timeit.timeit(lambda: rabin_karp_search(text_from_article1, pattern2), number=100)
print(time_pattern2)
print(rabin_karp_search(text_from_article1, pattern2))

print('тестування статті2 методом RK')

print('пошук реального паттерна')
time_pattern3 = timeit.timeit(lambda: rabin_karp_search(text_from_article2, pattern3), number=100)
print(time_pattern3)
print(rabin_karp_search(text_from_article2, pattern3))

print('пошук нереального паттерна')
time_pattern4 = timeit.timeit(lambda: rabin_karp_search(text_from_article2, pattern4), number=100)
print(time_pattern4)
print(rabin_karp_search(text_from_article2, pattern4))

# Data
data = [
    ["Стаття", "Алгоритм", "Пошук реального паттерна (сек)", "Пошук нереального паттерна (сек)"],
    ["1", "KMP", "0.0021", "0.0816"],
    ["1", "Boyer-Moore", "0.0014", "0.0420"],
    ["1", "Rabin-Karp", "0.0035", "0.2202"],
    ["2", "KMP", "0.0074", "0.1114"],
    ["2", "Boyer-Moore", "0.0030", "0.0607"],
    ["2", "Rabin-Karp", "0.0188", "0.3302"],
]

# Generate Markdown table
markdown_table = " | ".join(data[0]) + "\n" + \
                 " | ".join(["---"] * len(data[0])) + "\n" + \
                 "\n".join(" | ".join(map(str, row)) for row in data[1:])

# Print Markdown table
print(markdown_table)

## Висновки

#Зроблено висновки щодо швидкостей алгоритмів для кожного тексту окремо та в цілому. 

1. **Для Статті 1:**
   - Найшвидшим алгоритмом для пошуку реального патерна є Boyer-Moore з часом виконання 0.0014 секунди.
   - Найшвидшим алгоритмом для пошуку нереального патерна також є Boyer-Moore з часом виконання 0.0420 секунди.

2. **Для Статті 2:**
   - Найшвидшим алгоритмом для пошуку реального патерна є Boyer-Moore з часом виконання 0.0030 секунди.
   - Найшвидшим алгоритмом для пошуку нереального патерна також є Boyer-Moore з часом виконання 0.0607 секунди.

3. **В цілому:**
   - Алгоритм Boyer-Moore показав найкращі результати як для Статті 1, так і для Статті 2, з часом виконання 0.0014 секунди 
   для реального патерна та 0.0420 секунди для нереального патерна.
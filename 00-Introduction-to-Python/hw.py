# -*- coding: utf-8 -*-

"""
Реализуйте метод, определяющий, является ли одна строка 
перестановкой другой. Под перестановкой понимаем любое 
изменение порядка символов. Регистр учитывается, пробелы 
являются существенными.
"""
from collections import defaultdict, Counter

# С использованием встроенного словаря
def is_permutation(a: str, b: str) -> bool:
    letter_counter = {}
    if len(a) == len(b):
        for letter in a:
            if letter in letter_counter:
                letter_counter[letter] += 1
            else:
                letter_counter[letter] = 1
        for letter in b:
            if letter in letter_counter:
                letter_counter[letter] -= 1
            else:
                return False
        return not any(letter_counter.values())
    else:
        return False

# С использование модуля collections.Counter
def is_permutation_2(a: str, b: str) -> bool:
    if len(a) == len(b):
        letter_counter = Counter(a)
        letter_counter.subtract(Counter(b))
        return not any(letter_counter.values())
    else:
        return False

# С использование модуля collections.defaultdict
def is_permutation_3(a: str, b: str) -> bool:
    letter_counter = defaultdict(int)
    if len(a) == len(b):
        for letter in a:
            letter_counter[letter] += 1
        for letter in b:
            letter_counter[letter] -= 1
        return not any(letter_counter.values())
    else:
        return False


print(is_permutation('baba', 'abab'))
print(is_permutation('abbba', 'abab'))
print(is_permutation('baba', 'abbb'))
print("---")
print(is_permutation_2('baba', 'abab'))
print(is_permutation_2('abbba', 'abab'))
print(is_permutation_2('baba', 'abbb'))
print("---")
print(is_permutation_3('baba', 'abab'))
print(is_permutation_3('abbba', 'abab'))
print(is_permutation_3('baba', 'abbb'))
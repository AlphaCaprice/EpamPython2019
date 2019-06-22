"""
Реализовать дескриптор, кодирующий слова с помощью шифра Цезаря

"""

from string import ascii_lowercase


class ShiftDescriptor:
    letters = list(ascii_lowercase)
    alphabet = {letter: i for i, letter in enumerate(letters)}

    def __init__(self, key):
        self.key = key
        self.text = ""

    def __get__(self, instance, owner):
        return self.text

    def __set__(self, instance, value):
        self.text = self.__get_cipher(value)

    def __get_cipher(self, text: str):
        out_str = []
        len_al = len(self.alphabet)
        for i in text:
            index = (self.alphabet[i] + self.key) % len_al
            out_str.append(self.letters[index])
        return "".join(out_str)


class CaesarCipher:
    message = ShiftDescriptor(4)
    another_message = ShiftDescriptor(7)
    out_message = ShiftDescriptor(3)


a = CaesarCipher()
a.message = 'abc'
a.another_message = 'hello'
a.out_message = "xyz"

assert a.message == 'efg'
print(a.message)
assert a.another_message == 'olssv'
print(a.another_message)
assert a.out_message == 'abc'
print(a.out_message)

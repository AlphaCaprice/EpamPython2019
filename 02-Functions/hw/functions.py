def letters_range(*args, **kwargs):
    """ Возвращает список букв в указанном диапазоне c указанным шагом
        Например: letters_range('b', 'l', 2) -> ['b', 'd', 'f', 'h', 'j']
        letters_range('c') -> ['a', 'b'] """

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
    len_args = len(args)
    try:
        assert (len_args in range(1, 4))
        if kwargs:
            for i, letter in enumerate(alphabet):
                if letter in kwargs:
                    alphabet[i] = str(kwargs.get(letter))
        if len_args == 1:
            start, stop, step = alphabet[0], args[0], 1
        elif len_args == 2:
            start, stop, step = args[0], args[1], 1
        else:
            start, stop, step = args
        return alphabet[alphabet.index(start):alphabet.index(stop):step]

    except AssertionError:
        print("Wrong amount of arguments")
    except ValueError as e:
        print(f"{e}. Letters must be Latin lowercase")
    except TypeError as e:
        print(f"{e}. First and second args must be lowercase Latin letters,"
              "third - integer")


print(letters_range('b', 'l', 2))
print(letters_range('g'))
print(letters_range('g', 'p'))
print(letters_range('g', 'p', **{'l': 7, 'o': 0}))
print(letters_range('7', 'p', **{'l': 7, 'o': 0, 'e': 3}))
print(letters_range('p', 'g', -2))
print(letters_range('a'))


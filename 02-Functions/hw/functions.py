import inspect
from collections import namedtuple


def letters_range(*args, **kwargs) -> list:
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
              "third must be integer")


def test_letter_range():
    test_data = [('b', 'l', 2), ('g',), ('g', 'p'), ('p', 'g', -2), ('a',)]
    for test in test_data:
        print(letters_range(*test))

    print(letters_range('g', 'p', **{'l': 7, 'o': 0}))
    print(letters_range('7', 'p', **{'l': 7, 'o': 0, 'e': 3}))


def atom(*args):
    if not len(args) in range(2):
        raise TypeError("Expect one or zero arguments!")
    __value = None if not args else args[0]
    Functions = namedtuple("Functions", ['get_value', 'set_value',
                                         'process_value', 'delete_value'])

    def __get_value():
        try:
            return __value
        except NameError:
            return "Error! Value does not exist!"

    def __set_value(v: int):
        nonlocal __value
        __value = v

    def __process_value(*args):
        nonlocal __value
        for function in args:
            __value = function(__value)
        return __value

    def __delete_value():
        nonlocal __value
        del __value

    return Functions(__get_value, __set_value, __process_value, __delete_value)


def test_atom():
    x = atom()
    x.set_value(4)
    x.process_value(lambda k: k**2, lambda k: k-10)
    print(x.get_value())
    x.delete_value()
    print(x.get_value())
    x.set_value(22)
    print(x.get_value())


def make_it_count(func, counter_name: str):
    globals()[counter_name] += 1
    return func


def test_make_it_count():
    res = 5
    res = make_it_count(lambda x: x**2, "glob_x")(res)
    print(res)
    res = make_it_count(lambda x: x-20, "glob_x")(res)
    print(res)


def modified_func(func, *fixated_args, **fixated_kwargs):
    def nested_func(*args, **kwargs):
        doc_str = f"""
        A func implementation of nested_func
        with pre-applied arguments being:
        :param args: {inspect.getargvalues(inspect.currentframe())[3]['fixated_args']}
        :param kwargs: {inspect.getargvalues(inspect.currentframe())[3]['fixated_kwargs']}
        :source_code: {inspect.getsource(nested_func)}
        """
        nested_func.__name__ = "func_nested_func"
        nested_func.__doc__ = doc_str
        new_args = (*fixated_args, *args)
        new_kwargs = {**fixated_kwargs, **kwargs}
        return func(*new_args, **new_kwargs)
    return nested_func


def print_args(*args, **kwargs):
    print(args, "\n", kwargs)


def test_modified_func():
    new_fun = modified_func(print_args, 2, "var", [9, 8, 7, 6], one=1, two=2)
    new_fun(10, "more var", three=3, one=111)
    new_fun()
    print(new_fun.__doc__)
    print(new_fun.__name__)


if __name__ == "__main__":
    test_letter_range()
    print()
    test_atom()
    print()
    glob_x = 0
    test_make_it_count()
    print(glob_x)
    print()
    test_modified_func()


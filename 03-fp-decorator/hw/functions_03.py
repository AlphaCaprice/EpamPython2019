import functools
import random
import time
from functools import reduce, update_wrapper



def sum_square_difference(n: int)->int:
    return sum([x for x in range(1, n+1)])**2 - sum([x**2 for x in range(1, n+1)])


def special_pythagorean_triplet(n: int)->int:
    return [x*y*z for x in range(1, n//2) for y in range(x, n//2) for z in range(y, n//2)
            if x+y+z == n and x**2+y**2 == z**2][0]


def self_powers(n: int)->list:
    return list(str(sum([x**x for x in range(1, n+1)]))[-10:])


def champernownes_constant(n)->int:
    indexes = set(10**i for i in range(7)) # надеюсь это не считается за доп.строку
    return reduce(lambda a, s: int(a) * int(s),
                  [x for i, x in enumerate("".join([str(i) for i in range(n+1)])) if i in indexes])


def is_armstrong(number: int)->bool:
    return sum(map(lambda x: int(x)**len(str(number)), list(str(number)))) == number


def collatz_steps(n: int, counter=0)->int:
    return collatz_steps(n//2, counter=counter+1) if n % 2 == 0 else \
        collatz_steps(3*n+1, counter=counter+1) if n != 1 else counter


def make_cache(t: int):
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items())) if kwargs else args
            if key in cache:
                return cache[key][0]

            cache[key] = (func(*args, **kwargs), time.time())
            for key in cache.copy():
                if time.time()-cache[key][1] >= t:
                    cache.pop(key)
            print(cache)
            return cache[key]
        return wrapper
    return decorator


@make_cache(10)
def slow_function_1(k, *args, **kwargs):
    for i in range(100_000_000):
        ...
    return k


@make_cache(10)
def slow_function_2(k,  *args, **kwargs):
    for i in range(100_000_000):
        ...
    return k

if __name__ == "__main__":
    # print(sum_square_difference(100))
    # print(special_pythagorean_triplet(1_000))
    # print(self_powers(1_000))
    # print(champernownes_constant(1_000_000))
    # print(is_armstrong(153))
    # print(is_armstrong(10))
    # print(collatz_steps(16) == 4)
    # print(collatz_steps(12) == 9)
    # print(collatz_steps(1_000_000) == 152)
    for i in range(1, 6):
        print(slow_function_1(i*100, **{str(i): i**2}))
        # print(slow_function_2(i*400, **{str(i): i**2}))

    for i in range(5, 0, -1):
        print(slow_function_1(i*100, **{str(i): i**2}))
        # print(slow_function_2(i*400, **{str(i): i**2}))
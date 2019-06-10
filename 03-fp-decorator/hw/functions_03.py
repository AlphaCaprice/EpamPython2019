import functools
import random
from functools import reduce, update_wrapper
from threading import Timer


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


def make_cache(t: int, cache=[]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache.append(func(*args, **kwargs))
            Timer(t, cache.pop, [0]).start()
            print(cache)
            return cache[-1]
        return wrapper

    return decorator


@make_cache(5)
def slow_function():
    for i in range(100_000_000):
        ...
    return random.randint(1, 1000)

if __name__ == "__main__":
    print(sum_square_difference(100))
    print(special_pythagorean_triplet(1_000))
    print(self_powers(1_000))
    print(champernownes_constant(1_000_000))
    print(is_armstrong(153))
    print(is_armstrong(10))
    print(collatz_steps(16) == 4)
    print(collatz_steps(12) == 9)
    print(collatz_steps(1_000_000) == 152)
    for i in range(8):
        print(slow_function())

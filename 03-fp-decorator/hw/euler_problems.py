from functools import reduce

def sum_square_difference(n: int)->int:
    return sum([x for x in range(1, n+1)])**2 - sum([x**2 for x in range(1, n+1)])


def special_pythagorean_triplet(n: int)->int:
    return [x*y*z for x in range(1, n//2) for y in range(x, n//2) for z in range(y, n//2)
            if x+y+z == n and x**2+y**2 == z**2][0]


def self_powers(n: int)->list:
    return list(str(sum([x**x for x in range(1, n+1)]))[-10:])


def champernownes_constant(n)->int:
    indexes = set(10**i for i in range(7))
    return reduce(lambda a, s: int(a) * int(s),
                  [x for i, x in enumerate("".join([str(i) for i in range(n+1)])) if i in indexes])

if __name__ == "__main__":
    print(sum_square_difference(100))
    print(special_pythagorean_triplet(1_000))
    print(self_powers(1_000))
    print(champernownes_constant(1_000_000))

import random
from typing import List

import sympy

from numx._exceptions import NumXError


def return_same(number: int) -> int:
    return number


def calc_nth_prime(number: int) -> int:
    if number == 0:
        raise NumXError("The prime number index must be positive")
    return sympy.prime(number)


def random_number(number: int) -> int:
    return random.randint(0, number)


def py_nth_point(number: int) -> sympy.Float:
    return sympy.N(sympy.pi, number + 1)


def e_nth_point(number: int) -> sympy.Float:
    return sympy.N(sympy.E, number + 1)


def first_n_primes(number: int) -> List[int]:
    if number == 0:
        return []
    return primes_upto_n(calc_nth_prime(number))


def num_of_primes_upto(number: int) -> int:
    return int(sympy.primepi(number))


def primes_upto_n(number: int) -> List[int]:
    return list(sympy.sieve.primerange(number + 1))


def euler_totient(number: int) -> int:
    if number == 0:
        raise NumXError("The totient number must be positive")
    return int(sympy.totient(number))


def factorial(number: int) -> int:
    return int(sympy.factorial(number))


def fibonacci(number: int) -> int:
    return int(sympy.fibonacci(number))

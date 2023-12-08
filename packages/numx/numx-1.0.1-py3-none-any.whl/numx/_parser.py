import re
from typing import Tuple, Optional

from numx._actual_math import calc_nth_prime, return_same, random_number, py_nth_point, e_nth_point, first_n_primes, \
    num_of_primes_upto, primes_upto_n, euler_totient, factorial, fibonacci
from numx._exceptions import NumXError


FUNCTION_BY_PREFIX = {
    'p': calc_nth_prime,
    'pl': first_n_primes,
    'P': num_of_primes_upto,
    'PL': primes_upto_n,
    'n': return_same,
    'r': random_number,
    'pi': py_nth_point,
    'e': e_nth_point,
    't': euler_totient,
    'fa': factorial,
    'fi': fibonacci,
}


PREFIX_REGEX = "|".join(sorted(FUNCTION_BY_PREFIX.keys(), key=lambda x: -len(x)))

SIMPLE_INT = r'\d+'
SIMPLE_FLOAT = r'(?:\d*_)?\d+'
POWER_INT = rf'({SIMPLE_FLOAT})([ep])({SIMPLE_FLOAT})'
NUMBER_REGEX = rf'(?:{POWER_INT})|(?:{SIMPLE_INT})'

VARIABLE_NAME_REGEX = rf'({PREFIX_REGEX})({NUMBER_REGEX})'


def match_until_end(pattern: str, value: str, error_str: str, exact_size: Optional[int] = None) -> Tuple:
    match = re.match(fr"{pattern}$", value)
    if not match:
        raise NumXError(error_str)

    groups = match.groups()
    if not exact_size:
        return groups

    if len(groups) < exact_size:
        raise NumXError(error_str)
    return groups[:exact_size]


def parse_number(number_string: str) -> int:
    number_string = number_string.replace('_', '.')

    if 'e' in number_string:
        mul_num, exp = [float(num) for num in number_string.split('e')]
        return round(mul_num * 10**exp)

    if 'p' in number_string:
        base, exp = [float(num) for num in number_string.split('p')]
        return round(base ** exp)

    return int(number_string)


def parse_type_value(request: str) -> Tuple[str, int]:
    type_str, value_str = match_until_end(VARIABLE_NAME_REGEX, request,
                                          f"This variable name doesn't match any rule: {request}", 2)
    value = parse_number(value_str)
    return type_str, value


def raise_missing_if_magic_function(request: str) -> None:
    if re.match('(__.*__$)|(_ipython.*_$)', request):
        raise AttributeError()

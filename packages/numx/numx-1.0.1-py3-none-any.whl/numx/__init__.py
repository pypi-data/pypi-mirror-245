"""
With this package you can import numbers. For example:
from numx import p25   # == 97, the 25th prime
from numx import n300  # == 300

# Supported Number Types
- `pN`  - the Nth prime.
- `plN` - list of the first N primes.
- `PN`  - count the primes upto N.
- `PLN` - list of primes upto N.
- `nN`  - the number N.
- `rN`  - random integer in range [0, N].
- `piN` - pi to N decimal places (as numx.__Float).
- `eN`  - e to N decimal places (as numx.__Float).
- `tN`  - Euler's totient function of N.
- `faN` - N! (N factorial).
- `fiN` - fibonacci(N), starting from fi0 == 0.

Moreover, for big numbers you can use:
- `2e7` to denote `2 * 10**7`
- `2p7` to denote `2 ** 7`
- `_` as a dot, so: `6_25p_5` is `6.25 ** 0.5`

An import can fail only when importing a variable written in a bad format (e.g. numx.n7e will fail).
When it fails, numx will raise the numx.__NumXError exception, which inherits from ValueError.

numx.__Float is sympy.Float, which supports the str() and float() functions.
"""

from numx._numx_main import _calculate_number
from numx._exceptions import NumXError as __NumXError
from sympy import Float as __Float


def __getattr__(request: str):
    return _calculate_number(request)

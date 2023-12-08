# NumX - Import Numbers

[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/tomhea/numx)](https://github.com/tomhea/numx)
[![GitHub](https://img.shields.io/github/license/tomhea/numx)](LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/numx)](https://pypi.org/project/numx/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/numx)](https://pypi.org/project/numx/)

Just Import Numbers.

```python
>> from numx import p25  # The 25th prime
>> print(p25)
97
```

This library allows importing useful numbers, as the Nth prime, prime lists, random numbers, fibonacci, e, pi, ...  
The library is [thoroughly tested](#how-to-test), and uses [sympy](https://pypi.org/project/sympy/) as its computational mind.

### How to Download
```
pip install numx
```

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

### How to Test

The library is thoroughly tested. If you want to run the test, just run:
```
>> git clone https://github.com/tomhea/numx.git
>> pytest numx
```

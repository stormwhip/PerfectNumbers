"""Independent exact-integer checks for the newly added 61^10/61^12 LP cuts."""
from math import prod
from sympy import isprime

cases = {
    2: {3: 1, 13: 1, 97: 1},
    4: {5: 1, 131: 1, 21491: 1},
    6: {52379047267: 1},
    8: {3: 2, 13: 1, 19: 1, 97: 1, 903870199: 1},
    10: {199: 1, 859: 1, 4242586390571: 1},
    12: {187123: 1, 14421466756460791: 1},
}
for exponent, factorization in cases.items():
    sigma = (61 ** (exponent + 1) - 1) // 60
    assert prod(p ** k for p, k in factorization.items()) == sigma, exponent
    for p in factorization:
        assert p < 2 ** 64 and isprime(p), (exponent, p)
    print(f"SIGMA_61 exponent={exponent} verified_factors={factorization}", flush=True)
for odd_exponent in range(1, 256, 2):
    assert sum(pow(61, i, 31) for i in range(odd_exponent + 1)) % 31 == 0
assert 61 % 31 == 30
assert ((61 ** 15 - 1) // 60) % 3 == 0
print("PRIME61_FACTORS_OK all stated factorizations, exact products and primality verified", flush=True)

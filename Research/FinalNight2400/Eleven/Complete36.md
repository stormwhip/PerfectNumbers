# (11,462), first pivot 36 completely excluded

Combine the [initial 26-pair reduction](ThirtySix.md) and [forced U^6 reduction](ForceSix36.md) with this final [U^6 verifier](Complete36.py) and [12 actual split witnesses](Last36Six.json). All apply to the canonical family with primes 7 and 19 absent. For U=93156840075306751 the only remaining sixth power is now excluded.

A second common prime 73360625933069303328648469781 divides sigma(879701^36); its square forces the 49-digit prime 2143347344722745987754685625589825340891246255381. Both are 1 mod4, so one must first check they cannot be the Euler prime of *any* exponent: the verifier applies the root-only mixed price to its exact Euler base with all non-root rows restored as atoms, as detailed in the [first f42 proof](FortyTwo.md). Only after this comparison does it branch on even exponents. Their primality and divisor identities are checked offline; GMP-ECM is discovery only. All other [common price, tail, and source lemmas](FortySix.md) apply unchanged. At the final 12 recursive nodes all 1,625 direct leaves close (273 banned, 171 simple, 428 mandatory, 725 raw, 28 supplier). No heuristic tree stopping is accepted.

Full scoped replay:

    python -I -S -B Research/FinalNight2400/Eleven/ThirtySix.py
    python -I -S -B Research/FinalNight2400/Eleven/ForceSix36.py
    python -I -S -B Research/FinalNight2400/Eleven/Complete36.py

This closes just first f=36, not the entire root key.

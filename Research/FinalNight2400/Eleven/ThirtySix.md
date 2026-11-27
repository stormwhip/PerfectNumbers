# (11,462), f=36: forced pair of component exponents

Use the common [19/5 price and supplier-split proof](FortySix.md) and [mandatory bound and cutoff addendum](FortyTwo.md), this time at f=36. The [standalone verifier](ThirtySix.py) checks that both U=93156840075306751 and R=183172571 are primes 3 mod4 dividing sigma(879701^36), hence mandatory ordinary components. The U factor was discovered with locally cached GMP-ECM and is certified by complete Lucas factorization of U−1; no external programs are used on replay. Strict raw size tail for U is 102. All allowed positive even exponents of U and R are exhausted; after a first finite pass and a second mandatory-prime pass the following explicit pairs remain open:

| U exponent | Possible R exponents |
|---:|---|
|4|2,4,8,10,12,14,16,18,22,24|
|6|2,4,8,10,12,14,16,18|
|10|2,4,8,10,12|
|12|2,4,8|

There are 26 pairs, not putative actual numbers. U exponents 16 and 30 survive the first pass but no R exponent is left. No other U exponent survives. First R size tails in the six relevant cases: 200,196,186,182,174,146. No f=36 exclusion is claimed here.

    python -I -S -B Research/FinalNight2400/Eleven/ThirtySix.py

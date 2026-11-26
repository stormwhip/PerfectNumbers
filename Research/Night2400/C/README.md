# Night2400 C — exact conditional fibers of (19,420)

Reproduce from the repository root using only the checked-in files and Python 3.11 standard library (do not use `-O`):

```text
python -I -S -B Research/Night2400/C/Verify.py
```

The claim is restricted to odd perfect integers `N <= 10**2400` with `19^420 || N`, for the outstanding actual of `P19_I00080`. Let `q = 28174642921954703272833689609691232580811241064837460583`. The checker certifies `q` with the included ECPP chain and checks `v_q(sigma(19^420)) = 1`. Because `q ≡ 3 (mod 4)`, its actual exponent is positive even. An exact integer budget scan gives raw even exponents 2–24, with 14–24 directly too large after including the odd parts of both known sigma factors, and every even exponent >= 26 too large already from the single-root lower bound. There remain six candidate exponents (2,4,6,8,10,12).

The [joint valuation checker](../../FinalSprint/JointValuation.py) excludes the two exact fibers `q^10 || N` and `q^12 || N`, using both fixed bases as incoming valuation targets and no banned primes. The receipts `(exceptions, [price-window, no-block, interior-check])` are `(17, [3490, 720, 0])` and `(17, [4985, 67, 0])`, respectively. The method accounts for a possible Euler exponent one separately. This does **not** cover the fibers 2,4,6,8, any entire root or shard, or any other actual exponent. In particular it implies no divisibility lift.

Discovery provenance: `Discover.Finder(Discover.Bank(<official data-v1 index>), 0).factors(19,420)` returned the singleton `[q]` (185 bits); PARI `primecert` supplied the witness only. Neither the index, PARI nor any shared discovery cache is used at replay.

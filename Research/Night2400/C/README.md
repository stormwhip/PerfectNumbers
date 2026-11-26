# Night2400 C — exact conditional fibers of (19,420)

Reproduce from the repository root using only the checked-in files and Python 3.11 standard library (do not use `-O`):

```text
python -I -S -B Research/Night2400/C/Verify.py
```

The claim is restricted to odd perfect integers `N <= 10**2400` with `19^420 || N`, for the outstanding actual of `P19_I00080`. Let `q = 28174642921954703272833689609691232580811241064837460583`. The checker certifies `q` with the included ECPP chain and checks `v_q(sigma(19^420)) = 1`. Because `q ≡ 3 (mod 4)`, its actual exponent is positive even. An exact integer budget scan gives raw even exponents 2–24, with 14–24 directly too large after including the odd parts of both known sigma factors, and every even exponent >= 26 too large already from the single-root lower bound. There remain six candidate exponents (2,4,6,8,10,12).

The [joint valuation checker](../../FinalSprint/JointValuation.py) excludes the following exact fibers, pricing both `19` and `q` as incoming valuation targets. It accounts for a possible Euler exponent one separately.

| Exact exponent of `q` | Fixed extension | Receipt `(exceptions, [price-window, no-block, interior-check])` |
| --- | --- | --- |
| 8 | `r^2 || N` as proved below | `(16, [2549, 819, 0])` |
| 10 | none | `(17, [3490, 720, 0])` |
| 12 | none | `(17, [4985, 67, 0])` |

At exponent 8 the two-component price runs into its exterior Euler test. Instead, certify the prime `r = 18716166489844799458885230781362655242022878296316554735036307387001821111739679109236269675618028263`. The checker validates that `r` divides the forced cofactor outside the exact components, and `r ≡ 3 (mod 4)` requires even exponent. For every even `f >= 4`, either the monotone prefix-only lower bound excludes `r^f`, or the checker explicitly computes the strengthened three-component forced size and finds it exceeds `10**2400`. Thus only exponent 2 is possible. Its complete sigma emission then enters the size and window computations even though `r` is not a valuation target. No anonymous cofactor is presumed prime or squarefree.

**Coverage:** this does not cover the fibers 2,4,6, any entire root or shard, or any other actual exponent. In particular it implies no divisibility lift. The same forced-square inference and two-target valuation code were also verified on the already covered exponent-12 pivot fiber of [Tree7x168](../../FinalSprint/Tree7x168.json.gz); replay this regression only with `python -I -S -B Research/Night2400/C/Verify.py --regression`. That example is not additional coverage.

Discovery provenance: `Discover.Finder(Discover.Bank(<official data-v1 index>), 0).factors(19,420)` returned the singleton `[q]` (185 bits); the same finder at `(q,8)` identified `r`. PARI `primecert` supplied witnesses only. Neither the index, PARI nor any shared discovery cache is used at replay.

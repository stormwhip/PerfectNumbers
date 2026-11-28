# Exact `(19,276),1176672733^f`: Euler placement at 1109 excluded for all five even first pivots

Let `T=1176672733`, `s=1109`, `X=19^276 T^f`, `Y=σ(19^276)σ(T^f)` and `D=Y/gcd(Y,X)`, with `f∈{2,8,16,18,28}`. Replay certifies the bases by trial division and verifies `v_s(Y)=v_s(D)=1`. If `s` carries Euler, its exponent `h≡1 mod 4` and all exterior sources are ordinary. The strict original size tail `X(D/s)s^h>B` and the exact raw-live count are recomputed for each `f`:

| `f` | Strict raw tail | All raw-live Euler rows excluded |
|---:|---:|---:|
| 2 | 549 | 69 |
| 8 | 514 | 64 |
| 16 | 466 | 58 |
| 18 | 454 | 57 |
| 28 | 394 | 50 |

Thus `1109` is ordinary in every one of the five even first-pivot cases. Even `1109` exponents themselves are outside this packet.

The two target prices have disjoint support. At 19 use weight 2 and all primitive Hensel roots, which are exhaustive within the price-positive regime `b^(o−1)<19^(2z)` because `o−1≥2` and therefore `b<19^z`. Any order-one component or LTE additional unit is paid by the effective length budget; `U19≤10^6` by exact arithmetic. For `s` the only positive odd-order possibility is 277, with unavailable LTE and order one excluded by `(2s+1)^(s−1)>B`. All supplier bases are `<50,000,000`; every odd representative at depth 4 already exceeds the cap. For each smaller depth `z`, every odd base in a root class satisfies `b^276≥s^(100z)` by monotonicity in its least positive odd representative. Thus the `s` weight is 100 with no loss.

An actual Euler component `s^h` contributes at most three additional units at 19: `ord19(s)=3`, `v19(s³−1)=1` and `h+1≤5031<19³`. Therefore all such fixed prefixes retain demand `c19≥276−v19(Y)−3`, and at `s` demand `h−1`. The disjoint effective lengths of the external components permit the exact joint bound

```text
N·10^6 ≥ X·s^h ·19^(2(276−v19(Y)−3)) ·s^(100(h−1)).
```

The right side is strictly larger than `B·10^6` at `h=9` for every supported `f`, and increases on the entire remaining exponent tail. If the same comparison at `h=5` is insufficient, the exact demand at 1109 is four. Reserve `276m` units for every supplier with index `277m`, as in [Proof276.md](Proof276.md), while still paying the 19 effective length. The exact bound then forces `∏b^m<63700`. Exhaustive prime/valuation checks on the actual base interval find no supplier with two units, and the four distinct minima `13,29,53,67` already have product exceeding 63700; this exhausts the low Euler window.

For the last `s^1`, `(1109+1)/2=555=3·5·37` forces three ordinary primes. Append their minimum abundance ratios at exponent 2 (not exact exponents). The resulting lower bound already forbids `7,11,13,17,23,29,31`: adding the ratio at exponent 2 for any one makes the product strictly exceed 2. Each of `3,5,37` would force one of those absent labels at either exponent 2 or exponent 4: at exponent 2 their respective witnesses may be `13,31,7`; at exponent 4 all three have 11 as a factor of the divisor sum. Hence all three have exponent at least 6. Monotonicity of the geometric ratios now gives strict total abundance greater than 2. The verifier uses rational comparisons throughout. This completes the Euler placement at `1109`, but does not close the first-pivot fiber (ordinary `1109` still open).

```sh
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Pricing/VerifyT28Euler.py --pivot 28
# Also supported: --pivot 2, --pivot 8, --pivot 16, --pivot 18
```

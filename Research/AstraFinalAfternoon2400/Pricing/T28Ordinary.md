# Open-Euler joint price for even first-pivot exponents

Conditional domain: `19^276,1176672733^f,1109^h` exact, where `f∈{2,8,16,18,28}` is an unresolved even first-pivot value, `h` is ordinary (even), and `N` is odd perfect and at most `10^2400`. [VerifyT28Ordinary.py](VerifyT28Ordinary.py) implements an exhaustive **sufficient** exclusion test, not a search making primal assumptions about surviving windows. No full first-pivot fiber is claimed here.

## Budget and Euler positions

Write `N=X·q^(4k+1)·∏b^a` for the exact prefix product `X`, unknown Euler prime `q`, and the other ordinary components. Euler's identity is

```text
σ(q^(4k+1)) = (q+1) σ((q²)^(2k)).
```

Treat the Euler square `q²` as an ordinary atom, distinct from all ordinary prime bases, reserving the outer `q` separately. Its ordinary exponent is `2k`; if `k=0` there is no supplying atom. Every supplying atom has odd length at most 5031. At 19 the unit price is 2, at `s=1109` it is 100, these effective-length supports are coprime, and their costs can be added within each atom as in the [fixed-Euler proof](Proof276.md). The actual bases may now be odd primes **or** the one odd square `q²`, so the 19 loss generator preserves every candidate odd square even when it has a Fermat compositeness witness. The 1109 zero-loss bound was over all odd integer bases and is still valid for the square. The first impossible Hensel depth solves coverage for all larger levels without enumerating lifts; priced positive deficits at 19 satisfy `b<19^z` so use the legitimate least-positive regime.

Let `c19,c1109` be the demands after exact fixed output and set `j=v19(q+1)`, `i=v1109(q+1)`. The window `(i,j)` is inside the full independent bounded ranges `0..c1109` and `0..c19`. For `m=19^j*1109^i`, `q≡2m−1 (mod 4m)` and `q≥q0=max(5,2m−1)`. Thus the necessary inequality is

```text
B * U19 ≥ X * q0 * 19^(2(c19−j)) * 1109^(100(c1109−i)).
```

This product does not charge the anonymous compulsory mass at all. As a separate test, put `Y=odd(∏σ(p^h))` and `M=XY/gcd(X,Y)`. If `q∤Y` then `M*q|N`, which can exclude the entire outer case if `M*q0>B`. When the outer case fails, any possible `q` must divide at least one raw sigma block `A`; the cofactor `J=A/q` obeys `1≤J≤A/q0` and `J≡A(2m−1)^(-1) mod 4m`. If no candidate residue in this range divides `A`, the internal case is also excluded. Very wide residue windows are conservatively left open. When `j>0`, the `19^276` block is excluded immediately by quadratic reciprocity: `q≡−1 mod19` and `q≡1 mod4` give `(19/q)=-1`, whereas `q|σ(19^276)` would require an odd order and therefore `(19/q)=+1`.

The prefix's raw domain is computed afresh: the 1109 valuation is forced at one, the raw tail is linked to the strict `X(D/1109)1109^h>B` comparison, and only exact raw-compatible `h` are considered. All five exact replays returned the following domains; each range uses step 2. The [separate Euler-at-1109 proof](T28Euler.md) excludes every compatible odd placement in each of these five parent cases.

| `f` | Ordinary raw-live | Excluded range, count | Remaining range, count | Strict raw tail |
|---:|---:|---:|---:|---:|
| 2 | 137 | 184–274 (46) | 2–182 (91) | 549 |
| 8 | 128 | 172–256 (43) | 2–170 (85) | 514 |
| 16 | 116 | 156–232 (39) | 2–154 (77) | 466 |
| 18 | 113 | 152–226 (38) | 2–150 (75) | 454 |
| 28 | 98 | 132–196 (33) | 2–130 (65) | 394 |

These are local `1109` children, not complete first-pivot fibers. In particular other proofs not using this pivot may overlap them.

```sh
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Pricing/VerifyT28Ordinary.py --pivot 28
```

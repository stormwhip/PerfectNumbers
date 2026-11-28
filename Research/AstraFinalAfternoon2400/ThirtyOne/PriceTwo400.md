# Anonymous first 400 at canonical (31,2): exact source-price proof

Condition on the exact prefix `31^2`, `331^400`, with `19,7,11` forbidden. This eliminates one complete first fiber of the 143-entry `331` domain, **not** the whole `(31,2)` key. The only additional book-keeping needed when combining is set difference against previous packets (first 400 was open). No unknown cofactor is called a prime.

Set `t=331`, `X=31²t^400`, `A=σ(t^400)`, `D=3A`. Recompute `σ(31²)=3t`, `gcd(A,3)=1`, `v_t(S)=1` and `v_31(S)=0` with `S=σ(31²)A`. Thus `XD|N`, and 3 must occur with even exponent ≥2 because its prime is not 1 mod 4. The code certifies `ℓ=401`, `t≠1 mod ℓ`, and for every prime divisor z of A, `ord_z(t)=ℓ` (the case z=ℓ would require `t≡1 mod ℓ`), so `z≡1 mod 2ℓ`. [High2Refine.py](High2Refine.py) checks every such integer ≤10^8, and certifies A composite with Fermat base 2 and nonsquare by integer square root. The numerical coverage does not assume factorization.

## Price of ordinary and Euler-square atoms

Write the unfixed Euler component `q^(4k+1)=q(q²)^(2k)`, with sigma `(q+1)σ((q²)^(2k))`. Let the ordinary primes and possible square atom have odd lengths L. They are all distinct; the bare q is paid separately. For a nontrivial odd order o of y modulo t, `o|t−1=2·3·5·11`, `o|L`, and LTE gives `v_t(σ(y^(L−1)))=z+u` with `z=v_t(y^o−1)`, `u=v_t(L)`. Since `t^u|L/o`, the exponent cost can reserve `o−1` for base contributions and `t^u−1 ≥ u(t−1)` for the LTE increment, with their sum ≤`L−1`; `3^(t−1)≥t²` pays all LTE target units. For order one the same LTE payment pays the entire valuation; base y=t supplies none. This argument explicitly covers `L≥331`, not just lengths below t.

Any positive price-loss ratio at base depth z imposes `y^(o−1)<t^(2z)`. Since `o−1≥2`, only `y<t^z` can lose. [PricedTwo.py](PricedTwo.py) reconstructs *all* primitive order-o residues in that interval by digit Hensel lifting, from the complete prime-field search through every `z≤399`. A least-only table at larger weights would not inherit this bound. Eligible y are ordinary prime or admissible Euler-square q²; only fixed/forbidden bases, even values, definite composite witnesses or sizes incompatible with `X·lcm(D,y^(o−1))≤B` are rejected. A distinct base is counted once per maximum loss across all eligible depths; conservative upward rounding establishes one small deficit and universal multiplier `U` for any subset. No L or Euler position is fixed by this price: `cost·U ≥ (mass of t supply)²`.

## All Euler positions, exponents and allocations

Take `i=v_31(q+1)∈{0,1,2}`, `j=v_t(q+1)∈[0,399]`, `m=31^i t^j`, and `Q=max(5,2m−1)`. Actual `q≡2m−1 mod 4m`. Set `R=t^(2(399−j))`; `XQR≤BU` is necessary from all ordinary/square atoms and the bare q. This does not require any assumption about where q lies.

If q is internal to A and `j>0`, reciprocity contradicts its odd order of t because `q≡1 mod4`, `t≡3 mod4` and `q≡−1 mod t`. For `j=0`, internal candidates satisfy also `q≡1 mod ℓ`. [AnonymousEuler.py](AnonymousEuler.py) derives the unique CRT classes of q and the cofactor A/q. Both exceed 10^8 as A is composite and certified rough. If that interval contains no compatible factor, or its unique cofactor does not divide A, internal q is impossible. Otherwise [PricedTwo.py](PricedTwo.py) retains the necessary `9X·max(A,q^α)≤B`; the `max` avoids double counting q already in A.

For q external, A's nonsquare shape forces an additional (ordinary) factor >10^8; `9XA(limit+1)Q^α≤B`. There is a distinct ordinary source r of q, since q divides no fixed sigma, nor its own. It can be r=3; the independent source inequality uses **only** `Xq^α` alongside the r component, not an extra factor 9 which would then overlap. If its residual t supply mass is Y, the r component has size `>2QY/3` and `gcd(D,r^h)≤H=max(3,A)` by coprimality of these two blocks. From size with D, `2XDQ^(α+1)Y<3BH`. Price the other atoms separately, counting bare q and r once: `2XQ²R<3BUY`. Combining yields `4X²D Q^(α+3) R < 9B²UH`, with no duplicate r charge. All tests use integer inequalities preserving equality as an allowed relaxation. Every α is `1 mod4`; the necessary tests are monotone increasing in α, so testing exactly `α=1` and the minimum `α=5` for the class `α≥5` covers all possibilities.

The verifier tests the full `3×400×2=2400` mesh, rejecting all cells in both classes. Condition (31,2), first 400 is therefore impossible under frozen canonical scope. Isolated command:

```powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/ThirtyOne/Certificate2First400.py
```

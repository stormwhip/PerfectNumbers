# Uniform anonymous Euler cap and same-source cancellation

Let `X` be an exact even prefix. Write `D` for the odd forced cofactor after stripping fixed primes. If `N` is odd perfect, its special prime `q≡1 (mod 4)` lies outside `X`. For alpha `=4k+1`, use the exact splitting

```text
σ(q^alpha)=(q+1) σ((q²)^(2k)).
```

The atom `q²` is treated with the ordinary atom price. It is distinct from all ordinary prime-base atoms; the remaining factor of `N` at `q` is one `q`. For each fixed price target `p_i`, let `j_i=v_{p_i}(q+1)` and `m=∏p_i^j_i`. Because `q≡1 (mod4)`, `q=2m−1 (mod4m)` and `m≤q`, even when `m=1`. For a common price `w=A/C>1`, let `V=X^C(∏p_i^c_i)^A/U` be the priced bound before charging the linear Euler contribution, with complete powered deficit `U`. Then

```text
N^C ≥ V q^C / m^A ≥ V / q^(A−C).
```

This turns many apparently unresolved individual allocation cells into one integer comparison. If `q` divides an odd fixed-output block, bound it by the largest block after removing fixed primes; otherwise `q≤B/(XD)` or its improvement after adding proven ordinary reserve. If the bigger branch-independent cap is `Q`, it suffices to show `V>B^C Q^(A−C)`.

## Same-source extension for external Euler

Suppose `q∤D`, so some *other* ordinary atom `b^f` emits at least one `q` by perfection (`q` never emits itself; no fixed output has it). Let `W=∏p_i^u_i` be the target supply of that same atom. Then `qW | σ(b^f)` and `σ(b^f)<3b^f/2`, so `b^f>2qW/3`. With this atom's price removed, one gets `N^C>V(2q²/3)^C/(m^A W^(A−C))`; removing the atom's loss factor only strengthens the bound, so the old full `U` may safely remain. If `M=XD` including any separately proven ordinary reserves, and `D` including those reserves is partitioned into pairwise coprime anonymous blocks, then `gcd(D,b^f)≤K` where `K` is their maximum. Separately `N>(M/K)2q²W/3`. Taking the `(A−C)`-th power of the second and multiplying cancels `W`:

```text
N^A > V (M/K)^(A−C) (2/3)^A q^(2A) / m^A.
```

No independent source is selected for either inequality. The raw mass and price cannot simply be multiplied with arbitrary overlapping sources; this cancellation controls that overlap explicitly. For interior Euler candidates the residue of the complementary factor is inverse at `q0=2m−1` modulo `4m`. Skipping very wide residue windows is conservative. At any price target `p_i≡3 mod4` that has `j_i>0`, quadratic reciprocity excludes the block `σ(p_i^e)` from an interior Euler placement.

## Implementations

- [OrdinaryU28.py](OrdinaryU28.py) adds open-Euler square atoms, complete three-target cubic CRT allocation and full exact arithmetic to the `t^28,U^a` prefix from [T28U.md](T28U.md). It reuses the checked order/effective-length range; every retained squared base is treated conservatively. A few exact rational deficit factors are multiplied as fractions; larger tables use monotone upward rational rounding to preserve a bound.
- [Verify31Q210.py](Verify31Q210.py) binds the complete two-target atom enumerator [Replay.py](../ThirtyOne/Replay.py), tests `31^268,3229^210` by the uniform cap, and tests `31^268,3229^156` with the exact outside and inside allocation rules. The 102 case is not covered here.

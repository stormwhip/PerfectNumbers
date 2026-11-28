# U^12, ordinary 1109: four-target price removes 43 exact rows

Frozen baseline `495c59f55456a70994ce7848487e0c4e262c1984`; exact prefix `19^276,1176672733^28,244980869729503357305949^12`. Put `s=1109`. By [the Euler-placement proof](T28Euler.md), `s` is ordinary. The raw compulsory exponent tail is 217, with 54 live even exponents `2,4,…,108`. The present proof **excludes 43, namely `24,26,…,108`**. Bounds or residue cuts here do not exclude all Euler windows for `2,4,…,22`.

Let `t=1176672733` and `U=244980869729503357305949`. We retain the exact `(19,t,U)` price with all weights `19/10` and a common powered loss bound for all children; fixing `s` only increases the raw `lcm(X,Y)` and reduces incoming demand caps, so a loss table for the original prefix is a valid superset. The table in [OrdinaryU28.py](OrdinaryU28.py) was computed for prime ordinary bases and one possible Euler-square atom.

An atom supplying `s` can only have order 277, no LTE, and with effective expenditure 276 has weight 100 and zero deficits, as in [VerifyT28Ordinary.py](VerifyT28Ordinary.py). The only odd orders of `t` which share 277 are 277 and 831. Check **all** primitive combinations of their roots mod `t` with the full order-277 roots mod `s` under CRT. For each class, increasing its odd representative by `2*s*t` is beyond the actual size bound. At T-order 277 the only in-range odd integers are `19,19²,19³,19⁴` and at T-order 831 there are none. No ordinary prime or Euler square among them is legal (19 is fixed ordinary). Hence an `s` supplier cannot have either overlapping order at `t`. In all remaining configurations the complete length scan checks that an additional 276 powers can be reserved independently for `s`, with the three usual cubic and higher-order prices and 19-LTE still fully accommodated. This is necessary at every possible odd length ≤5031 and is not a presumption of independence from unequal target labels.

In each exact `s^h` branch, write `i=v_s(q+1)`, where `q` is the Euler prime, and `m=s^i`. Build a window-specific upper bound `Q` for `q`: if exterior, use the raw cap or the tighter same-emitter cap when pairwise coprime block groups prove it; if interior, retain only blocks admitting the complement residue for `q≡2m−1 mod4m`. For the three other linear supplies let their weighted base product be `z`. Because `q≥m*z`, their aggregate effect is bounded by charging `q^9/m^19` against the exact powered price; explicitly,

```text
N^10 ≥ V · m^19 · s^(1000(h−1−i)) / Q^9.
```

Here `V` is the powered `(19,t,U)` price and fixed mass of this exact branch. As an independent terminal, optionally weaken the fourth weight from `100` to `19/10`. Then all four targets share one weight, and the exterior same-source cancellation in [UniformEuler.md](UniformEuler.md) applies even if the compulsory Euler emitter itself supplies 1109. A finite set of exact integer breakpoints separates the direct price from the cancellation region; at least one must pass both comparisons to close exterior. For interior Euler, compare against the maximum stripped block. This second terminal excludes four additional rows beyond the first method. The size and price uses of the anonymous mass are distinct, and the two prices are not multiplied. All comparisons are exact; no factorization, network or floating point is required.

```sh
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Pricing/U12SHigh.py
```

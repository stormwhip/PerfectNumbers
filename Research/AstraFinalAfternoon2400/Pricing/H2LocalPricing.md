# Local price refinement of the remaining `1109^2` prefix

This supplement only refines the `h=2` source partition from [Proof276.md](Proof276.md); it does not modify that certificate or exclude the full `h=2` case. Reconstruct the 45 exact `b^276` source rows with the same `K=68465` argument, then also price the inbound demand at the **source base itself**. Use the standard-library [Explore276H2.py](Explore276H2.py):

```sh
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Pricing/Explore276H2.py
```

## Single-target stage

After appending exact `b^276`, write `c_b=276−v_b(Y)`; in this partition it equals 275 or 276. Every external ordinary component is distinct from the fixed rows. Take `w_b=min(12,min_{o>1 odd, o|b−1}(o−1))` (minimum of the empty set taken as `+∞`). For a positive `b`-supply from an external prime `r`, the usual LTE effective length is `b^u` in order 1 and `o·b^k` for higher order `o`, doing exactly the same job as in [Proof276.md](Proof276.md). Verified `3^(b−1)≥b^w_b` pays order-one and the LTE surplus using `b^k−1≥k(b−1)`. For each higher odd order with `o≤5031`, a positive basic deficit at `z` implies `r^(o−1)< b^(w_b z)`, so `r<b^z`. Enumerate only in this valid least-residue regime, or end earlier if every least **odd** root exceeds the strict actual size cap `floor((B/X)^(1/(o−1)))`; all deeper classes are then impossible. Hold one maximum deficit per possible base. If its product is `U_b`, the exact terminal is `X·b^(w_b c_b)·den U_b>B·num U_b`. This excludes 38 of the 45 rows, leaving `b∈{13,67,103,139,199,271,277}` for the next stage.

## Joint stage for 19 and `b`

Raise all bounds to the tenth power and use weights `19/10` for both targets. Their mutual LTE bases are excluded from the opposite order support by checking `19∤b−1` and `b∤18`. For both nontrivial orders `o1,o2`, let `L0=lcm(o1,o2)`. Actual odd length `L` is a multiple of `L0·19^k·b^j`; the extra length above `L0` pays for both LTE shifts because `L−L0 ≥ (19−1)k+(b−1)j`. If one order is 1, the actual effective orders are coprime (the order-one target does not divide the other target's order), so order-one and LTE costs can also be paid individually; the spare base exponent for any remaining nontrivial order is at least two. If both orders are nontrivial and **not both 3**, `L0−1≥8≥2+2`, so two exponents per target suffice for their basic deficits. These separate deficit tables are raised to the tenth power and bounded by least residues (`20≥19`). If both orders are 3, allocate two exponents once and compute an exact joint cubic CRT deficit for `M=19^i b^j`; strict positive deficit means `r^20<M^19`, hence `r<M`. Capped actual basic valuations are within the enumerated demand bounds. Only rigorously impossible bases are removed (range, parity, fixed distinctness, or Fermat compositeness witness). The maximum of the cubic joint loss and the product of the two separate losses controls each actual base, and distinct bases are multiplied only once. The terminal uses the exact integer comparison `X^10(19^c19 b^cb)^19·den U>B^10·num U`.

The isolated exact run excluding all six joint-price rows returned `h=2 joint missing-target prices: remaining [13]`. Thus the residual is the single exact prefix `19^276,1176672733^1,1109^2,13^276`; no conclusion is claimed for that prefix.

No multiplication by `Y/gcd(Y,X)` takes place in either price. That earlier raw comparison applies as a separate necessary condition only.

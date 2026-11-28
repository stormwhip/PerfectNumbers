# Independent Euler review: root 31 anonymous cuts (not first or key closures)

Scope throughout: frozen `495c59f55456a70994ce7848487e0c4e262c1984`, odd perfect `N≤10^2400`, canonical root 31 (bans `19,7,11`), exact root exponent. No complete keys. Only the **default non-price** anonymous matrix is reviewed here, not `--price`.

## `(31,268)`, fixed `3229^f`, `f=102,156,210`

Full finite [allocation verifier](Check31Masks.py) independently reconstructs both coprime anonymous blocks as geometric sums and checks every candidate through `10^8` in their required progression as well as composite and nonsquare witnesses. For each positive odd order factor of the prime-length sigma, the order is exactly that length: order one could occur only at that index prime, excluded by direct gcd. Thus a prime divisor lies in `1 mod 2ℓ`. The split `(i,j)=(v31(q+1),v3229(q+1))` is covered by the exact capped supply rectangle; `q≡2m−1 mod 4m` for `m=31^i3229^j`, including the `(0,0)` class with representative 1 (the exterior lower bound uses `q≥5`). Higher exponent classes use `α=5` as a monotone relaxation, not an assertion `α=5`. If `i>0`, reciprocity forbids q in the root block since 31 is 3 mod 4. For each other internal candidate, `q≡1 mod ℓ`; solve for this actual CRT class and for the inverse cofactor class, bounding both below by `10^8+1`. The cofactor is >1 because the block is composite and q prime. Rejection when the minimal class-product exceeds the block is strict; a single candidate cofactor is also checked for exact division. No untested divisor class is dropped.

If q is internal to one block, the other is coprime to it and nonsquare, so it needs an additional ordinary prime factor ≥`10^8+1`. The internal block's own cost is bounded by `max(block,q^α)`, not by their product. If q is external, each mutually coprime nonsquare block has a distinct ordinary square-completion factor, justifying the square of the lower factor bound (not squarefreeness). One independent exterior inequality is `N>(2/3)Xq^(α+1)` because some other ordinary source emits q; it is not multiplied with the preceding mass bill.

`python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/ThirtyOne/AnonymousEuler.py` and the independent `python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Audit/Check31Masks.py` both exited 0. The latter uses the reverse CRT construction and exact output powers, and recomputes complete matrix digests (102/156/210):

```text
0f4785bb763766e918432a6b63b0c4a80696c79592896dd83cac92c9c7883f7a
9343823e6a6c23a9016da9a4daeab31e6f9b9f7083e6d4700791e8e41a611b0a
f1d8f7827ba215ec0e90635f678237b6f977aa1005a3e26c3fc81205a2eb5d55
```

**2026-11-28 correction (PR #14, independently checked).** The default non-price test for `f=102,(i,j,α)=(0,0,5)` uses `Q=5` and retains the exterior bit: both `XAC(10^8+1)^2 5^5≤B` and `2X·5^6≤3B` hold by exact integer evaluation. The earlier statement that every exterior high-index Euler position was excluded for 102 is withdrawn; this does not imply a realizable prime or counterexample. For 210 the original observation concerning masks consisting only of the exterior position is retained as a historical observation. These are local tests, not full-first exclusions. The current frontier is given by [the checkpoint](../Checkpoint.md); only 102 remains for (31,268). See [the new theory](../../JointConservation2400/Root31x268.md).

## `(31,456)` and `(31,466)`

For positive `j=v31(q+1)`, reciprocity forbids q in `A=σ(31^e)` because 31 is 3 mod 4, q is 1 mod 4, and an odd order in a root emission would make 31 a quadratic residue mod q. All allowed Euler exponents are `1 mod4`; the size of `X A q^α` and independent size of the distinct q-emitter give monotone necessary comparisons. Independently regenerate the first excluded j for each minimum `α=5,9,13,17,21`: **140,78,54,41,34** at e456; **136,76,52,40,33** at e466. None at `α=1` by this comparison. Higher `α` only strengthen these cuts, and if `5^α>B` the exponent is globally impossible.

Optional source shape cut: when `q>8000`, order one cannot contribute because the actual length is at most 5031. For odd order `o>1`, if `L/o≥k` then `r^h>3^(k−1)(2Q/3)^k` with `Q=2·31^j−1`, from `q|σ(r^(o−1))`, `σ(r^(o−1))<3r^(o−1)/2` and `r≥3`. If `β=v31(σ(r^h))≤e−j`, then `N≥31^j(r^h)^2` by stripping 31 from that geometric output; the output is automatically coprime to r. For an **exterior r**, multiplying the output alternative by A is valid **by adding valuations from distinct fixed sigma factors**, not by presuming the outputs are coprime; A is coprime to r and 31. A separate size lower bound `XQr^h` can also add A only if r exterior. Monotone integer cutoff recomputation agrees with the `first_j_by_source_index` table of [EulerCuts.py](../ThirtyOne/EulerCuts.py). It derives specialized restrictions, without claiming each is new relative to all prior source results. Candidate and independent arithmetic both exit 0.

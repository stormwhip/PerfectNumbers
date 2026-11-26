# Night2400 C2 — three conditional fibers of (19,330)

From the repository root, run this with standard-library Python (assertions enabled):

```text
python -I -S -B Research/Night2400/C2/Verify.py
```

This packet concerns only odd perfect integers `N <= 10**2400` with `19^330 || N`, the outstanding actual of `P19_I00065`. It excludes the exact pivot exponents **8, 10, 12** for the prime `q = 1214428680506010004551311201724184433986966434253654794712076383` (210 binary bits). The checker certifies `q` and checks it divides the forced cofactor of `19^330`. It rebuilds the split starting at `v_q(sigma(19^330)) = 1`: all odd exponents are Euler-incompatible, even exponents 14 to 24 are rejected directly, and the monotone prefix-only size bound rejects every exponent at least 26. Pivot exponents **2, 4, 6 remain open**; this is neither a root cover nor a shard closure, and it cannot be lifted to other actual exponents.

At pivot exponent 8, the checked-in ECPP chain certifies the additional prime `r = 2649006202622389754026474949684537136117722932291062868195158132223440533168779423867212541`. The checker verifies that it is forced by the fixed path. It rebuilds all exact exponents for `r`: 3 and 7 violate Euler form, 4 through 6 are rejected directly, and the prefix-only size bound excludes every exponent at least 8. Only `r^1 || N` and `r^2 || N` remain. Both are checked separately, including the already-fixed Euler component in the first case. This generalizes the singleton forced-square split to two surviving exponents, without treating either exponent as forced before split.

The [joint valuation checker](../../FinalSprint/JointValuation.py) targets `19` and `q`; at exponent 8 the additional fixed component contributes its full emission and size, but is not a valuation target.

| Exact `q` exponent | Exact additional `r` exponent | Receipt `(exceptions, [price-window, no-block, interior-check])` |
| --- | --- | --- |
| 8 | 1 | `(16, [0, 0, 0])` |
| 8 | 2 | `(16, [1260, 1388, 0])` |
| 10 | — | `(16, [2294, 948, 68])` |
| 12 | — | `(16, [3831, 141, 0])` |

`Discover.Finder(Discover.Bank(<official data-v1 index>), 0)` located `q` at `(19,330)` and `r` at `(q,8)`; PARI was used to generate ECPP witnesses. None of the discovery data or programs is used during replay. The C2 packet does not load the sibling C packet.

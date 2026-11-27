# C7 — independent review of exact prefix supplier price

Candidate `6343cd72e6aa49d3b9756934a273c7d979a83573`, detached clean tracked checkout, CPython 3.11.9. SHA-256 of `Leaf2.json`: `2ab827e1024bd78e093d93bbb53e3ab252f1d6099851eb61470a40af9fb6b293`; `PrefixPrice.py`: `04e63cb8171cffe4b82787a7346a4a37ad4fa25bb93b1daff43d467e5c12af2a`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C7/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C7/Verify.py --regression
```

**PASS exact local path only.** Both commands exited 0 at 2026-11-27 01:52:36.616–01:53:17.590 +08:00. Candidate 16.0628925 s, receipt `(1,[4442,9335,8483])`; known regression 25.1131185 s, receipt `(10,[5188,1814,0])`.

The candidate freezes one exact local path `[(13,372),(438552673580231875649,12),(756749110661077,4),(463891,28),(2239,2),(128599,60),(3,2)]` in canonical root 13 (19,7,11,31 absent). All seven prime labels are checked. Replay is local: it does **not** prove completeness of a parent split, does not discharge the entire first fiber 12, and does not close the key or shard. The known `(31,388)` regression is not new credit.

**Paid mass / lcm.** For exact assigned part `X`, the odd fixed sigma product `S` divides `N`; the conflict test establishes no excess assigned valuation, so `C=S/gcd(S,X)` is coprime to `X` and divides `N/X`. For a genuine nonfixed prime power `a=r^f`, exact scope gives `a | N/X` as well. Thus `X*lcm(C,a) = X*C*(a/gcd(C,a)) | N`. The additional rejection `a/gcd(C,a) > floor(B/(X*C))` is equivalent to strict overflow of this necessary integer divisor, **retaining equality**. It applies only to deficit candidates (`num > den`) and can never remove a genuine supplier. For exterior `r`, no paid overlap exists; for interior `r`, only unforced excess is compared. It does not add `C` to the multiplicative price, which still starts from `X` and hence does not charge interior components twice. Nor does it sum individually feasible suppliers as though their budgets were independent necessary exclusions.

The source diff against frozen JointValuation changes only this predicate and its comments, not the LTE/Hensel/CRT enumeration or price/euler comparisons. Independently recomputed exact fixed `X,S,C`, coprimality, canonical absence, abundancy and `XC<=B`. Target valuation capacities `(13,370),(128599,59)` give 22,260 Euler windows; `floor(log10(X)), floor(log10(C)), floor(log10(floor(B/(XC))))` are 1194,1142,63. Integer floor identities and direct lcm equivalence were checked independently.

**Strict Euler windows.** At no exponent-one Euler component, `V=X M²/U>B` must hold. At exponent one, the prime `t≡2m−1 mod 4m` where `m` is the target mass taken by that component. First require strict `V(2m−1)>Bm²` or continue. If `t∤C`, require the independent strict exterior lower bound `XC(2m−1)>B`. Otherwise `t` divides one fixed sigma residual block, and any positive cofactor must belong to the fully enumerated residue progression modulo `4m` within the inclusive geometric bound; the quadratic-reciprocity shortcut is only used for an odd exponent-order obstruction when the emitter is `3 mod 4` and divides `m`. A large unresolved interior progression fails the verifier; it is not silently excluded. The purported 4,442 + 9,335 + 8,483 categories sum to the full 22,260 windows.

# `(19,222)`: exact ordinary/unrestricted `f=2,g=22,j=2` cut

At the canonical frozen `(19,222)` root, with pivot bases `t=7579985624053`, `r=3705121363`, `q=2032322226061`, the exact prefix `19^222,t²,r^22,q²` cannot occur in an odd perfect number ≤ `10^2400`. The proof [rechecks](VerifyPlain222J2.py) the frozen `g=22` third window, its strict raw tail 114, and membership of 2 in the original live set `[1,2,4,18,28]`. The only sibling values remaining after the disjoint [inert](Proof.md) and [masked j=4](Mask222J4.md) proofs are `18,28`.

The [integer forest](Plain222J2.json.gz) has no local absence assumption and allows every legally possible Euler prime, including outside the forest. The tail remains the monotone bare-power lower bound. Nine new actual outgoing factor labels were available to strengthen a previously insufficient forest; each used label's bundled ECPP certificate is checked and it contributes only if its parent really emits it. The proof uses two independent integer recurrences. See [base algorithm invariants](Forest222.md). No withdrawn PR #11 method is used.

Cold replay exited 0: bounds floor 2407 in both evaluations, seven roots, 707 edges and 111 verified ECPP chains. SHA-256 `e23cd70133042e8b236f6989f74c9f1c7447a09957a264045a01e7bad76e3785`.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyPlain222J2.py
```

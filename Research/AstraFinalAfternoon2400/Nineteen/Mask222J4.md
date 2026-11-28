# `(19,222)`: exact masked cut `f=2,g=22,j=4`

In the canonical root-19 frontier frozen at `495c59f55456a70994ce7848487e0c4e262c1984`, the exact four-row prefix `[19^222,7579985624053²,3705121363^22,2032322226061⁴]` is impossible for an odd perfect number at most `10^2400`. The frozen third window originally left `[1,2,4,18,28]`, strict tail 114. After [the inert `j=1` cut](Proof.md) and this `j=4` cut, it leaves **`[2,18,28]`**. Since the preceding overlays close the other complete second windows under the first exponent 2, these are the remaining deep windows under that first fiber; the fiber itself remains open.

The nine certified independent compulsory roots give a conservative lower abundancy `I>1.84418`, obtained with minimal exponents permitting individual Euler choices independently. More permissive Euler choices only weaken this lower bound. Neither 7 nor 11 is a fixed or compulsory root; multiplying `I` by `σ(7²)/7²=57/49` or by `σ(11²)/11²=133/121` strictly exceeds 2 by exact arithmetic. Both primes are `3 mod 4`, therefore cannot be Euler. Consequently 7 and 11 are independently excluded before any forest is evaluated; this is not a stronger canonical ban and is not used outside the named exact prefix.

Two distinct [masked forest recurrences](../../Night2400/A/MaskedForest.py) then keep all remaining Euler possibilities and return strictly greater than `10^2400`, both decimal floor 2426. The [verifier](VerifyMask222J4.py) rebuilds the full raw window, every compelled root, each local absence, prime labels, actual edge incidences and the unrounded dual strict comparison. Cold run exit 0, 21 ECPP chains; [Mask222J4.json.gz](Mask222J4.json.gz) SHA-256 `02c74f80b8112d0e4a9b3fdb1f36b118e3f3d7ed450837a194f1f3517fdc7b27`.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyMask222J4.py
```

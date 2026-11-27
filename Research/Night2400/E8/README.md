# (7,36): complementary first fibers for P7_I00011

The fixed first pivot `4805345109492315767981401` has valuation one.
Among exponents below the size tail 96 (floor 2405), exactly 31 first
exponents are live; 32 otherwise admissible exponents are eliminated
by the exact-state bound. The preclassified siblings and the full domain
are reconstructed by the standard verifier.

The first checkpoint proved fibers `1,4` only; it is subsumed by the retained four-fiber packet. Fiber 1 is one ordinary-size exact forest.
Fiber 4 uses the 214-bit second pivot
`18937002577126532099173623699263783311238456422353508197844826911`;
it has eight children, all excluded by forests. Its last previously
unproved exponent 4 was excluded directly by a new forest (floor 2405),
instead of keeping a speculative 48-hole deeper tree. The
three-fiber checkpoint (also subsumed) closes `6` via its 455-bit second pivot. The last missing exact
square of that pivot uses one forest at head 384 and floor 2400, instead
of leaving its deeper 34-bit pivot as a separate split.

The [four-fiber checkpoint](Fibers7x36ComplementFour.json.gz), SHA-256
`5ae6d109c9c4440db0bd4c4a71e07f59b921e87f97f3b162c7cb7ae1af1d3227`,
also excludes `18`. Its last two leaves under the same 71-bit pivot
passed exact forest checks (floor 2405 for each). This packet has 66
forest leaves, five inner splits, 103 direct rejections, and 1,428 ECPP
chains. It proves `1,4,6,18` only.

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E8/Fibers7x36ComplementFour.json.gz
```

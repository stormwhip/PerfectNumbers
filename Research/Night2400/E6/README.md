# (7,682): complete exact first-pivot exclusion for P7_I00123

The forced first pivot `6298826803` has initial valuation one. The live
fibers are the even exponents 2 through 64. Even exponents 66 through
128 are directly rejected, odd exponents are inadmissible, and the
monotone size tail starts at exponent 129.

Only the complete packet is retained here. The anonymous 58 fiber uses
joint pricing on both exact components (99 blanket exceptions and Euler-window
counts `[37010,2604,0]`); separately pricing either component did not close it.
At first value 36 the difficult `2765677^16` child closes by an exact forest
(floor 2423) after a capped 220-second PARI factorization of its 343-bit emission.
## Complete packet

The [complete certificate](Fibers7x682Complete.json.gz), SHA-256
`856e9c4dd428cec862860d1c1fb8effead573020d9673e68e0cd998142eff138`, covers
the entire 32-fiber domain. It includes 6,679 ECPP chains, 1,378 forests,
29 splits below the first pivot, and one joint price leaf. The difficult first fiber 6 has 545 forests
and nine splits. Its 186-bit forced pivot is
`50083139791258965781304433685356860890168148134478426219`, with initial
valuation 1 and live exponents `2,4,6,10`; the monotone tail begins at
22 (floor log10 2430). The other exponents below 22 fail the branch
conditions or the direct exact-state bound. The four late forest
prefixes, in addition to the first pivot's exponent 6, were
`(r,2),(349,1),(43,2),(631,2)`, `(r,2),(349,106),(43,2),(631,2)`,
`(r,6),(43,2),(631,2)` and `(r,6),(43,2),(631,4)`, where `r` is the
186-bit forced prime. A 220-second discovery budget per prefix with
head 640 and smoothing parameter 29 yielded respective forest floors
2404, 2798, 2400 and 2402. Exact replay checks every sibling and every
size tail, not only these low prefixes. The root-only tail at 129 has
floor log10 2407.

No ledger edit or divisibility lift is claimed.

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E6/Fibers7x682Complete.json.gz
```

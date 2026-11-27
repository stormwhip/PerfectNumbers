# G2 — (19,432), eleven exact conditional fibers plus partial masks

Candidate `2d5a08175ba170b5982346a0c2c0fa9ed58c1eeb`, detached clean tracked checkout, CPython 3.11.9. Packet SHA-256 `9fa08422b67fd1d09bdcbbedd7d61511539e700cf0907adc13ee22dfeaf6ae95`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/G2/Verify.py
```

**PASS conditional.** 2026-11-27 02:11:38.155–02:17:39.168 +08:00, elapsed 361.016003 s, exit 0. Forest minimum floor 2402, minimum exact abundancy floor 2000358 ppm. Eleven full first fibers and six projected support masks, not a complete key.

Independent integer reconstruction confirms all 128 masks containing 19, compelled pivot `11842464881317660217` valuation 1, `q≡1 mod 4` and `3 | q+1`, first raw size tail 69. Raw viable cells are 2440 across all masks and 1006 across the 55 projected masks. Complete first valuations `[2,5,9,13,17,21,25,29,32,33,34]`; full projected mask closures `[67,81,113,189,197,223]`. There are 908 OPEN cells across 82 masks, 584 cells projected, so no key or shard closure. Independent check counted 555 regular forest leaves and 1 special forest, 69 fixed-path rational abundancy cells and 40 root abundancy masks; 3663 embedded ECPP labels. Projection is not used as a completeness premise; equality is kept at the size threshold and abundancy must strictly exceed 2.

Special cell `(mask 113, first valuation 16)`: 5 is compulsory, 7 absent, and no fixed Euler component. Positive exponents of 5 below six admitted by the Euler rule are 1,2,4,5; independent exact sums rule out 2,4,5 under the banned support. For every exponent at least six, independent rational abundancy with required primes `{3,5,13,409}` and exactly one possible Euler placement (or outside the listed set) yields a strict lower bound over 2, minimum floor 2068765 ppm. Thus only exact `5^1` remains. Its scoped forest fixes this Euler component, verifies prime ownership and uses two exact strict integer bounds; the result does not transfer to other masks or prefixes.

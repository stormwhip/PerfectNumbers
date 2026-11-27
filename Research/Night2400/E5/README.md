# (7,586): exact pivot proof for P7_I00106

The forced first pivot is `q=360863295229781`. The first monotone size tail
is 98, and 35 additional admissible-before-state-test values are directly
rejected. The exploratory counts progressed from 25 to 31 to 33 of the 35
live fibers; only the final complete packet is retained here.

## Complete certificate

[Complete packet](Fibers7x586Complete.json.gz), SHA-256
`21e875b86bd945adf4f600d35de066ccba8b769c5f7b8aa57f0150b4061d458b`, covers
all 35 first fibers. Cold replay confirms no open paths, 448 forest
leaves, 22 inner splits, 477 direct rejections and 1,647 ECPP chains. The six nontrivial first
fibers have the following second-level partitions; each second pivot
has initial valuation one.

| First exponent | Second pivot | Live second exponents | Monotone tail starts |
| ---: | --- | --- | ---: |
| 1 | `9020467` | even 2–100 | 202 |
| 2 | `169339815141867936921826447` | even 2–26 | 54 |
| 6 | `86400418231171916049438185093890962633068083355090388366865418565919125619859` | `2,4,6,8` | 18 |
| 10 | `37447602253249` | `1,2,4,5,6,8,9,10,12,13,14,16,18,20,21,22,24,25,26,28,29,30,32,33,34,36,37,38,40,41,42` | 85 |
| 18 | `134219759227` | `2,4,6,8,10,12,14,16,20,22,24,26,28,30,32,34,36,38,40` | 82 |
| 28 | `5685683` | `2,4,6,10,12,14,16,18,20,22,24,28,30,32,34,36,38,40,42` | 92 |

Any other sibling below each tail fails admissibility or an exact-state
bound. Replay recomputes all deeper siblings, rather than trusting this
summary. No divisibility lift or ledger edit was made.

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E5/Fibers7x586Complete.json.gz
```

Discovery-only: in the first bounded ECM batch `B1=240000`, up to 550
curves/170 seconds per residual, yielded additional factors for first
exponents 16 and 22. In the descendant batch `B1=380000`, up to 600
curves/150 seconds per residual, yielded `23889543456671` in the 331-bit
residual shared by the difficult exponent-2 subtree and enabled stronger
forests for all remaining low and middle fibers. The factor bank,
FLINT, ECM and PARI are not needed for cold verification.

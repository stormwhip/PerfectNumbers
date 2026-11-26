# (7,420): complete first-pivot cover for P7_I00081

This is root seven, not the separate root-nineteen exponent 420 case.
The forced 120-bit first pivot is `1169407471026387018305554817094515359`,
with valuation one in `σ(7^420)`. Its live exponents are
`2,4,6,10,12,14,16,18,20,22`. Below the monotone size tail at 48
(floor log10 2405), the exact-state bounds directly reject
`24,28,30,32,34,36,38,40,42,46`; the other nonlive exponents fail
parity or forbidden-emission tests.

The [complete certificate](Fibers7x420Complete.json.gz) covers all ten live
fibers, including the final valuation 6. SHA-256
`0425676e7b43125d1b1369b9dba1b128347575ddabb6d0caeacc2428c4ef97d0`.
The independent replay checked 1,076 forests, 30 nested splits, 1,119 direct
exclusions, two joint price leaves and 6,730 ECPP entries, with no open paths.
In valuation 6, `120298224779693` has 34 exact live exponents and monotone
tail 93. The deepest late split `284860058207025151` has exactly even live
exponents 2 through 22 and tail 45; all siblings are computed independently.

The initial [five-fiber certificate](Fibers7x420Five.json.gz) covers
`10,14,18,20,22`, and deliberately excludes no claim for `2,4,6,12,16`.
SHA-256 `201d8fe2e7f4b15f6d2afd1c8f0d2fe26b03fc8364a2659889207fd68a618efd`.
The first four are dual-evaluated forests. The `22` leaf uses joint
incoming valuation with the first pivot as its sole target, no blanket
exceptions, and Euler-window counts `[8,0,14]`.

The historical [nine-fiber certificate](Fibers7x420Nine.json.gz) closes
`2,4,10,12,14,16,18,20,22`, leaving only `6` open. Its SHA-256 is
`6fa4aedf044f62e21c365ceec486b9c97ddbda3fe801783c362609d75d050a5f`; cold
replay reports 55 forest leaves, four inner splits, 65 direct exclusions,
and one price leaf. This is a strict subdomain, not a shard closure.

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E4/Fibers7x420Complete.json.gz
```

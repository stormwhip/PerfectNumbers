# (19,162): complete proof for P19_I00036

[Complete certificate](Fibers19x162Complete.json.gz), SHA-256
`ad2d23ca3817e8a04577246028c2d80c8b942d208a990326127b323c2a711b58`.
The [new fourth fiber](Fiber19x162Four.json.gz), SHA-256
`ca9b7e8c2d48ee117f05b8f752653954c3c53ba4106b6cb8f82cf1ce68f3617c`,
was sealed separately and then combined with the already verified fibers
2 and 6 (input SHA-256
`dd5f825e557807f7f23569ca8bcf20536a6f39e48355f8648f67a87bd9d8d65b`).
No ledger changes and no divisibility lift from this exact exponent.

The 512-bit first pivot is
`6785461147705964602329621028147667329358150964229375773743284675075632536874762538857627745903744014004067764051322273926713174135119053611369178360593559`.
Its compatible valuations are `2,4,6` and all three are excluded. The odd
valuations are inadmissible; `8,10,12` fail the direct exact-state bound;
the first monotone size tail is `f≥14`.

In first fiber 4 the forced second pivot is
`342824539081437076343940054698469728805379685794103`, with initial
valuation 1. Its odd valuations through 17 are illegal; `10,12,14,16,18`
fail the direct exact-state bound; `f≥19` is past the monotone size tail
(strict integer comparison, floor log10 2400 at exponent 19). The four
other siblings have a forest each, with independent evaluations agreeing:

| Exact second exponent | Roots | Owners | Head | Floor log10 |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 4 | 331 | 192 | 2405 |
| 4 | 5 | 645 | 384 | 2401 |
| 6 | 7 | 152 | 192 | 2404 |
| 8 | 4 | 28 | 192 | 2403 |

Replay both packets offline from the main checkout once these files and
its [Night2400 verifier](../VerifyFibers.py) are present:

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E2/Fiber19x162Four.json.gz Research/Night2400/E2/Fibers19x162Complete.json.gz
```

The complete receipt is `covered=[2,4,6]`, `open=[]`, and
`counts_forest_split_direct_price=[5,1,8,1]`. The new fiber alone has 99
ECPP chains and precisely four forest leaves. The combined certificate
retains the prior sibling witnesses unchanged.

Discovery first enumerated 35 deep open states. Of these, 34 shared the
290-bit composite remaining in the second pivot's square emission. A
bounded GMP-ECM run (`B1=200000`, at most 550 curves and 110 seconds per
residual) split it into `266028891483340333` and
`6848000765803122294344694763407717979023194314254433348828648502959153`.
The new factors allowed replacing that entire deep tree with a single
forest. The remaining second-exponent 4 leaf used a 71-bit recovered
factor (`1419823391966350551941`), local smoothing with parameter 32, and
head 384; the 2045-bit main cyclotomic residual did not need to be factored.
Discovery factors, ECM, FLINT, and external factor data are not replay
requirements.

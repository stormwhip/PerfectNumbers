# P19_I00050 — exact key (19,238)

This packet is an addition to the main Night2400 candidate, not a divisibility-lifted or total proof. It covers first-pivot exponents `4,10,12` of `q = 606492758240679674698864343145363724798136175178043`. The compatible first domain is the nine even exponents `2..18`. The previously sealed main candidate covers `8,14,16,18`, so the union still leaves `2,6` open. The 9 even values `20..36` exceed the exact-state base bound. Odd values are inadmissible since `q ≡ 3 (mod 4)`. The monotone size tail begins at `37`.

- Packet: [Fibers19x238.json.gz](Fibers19x238.json.gz)
- SHA-256: `b6eccf864b4209dfd8e938758cf7575775b45bc5f2ab4e0f00baf46332092bb7`
- Independent receipt: `counts_forest_split_direct_price = [1279,52,1514,0]`.

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F2/Fibers19x238.json.gz
```

Discovery only (not used during replay): repaired null leaves in the main scout tree. On fiber `10`, completing the cyclotomic factorization at degrees 3 and 5 of `7291076231098039426732402751` supplied the decisive large roots. For fiber `12`, the remaining three leaves needed degree-3 factors of `44147465170182893593` and degree-7 and degree-11 factors of `6269332690843`. Local GMP-ECM focused on those exact cofactors with stage-one bounds `175000..550000` and bounded curve counts; the frozen arithmetic checks divisibility, ECPP primality, exact-tree domains, and forest lower bounds without the factor index or GMP-ECM.

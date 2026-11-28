# Scoped final-night receipts (canonical exact valuations only)

Baseline: 1447d41b. Final update: (31,310) is FULL, 26/26 verified. See Proof31.md, Full31.py and the two Root31x310 gzip certificates. (13,262) is also FULL, 29/29 independently reproduced; see Proof13.md and Full13.py. The entries below record the earlier partial checkpoints and are superseded by those complete-key proofs.

* (13,262): new complete first exponents 12,28,42,60. Two additional historical OPEN paths close on first 16, whose only remaining canonical path is (13,262),(231050784610489,16),(6021499041499502533249,18). The other first exponent not yet covered by the union is 46. Overall **27/29** after prior 23 distinct firsts. SHA-256 23e91a724829cac6f849993452067010df3bb66d9d4bc8b4f07ad105b08b7f21; 1779 ECPP chains, eight new ones in the discovery run. Original G6 independent dual recurrence, exact domain and all certificate tests passed (including strict >B thresholds when decimal floor is 2400). Packet contains its own certs, no optional dependencies.
* (31,310): canonical first 18 now completely closed, not the previous conditional path or support masks. All four children of forced 707818236468853019281602309439653890995043 are closed by unconditional forests. SHA-256 680539a9f43d372b26816eab8a110e741db2ba2c5b461418bb270d9c3986374d; 502 ECPP chains, 27 direct eliminations and 1 split. Old 24/26 plus this = **25/26**, first 4 still open unless independently updated below.

Cold replay passed from repository root:

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/G6/Verify.py --packet Research/FinalNight2400/Others/Thirteen262.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/FrontierTree.py Research/FinalNight2400/Others/Root31x310F18.json.gz
~~~

Only the sealed gzip packets and historical verifiers are proof prerequisites. Unsealed search JSON, ECM outputs, optional local tools and online factor hints are not proofs. First exponents refer to the historical forced pivots for each root. See also F18Review.md and Audit18.py for the independent conditional 19^432 review.

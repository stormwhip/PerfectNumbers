# (19,280): all fifteen historic scout gaps excluded, but not an entire first fiber

This supplements [the eleven-path proof](Proof280.md) with all four remaining listed T⁶ gaps. In the same notation exclude exact prefixes (19^280,s²,t⁶,y^h) for **h=18,22,28,30**. These four are independent exact-path contradictions; the same [verifier](Verify280.py) and same free-Euler proof apply, without an assumed pattern for unlisted siblings. The new forests and [third](AbBook5X6X7.json.gz) and [fourth](AbBook8.json.gz) ECPP packages came from a more efficient choice of split prime; factor/optimizer heuristics play no role in proof replay.

~~~text
python -I -S -B Research/FinalNight2400/Ten276/Release280/Verify280.py 5 6 7 8
~~~

Clean elapsed 519.186 s; exit 0. Rechecked **3,195** ECPP chains needed by this subset, 40,911 split nodes, 128,881 raw/conflict terminals, 66,429 parity-size terminals, 6,102 strict abundancy terminals. Across both complementary runs the complete 15-gap total is 52,192 split nodes and 253,425 finite terminals (162,188 raw, 83,193 parity, 8,044 abundance; plus the exhaustive tail and forbidden-antichain handling at each split).

Coverage caveat remains material. For example the full direct domain under s²,t⁴,r includes r¹; it is not in the 77 submitted C13 certificates or the explicit 15 historic gaps. It was absent from the discovery gaps, not formally discharged by that fact. Hence no s² fiber, key or whole shard follows from this union alone.

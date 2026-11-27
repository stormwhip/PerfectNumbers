# (19,222) two-pivot reduction: seven first values and 42 exact pairs remain

After the [initial direct certificate](Firsts.md), first f is among 1,2,12,16,18,22,28,40,46 at t=7579985624053. Fresh mandatory factors of sigma(t^40) and sigma(t^46) found by local native ECM have allowed complete free-Euler forests for 40,46. The remaining seven fibers are exhaustively split at the separate prime r=3705121363, whose compulsory membership is independently checked as (r*t)|sigma(19^222). In each exact case the assigned components, odd sigma product, incoming valuations, Euler parity, partial abundancy and mandatory-size overflow are recomputed. All positive g from v_r(D) until X(D/r^v)r^g>B are accounted for once. Every claimed elimination uses a fully validated single-parent forest with the proper Euler role, complete listed prime proofs, and a strict lower bound. Replays consume 558 ECPP chains and exclude 227 complete conditional second rows. No claims on branches outside the listed root or exponent.

    python -I -S -B Research/FinalNight2400/Root222/Firsts.py
    python -I -S -B Research/FinalNight2400/Root222/Two.py

[Second stage verifier](Two.py) and [packet](TwoForests.json.gz). Residual pairs (f,g):

|f|g|
|---:|---|
|1|2,4,12,16,22,30,36,40,42,46,52,58|
|2|2,16,22,46|
|12|2,16,22|
|16|2,16,22|
|18|2,4,8,12,16,22,28,30,36,40,42,46,52,58|
|22|2,16,22|
|28|2,16,22|

Exactly 42 pairs in total, not 42 hypothetical numbers. The key is still open.

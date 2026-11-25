# Low-root ownership refinement

The historical archive is input data only. The scout adapted the worst-source iteration from [the root-seven search](../seven/Search.py) to the ordinary low-root order `19,7,11,31,13,3,5,17`. It learns factor hints from the current lowest valid cell assignment, then adds or reassigns owners and repeats. A heuristic alternative considers nearby cells to escape ties. Factor hints come from the archived graph bank, existing Ochem factor data, cyclotomic splitting and (for 31/438) GMP-ECM. No historical script was run. No change to the baseline or proof registry is required.

Both the scout and its search numbers are discovery only. Pack assembles an explicit self-contained graph and verifies its ECPP certificates; an exact comparison against `10^(2400*den)` is made by [the pinned arithmetic](../../NightLowRoute/Release/ForestReplay.py), followed by the existing [baseline-matching adapter](../ForestPackets.py). No claim in this directory depends on a float score or accepting an unfactored cofactor as prime.

| Seed | Historic scout | Best scout before trim | Search time | Disposition |
|---|---:|---:|---:|---|
| 13/100 | 2385.494787 | 2400.012212 | 20.2 s | [Exact packet](../Forests/candidate-13x100-refine1.pack.json.gz), strict >10^2400, 3 modes; P13_I00025 |
| 31/486 | 2366.230944 | 2411.319548 | 8.7 s | [Exact packet](../Forests/candidate-31x486-refine1.pack.json.gz), floor 2401, 1 mode; P31_I00091 |
| 19/148 | 2369.651109 | 2401.157279 | 174.9 s | [Exact packet](../Forests/candidate-19x148-refine1.pack.json.gz), floor 2401, 1 mode; P19_I00033 |
| 19/598 | 2358.855972 | 2400.896501 | 145.9 s | [Exact packet](../Forests/candidate-19x598-refine1.pack.json.gz), strict >10^2400, 4 modes; P19_I00107 |
| 19/360 | 2367.357462 | 2404.374432 | 167.6 s | [Exact packet](../Forests/candidate-19x360-refine1.pack.json.gz), floor 2404, 4 modes; one exact exponent only |
| 31/438 | 2360.270972 | 2402.489446 | 1.55 s after ECM | [Exact packet](../Forests/candidate-31x438-ecm-refine.pack.json.gz), floor 2402, 2 modes; P31_I00083 |
| 13/58 | 2320.455405 | 2401.632835 | 280.8 s | [Exact packet](../Forests/candidate-13x58-refine1.pack.json.gz), floor 2401, 3 modes; P13_I00016 |
| 13/490 | 2306.814687 | 2314.065902 | 360.9 s | Open |
| 31/316 | 2289.987994 | 2343.244608 | 310.4 s after ECM | Open; 2277-bit composite residual not split |
| 13/690 | 2305.572271 | 2400.799947 | 152.9 s after ECM | [Exact packet](../Forests/candidate-13x690-ecm-refine.pack.json.gz), strict >10^2400, 1 mode; P13_I00124 |

Replay from the workspace root: `python -B Research/Nov25/ForestPackets.py Research/Nov25/Forests/<packet>.pack.json.gz`. Only the packets in [Forests](../Forests/) are intended for registration. Scratch candidate graphs, logs, and missing-prime lists are discovery inputs/outputs and are not proof packets. To assemble a standalone local packet after prime generation, `python -B Research/Nov25/boost/Pack.py --cache <extra-cache> <graph>` (no write outside this directory).

## 31/438 ECM provenance

The original minimizing ordinary rows were `100294819^18` and `9133083420203886755465057^16`. The [recorded ECM hints](31x438-ecm1.json) are the proven-small primes `117100346982559771 | Φ19(100294819)` and `10364969 | Φ17(9133083420203886755465057)`. Each is less than `2^64`. The search checked divisibility before using them and then refined the ownership graph. To reproduce discovery when GMP-ECM is available, run [ECM.py](ECM.py) on the archived Intra seed or its saved best graph (use `--seconds 220 --b1 30000 --curves 1000`), then pass the [listed hints](31x438-ecm1.json) via `--hints` to [Search.py](Search.py). This is independent of proof replay, which needs neither ECM nor the archive. Neither hint changes the root sigma `σ(31^438)`, the root order, nor any tail rule. The independent replay checks that every explicit root divides `σ(31^438)` and activates each edge only with its actual valuation at the enumerated source; outside cofactors and the omitted exponent tail are handled by the unchanged pinned lower bound.

## 13/690 ECM provenance

The first refinement left the minimizing ordinary row `103878031^30`. GMP-ECM split its cofactor into exactly `Φ31(103878031) = 114143 × Q`; the [raw hints](13x690-ecm1.json) list both factors and source. The cofactor `Q` has 783 bits and must have its own ECPP chain. Both trial owner edges `114143 → 103878031` and `Q → 103878031` survived trimming, and both arithmetic divisions, and the product identity, were checked with exact integers. The graph retains the two roots `103878031` and `8047448191` (both divide `σ(13^690)`) and head 450. The replay treats the factors as ordinary graph edges, without assumptions on ECM or a modified tail rule.

## Literature check

[Ochem–Rao (2012)](https://doi.org/10.1090/S0025-5718-2012-02563-4) is the pertinent reference for factor-chain lower-bound computation. Recent [Fathi working paper v17](https://zenodo.org/records/21795420) gives a genuinely different complete-graph cut identity: for a set of exact components, the ratio of outgoing to incoming prime-power edge products is the product of `σ(q^f)/q^f` over the set, divided by 2 if it contains the Euler component. This follows by canceling internal valuations and the Euler factor in `σ(N)=2N`. However, the complete graph and the trial ownership graph are different, and strong connectivity does not imply termination or new distinct prime factors. Its stronger receiver-core reductions require hypotheses absent here. No literature shortcut was used to discharge a branch. Targeted ECM on the actual minimizing cyclotomic residual is the practical method that moved the 31/438 case.

# Final held-out root-19 ownership pilot (no proof credit)

Started at approximately 09:15 Beijing, reusing the ownership refinement and fixed root bans without changing the proof. Both 330-second discovery runs finished below threshold:

| Target | Nominal seed | Nominal best | Owners | Complete? |
|---|---:|---:|---:|---|
| `(19,576)` | 2285.396067 | 2362.451569 | 1535 | No |
| `(19,646)` | 2231.987340 | 2339.160805 | 1173 | No |

The [576 graph](Best19x576Finalpilot.json) and [646 graph](Best19x646Finalpilot.json) are factor-bank inputs for a future run. Their vertex primality has not been fully certified and the logarithmic scores are heuristic. Their `scout` and any hints are not acceptance inputs. These two are not included in [the delta](../Delta.json).

Reproduce the bounded discovery command with the historical seed and optional local factors as in [the method note](README.md); the uncommitted historical seed was passed only as data:

```text
python -B Research/Nov25/Boost/Search.py 19x576 --start <historical-cache>/Intra19_576.json --seconds 330 --label finalpilot
python -B Research/Nov25/Boost/Search.py 19x646 --start <historical-cache>/Intra19_646.json --seconds 330 --label finalpilot
```

The blind increases slowed to about four decimal orders per minute at `(19,576)`, so we switched to ECM only on residuals of the minimizing exact emitter options. The first factor pass produced the [576 hints](P19x576Finalecm.json) and [646 hints](P19x646Finalecm.json), and then a 250-second ownership run moved `(19,576)` to a nominal 2394.093 and `(19,646)` to 2401.107. The latter has a [verified two-mode packet](../Forests/Best19x646Finalecm.pack.json.gz), exact floor 2401. The [second 576 hint pass](P19x576Finalecm2.json) exposed three useful cyclotomic splits including `6956771765889793 | Φ_7(2910950775467019154235883439668838067692289)`; the 576 candidate reached nominal 2402.985 and its [verified three-mode packet](../Forests/Candidate19x576Finalecm2.pack.json.gz) strictly exceeds `10^2400` (integer floor 2400). Both are singleton closures in the frozen snapshot. All factor hints are conditional on the emitting component's actual exponent; proof replay activates only genuine sigma valuations and verifies every prime chain.

Further cold verification requires only the compressed final packet. Discovery reproduction (optional, GMP-ECM path specified in the script):

```text
python -B Research/Nov25/Boost/ECM.py Research/Nov25/Boost/Best19x646Finalpilot.json --seconds 165 --b1 22000 --curves 120 --label finalecm
python -B Research/Nov25/Boost/Search.py 19x646 --start Research/Nov25/Boost/Best19x646Finalpilot.json --hints Research/Nov25/Boost/P19x646Finalecm.json --seconds 250 --label finalecm
```

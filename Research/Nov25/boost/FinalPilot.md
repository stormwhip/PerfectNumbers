# Final held-out root-19 ownership pilot (no proof credit)

Started at approximately 09:15 Beijing, reusing the ownership refinement and fixed root bans without changing the proof. Both 330-second discovery runs finished below threshold:

| Target | Nominal seed | Nominal best | Owners | Complete? |
|---|---:|---:|---:|---|
| `(19,576)` | 2285.396067 | 2362.451569 | 1535 | No |
| `(19,646)` | 2231.987340 | 2339.160805 | 1173 | No |

The [576 graph](best-19x576-finalpilot.json) and [646 graph](best-19x646-finalpilot.json) are factor-bank inputs for a future run. Their vertex primality has not been fully certified and the logarithmic scores are heuristic. Their `scout` and any hints are not acceptance inputs. These two are not included in [the delta](../Delta.json).

Reproduce the bounded discovery command with the historical seed and optional local factors as in [the method note](README.md); the uncommitted historical seed was passed only as data:

```text
python -B Research/Nov25/boost/Search.py 19x576 --start <historical-cache>/Intra19_576.json --seconds 330 --label finalpilot
python -B Research/Nov25/boost/Search.py 19x646 --start <historical-cache>/Intra19_646.json --seconds 330 --label finalpilot
```

Do not rerun the same long bank scan unchanged: final increases slowed to about four decimal orders per minute at `(19,576)`. Select an exact minimizing emitter and obtain a new certified factor or improved independent lower bound before expanding substantially.

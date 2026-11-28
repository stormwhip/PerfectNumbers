# Follow-up exact exclusions under canonical (31,2)

Base [Certificate2More.json.gz](Certificate2More.json.gz) is immutable and locally replayed **117/143**. New packets are disjoint single-first supplements; new exact arithmetic does not rewrite old BFS scopes. Each supplement still re-enumerates and matches the entire 143-entry first domain but marks all other firsts `null`; when unioning, count only one closure per exponent. All fourteen additions individually replayed with exit 0: `{12,24,40,48,156,162,196,226,268,276,316,382,388,400}`. They are disjoint from the base 117. The consolidated [Certificate2Followup131.json.gz](Certificate2Followup131.json.gz) has SHA-256 `327683e54e81452029ee229a33346de4649f8445a82908510a2194437b978c5e` and 131/143 complete firsts, leaving exactly `{4,6,130,150,172,178,192,222,240,250,280,282}`; 60 internal splits, 1585 strict forest leaves, 6058 ECPP labels, 3 analytic leaves. The intermediate [130-first packet](Certificate2Followup130.json.gz) (SHA-256 `b224fba6df4a02fa1060e9b9f7bca38a0fb53f589e78fd870a5b939df893bf55`) exited 0 under the integrated verifier; the disjoint [first 196](Certificate2Fiber196.json.gz) (SHA-256 `00fa2a140654506bf65195402d0afb31a17d72b1220fb9a775d4261cf43a4d65`) exited 0, with 278 stricter forest leaves, 10 internal splits and 823 ECPP labels. The consolidated 131-first packet also exited 0 in the full isolated local replay with exactly the same residuals and counts. This is not a full key/shard.

Proved reasoning:
- [First 400](PriceTwo400.md): no factorization, complete extreme Euler allocations for a single 331 source price; validated with `Certificate2First400.py` test of all 2400 supply/height combinations, no survivors.
- [First 316 price leaves](PriceTwo316.md): fixed-Euler analytic subterminals for exactly `1510189^52` and `1510189^58`, using complete cubic and higher odd orders and LTE at 331. Standalone arithmetic does not close the first without a complete surrounding forest packet.
- Every remaining exclusion in the release table is a frozen split/forest proof, including certified 950-digit and 919-digit primes at the high firsts 382/388. No factorization hints are trusted in replay.

## Isolated verifier

```powershell
$d='Research/AstraFinalAfternoon2400/ThirtyOne'
python -I -S -B -X int_max_str_digits=0 "$d/Certificate2First400.py"
python -I -S -B -X int_max_str_digits=0 "$d/PriceTwo316.py"
python -I -S -B -X int_max_str_digits=0 "$d/ForestVerify.py" --details "$d/Certificate2Followup131.json.gz"
```

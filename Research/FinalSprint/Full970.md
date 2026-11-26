# Registration addendum: (3,970), P3_I00165 — complete

This addendum supersedes the conditional status and 82/84 snapshot of the [first-stage proof](Proof970.md). Additional E3a cell4 and cell8 witnesses cover every source-support atom (6475 and 6811 atoms, five intervals each), with integer minimum net prices 1358262615260 and 1259113258173 nanonats respectively. Both exceed 545·ln(10) nanonats; together with the external base >1855 decimal digits this strictly contradicts N≤10^2400. All atom incidences are reconstructed in the actual 970 model via pairwise gcd; an interval debits every potentially contaminated anonymous support and checks its integer dual branch tree. Previously covered E0/E1/E2, 42/42 internal supports and 40/42 external supports now combine to 84/84 E3 role/support alternatives. No other exponent follows.

From the repository root, run:

```sh
python -I -S -B Research/FinalSprint/Root970.py
```

The wrapper unpacks the [990 prerequisites](Root3x990.zip) and the [full 970 archive](Root3x970Full.zip), then runs `check970.py` in `next970`. This compiles and checks the native sift and calls all frozen and new scope verifiers, not just the final two leaves. The script prints PASS only after all branch checks have returned zero.

For a manual check of just the final two leaves, set `REPO` to the absolute path of your checkout. From `next970` in the unpacked archives, run `python -I -S -B model/Next/Lower/StrictInterval.py "$REPO" 970 2 545 4 8`.

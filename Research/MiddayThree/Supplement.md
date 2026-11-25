# Additional root-three proofs beyond the frozen 20-row release

The base manifest `Release.json` intentionally remains byte-stable (20 actual exponents, eleven whole shards). **Add `(3,96)` once:** `Nested96.json.gz` SHA-256 `7dbc8e15ad6ba143bf539843f4840adbc83f5543d1cdc731ac0d9fd66b702a5f`. This also closes the singleton `P3_I00026`. The original forced prime's exponent-12 branch splits on a second forced prime 76631, using all allowed exponents before 49 plus the ≥49 tail. Every leaf recomputes both geometric-sum forests (and both ECPP routines), with the exact costs required to agree. No new verification code is required for this packet:

```
python -I -S -B Research/MiddayThree/NestedReplay.py Research/MiddayThree/Nested96.json.gz
```

**Joint complete proof `(3,148)`, closing `P3_I00036`.** `Join148.py` runs both independent proof components in isolated interpreters after binding the same forced pivot to the complementary cases: `Complement148.json.gz` (SHA-256 `2739eeb17201a67edc628e081ee793a532c4719da22f5f901fbeff9d7bd2bb5b`) with `Complement.py` certifies f=2,8,10,12 and f≥13, floors 2572,3124,2533,2528,2602; the external `../MiddayTerminal/Leaf148x6.json.gz` (SHA-256 `a306f11dc4c273714d14384bd5bcd5bc7f73869653f1ab76ae6fe821f50080ed`) with `HardRootAudit.py` covers f=6 at floor 2471. `python -I -S -B Research/MiddayThree/Join148.py` passed the full composition offline. This is a single actual, not two.

**Joint complete proof `(3,88)`.** `Join88.py` pins the 25-digit prime `5042939439565996049162197`. For f<41, the forest accounts for 6,10,12,16,18,22,28,40; all other legal values in the prefix are 30 and 36, covered separately. The forest tail covers every f≥41. `Complement88.json.gz` SHA-256 `a946a4dd8aa42d53be1e8811dd125898b835db5eb014000d03f095cbd856895b`, `../MiddayTerminal/Leaves88x30x36.json.gz` SHA-256 `6ca1bab8e1407820e7492de6694c647c98594555760911d5b4175221e4df970d`. Both forest implementations and `Hard88Audit.py` are invoked by `python -I -S -B Research/MiddayThree/Join88.py`: the two exceptional leaves give 2495 and 2610; the weakest forest case gives 2401. Full composition passed cold.

**Joint complete proof `(3,112)` closes `P3_I00031`.** `Join112.py` binds the 42-digit pivot `526256453012063980796131127321354599535039` in both packets: `Complement112.json.gz` SHA-256 `881eb8f3d7450926858cb9597de4d4b84e17663099c710b22afae8ad001a5891`, `../MiddayTerminal/Leaves112x12x16.json.gz` SHA-256 `018c449c70cd7b771206883feb339d27cbabb4db7c550d7422ec2b30e38094f2`. Forest f=4,6,18,22 and ≥23 gives 2553,2508,2418,2471,2898; `RootSlices.py` gives 2635 and 2447 for f=12 and 16. The joint offline command `python -I -S -B Research/MiddayThree/Join112.py` passed all cases.

At the final checkpoint the union is **24 distinct actuals / fifteen whole shards**, or 38 of the original 62 actuals still untouched by these root-three packages. Always merge by `(p,e)` with other directories rather than adding their counts.

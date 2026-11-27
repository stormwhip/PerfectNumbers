# Independent replay of $(13,372)$

The complete replay certifies exclusion of the canonical exact pair $(13,372)$. The frozen ledger assigns this pair as the sole remaining member of `P13_I00073`.

## Complete replay

Candidate `551e1a25f837fdc01121c6b7b0d037d2f217af79`, detached clean tracked checkout, CPython 3.11.9. Complete deep gzip SHA-256 `e8f06dca5cb23a8df0abc45b77cffa0ecf334906aa2042a551746fa7bf742354`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Verify13x372.py
```

Initial invocation (0.516105 s, exit 1) lacked `NightMerge/LatticeLeaf.py` in the sparse worktree, though tracked at the candidate. The reviewer materialized only this tracked dependency (`git sparse-checkout add '/Research/NightMerge/LatticeLeaf.py'`) and left candidate files unchanged. Git blob `56542cce46ace94125ebe3f7b44a4bf197564136` is identical at frozen `49b19bbd` and the candidate. No external factor/ECPP or author cache.

**PASS `EXACT_COMPLETE`, all 25 first fibers, zero OPEN.** Corrected sparse replay 2026-11-27 02:37:22.481–02:40:11.619 +08:00, elapsed 169.2468755 s, exit 0. For the two last leaves: `(10,[3025,9395,9900])`, 11864 interior checks / 11642 empty / 620429 divisions / 0 lattice; `(10,[2774,9335,10151])`, 12454 interior checks / 11975 empty / 2033549 divisions / 240 lattice. No rounded comparison enters the proof.

**Coverage.** Exact canonical root 13 means 19,7,11,31 absent. First pivot and independently reconstructed domain agree across the packets (valuation 1, strict raw tail 78). The union checker requires matching key and pivot, equal domain, disjoint parts totaling 25, disjoint/exhaustive eight masks at valuation 2, and a completely closed first fiber 12. The existing 18+5 complete fibers and first fiber 2 use the same exact root scope. Comparing the complete deep tree to the cold-replayed frontier (same parsed ECPP entries) shows exactly two OPEN leaves replaced by `interior_price`, no reparenting, split/pivot changes or gaps in branch sets; targets are `[0,5]` and `[0,4]`, respectively. The first has no lattice certificate, the second carries 240. Frozen `FinalSprint/Delta.json` leaves exactly `[372]` in `P13_I00073`; no different valuation or divisibility lift.

**Price and CRT.** For an exponent-one Euler prime `t`, exact positive rational `V` gives `t <= floor(B m²/V)`; evaluating numerator/denominator entirely in integers retains equality, and `min(block,upper)` is also necessary for a block divisor. The Euler residue `lo=2m−1` is the least positive representative modulo `4m`. Where `n=e+1` is an odd prime and `n∤block`, an odd prime divisor `t` of the residual block divides the original geometric sum. If `t|p−1`, then that sum is `n mod t`, implying `t=n`, contrary to `n∤block`. Otherwise `ord_t(p)` divides prime `n` and is not 1, so `2n|t−1`. The intersection is empty exactly if `gcd(4m,2n) ∤ 1−lo`; otherwise the canonical CRT multiplier is in `[0,2n/g)`, making `q0` the least positive residue in the merged modulus. Being congruent to a unit modulo each original modulus implies `gcd(q0,mod)=1`. If the source-order premises fail, the code retains the weaker Euler congruence.

**Integer/cofactor windows and lattice.** For divisor `t` and cofactor `k=block/t`, the exact interval is `ceil(block/upper) <= k <= floor(block/q0)` and the cofactor residue is `block*q0⁻¹ mod mod`. Align both ranges before choosing the shorter complete progression; tightening the prime interval using cofactor endpoints cannot lose a real divisor. Too-small/empty intervals only reject infeasible cases. If lattice is used on the prime side, removing every block factor that shares the modulus preserves every divisor in the unit class. Cofactor-side lattice (if used) requires the block already coprime to the modulus. Frozen checker reconstructs centered inclusive index bounds; `K` dominates both ends. Its exact coefficient norm must be strictly less than `first^m`, with every basis value divisible by the candidate divisor to power `m`, forcing an integer root. Exact division and residual Sturm checks include both interval endpoints; any actual divisor root or unresolved witness fails the verifier. All witness keys are consumed exactly once; a missing window is not accepted by assumption.

## Earlier replay stages

The following stages all use the canonical root and exact exponent of the complete replay. Their conditional exclusions are included in the corresponding first-pivot domain above.

### Lead packet

The 18 certified first-pivot valuations leave $1,2,4,6,8,12,16$ in the independently reconstructed 25-value domain. The compulsory pivot is $438552673580231875649$, with incoming valuation one and a strict size tail from 78. The cold replay took 16.862 s. [Original replay record](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/Night2400/Receipts/Review13x372.md).

### Complementary packet

Valuations $1,4,6,8,16$ raise coverage to $23/25$. The proof at 16 covers all eight canonical support masks by seven forests and one strict abundancy inequality. The cold replay took 34.539 s. [Original replay record](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/Night2400/Receipts/Review13x372C5.md).

### Support partition at valuation two

The support masks are $16+32i$ for $0\le i<8$. The two cold replays cover the disjoint sets $\{48,112,176\}$ and $\{16,80,144,208,240\}$. This raises coverage to $24/25$, with valuation 12 remaining. [Original replay record](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/Night2400/Receipts/Review13x372V2.md).

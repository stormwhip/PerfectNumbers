# Two full second-level fibers via mixed exact trees

For an odd perfect `N≤10^2400` with `19∤N`, `v_7(N)=438`, and `v_t(N)=12` at `t=572749682520506652634407616247`, two additional complete second-level fibers are excluded: **`v_27431(N)=10` and `26`**. They are disjoint from both [22](Proof.md) and the [six reserved forests](Reserved438x12.md), and from the root-seven team's `t^10` work. All listed exponents are exact.

## Exhaustive split / leaf checker

Use the same independently replayed Euler rule: `q^1` is the Euler component with `q≡LOW=2t^11−1 mod MOD=4t^11`. At each tree split the certified prime label `z` must be forced in D and outside the Euler class. If `v=v_z(D)`, every possible even g≥v is enumerated. The bare size tail is `X(D/z^v)z^g`; only if all compatible divisors of parent D have been ruled out using the complete Euler cofactor progression may the tail also include LOW. In each child recompute X, all exact sigma emissions, D and demands. Reject direct contradictions, and multiply LOW into the child size only after independently excluding q from that child's D. The output case-key set must equal the regenerated live set. This includes the infinite tail and every surviving child even if a discovery script tried fewer options.

Terminals are either the [reserved forest](Reserved438x12.md) or the [two-target exact price](Proof.md#3-四个活子行全部排除). The latter is unchanged except that an externally supplied ECPP primality checker may authenticate the proven compulsory labels. It reuses the same prices 2/4 at 7/27431 and still uses disjoint effective indices. Ready credit labels below LOW cannot be Euler, and no price method assumes the Euler q external to new sigma blocks until exact cofactors exclude it. Every finite window is checked rather than sampled. No untested high-weight lift enters the price. Anonymous orbit cuts are separate and are not assumed by either tree.

- For h=10, first forced anchor `9188322716316891776727010433305586231` has live g `2,4,6,8,10,12`; additional exact splits use `26254031` (twice on distinct branches) and `91551871`. Four split nodes, 51 price leaves and eight reserved forest leaves.
- For h=26, first forced anchor `426039475024516587313032073` has live g `2,4,6,10,12,14`; all six children are price leaves.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/VerifyReserved438x12.py 10
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/VerifyReserved438x12.py 26
```

| h | Sealed proof data | ECPP | SHA-256 |
|---:|---|---:|---|
| 10 | [packet 10](Reserved438x12-10.json.gz) | 119 | `e60377ca9694c5d7d88c75a1216e6e2622c9d8363f303517ce1f151cc8e542a8` |
| 26 | [packet 26](Reserved438x12-26.json.gz) | 2 | `fc325585a55085567280fdbe9a3bd613384d27aed22266bd62e151582ec435c0` |

This module's nine exclusions (10,12,14,16,18,20,22,24,26) leave `{2,4,6,8}` before any distinct results of the root-seven team. No key or shard credit from this module alone.

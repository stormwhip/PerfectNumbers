# `(19,276)`: complete first-pivot exponent 18

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. If `N≤10^2400` is an odd perfect number with the canonical root `19^276 || N`, then `1176672733^18 || N` is impossible. This is a **whole first fiber**, not an exclusion of the entire key or its shard.

The sole exact prefix is `[(19,276),(1176672733,18)]`. No Euler position is fixed, so all allowed positions, including outside the labelled forest, are retained. The first pivot really divides `σ(19^276)`. Rebuilding its initial exact domain finds 70 live valuations, strict raw tail 188. The frozen 64-case packet leaves `[1,2,8,16,18,28]`; this packet alone removes `18`. No historical forest is imported to prove this new fiber: the cold replay only checks the archived first-domain bookkeeping against it.

The certified forest has six distinct roots and 551 subordinate ownership edges (39 matched ECPP labels). Among the mandatory roots, `2395723558714191605903463333646981101789939140815259939` divides `σ(1176672733^18)`, and the newly authenticated 102-digit prime `720115882406222085965068726893873898633343366787816797352202677324108536240208081709751502952901480917` divides the former's geometric sum at exponent 2. It is used only when an actual parent emission activates that edge. All forest rules are those documented in [Forest222.md](Forest222.md), including a single Euler exception, finite heads with unconditional monotone bare-power tails, and no duplicate charge of mandatory root values or outside support.

The [verifier](VerifyFirst18.py) replayed the two independent integer forest recursions on the same certified forest; both give a strictly sufficient lower bound with diagnostic decimal floor **2412**. The [packet](First18.json.gz) SHA-256 is `d38b7f915e9f3110683b2a6117670c6a7a2c5c708d01e1a7b8aa27ddad537547`.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyFirst18.py
```

Isolated replay exited 0. The narrower [Even276](Even276.md) exclusions under `t^18`, [E18Upper](E18Upper.md), and the independent `R^1` alternative are entirely subsumed by this direct theorem; do not count them as additional first fibers. Separately the joined `t^1` packet may close one other first fiber; if accepted jointly, this leaves `[2,8,16,28]` at this key. The disjoint `t^1` arithmetic is not used here. No withdrawn [PR #11](https://github.com/stormwhip/PerfectNumbers/pull/11) claim is used.

# Independent acceptance: exact `(7,438)` and `(7,12)` subtrees

Freeze `495c59f55456a70994ce7848487e0c4e262c1984`. For odd perfect `N≤10^2400`, assume canonical root 7, so `19∤N`. Accept only the following **27 pairwise distinct conditional exact prefixes**:

| Root key | Already fixed exact components after 7 | Additional exact exponents excluded |
|---|---|---|
| `(7,438)` | `572749682520506652634407616247^10` | `v67=130,132,134,136,138,140,142,144,146,150,152,154,156,158` |
| `(7,12)` | `Q^12,T²`, `Q=16148168401`, `T=σ(Q^12)/13` | `v3453283=10,16,22` |
| `(7,12)` | `Q^42` | `v173=160,162,164,168,170,174,178,186,188,194` |

The first list is within the frozen `2..158` even list except 148 ([arithmetic source](../../FinalNight2400/SevenNext/Mixed67Proof.md)); the two `(7,12)` lists are inside the 30 and 86 active values audited in the frozen chain ([report](../../FinalNight2400/Report.md#L30-L36), [result ledger](../../FinalNight2400/Results.json)). They are not closures of the preceding components or the keys. The map and key totals do not change.

## Legal branches and arithmetic

1. Independently reconstruct the exact prefix with finite sums and `lcm(X,odd(σ(X)))`. A forced pivot requires positive valuation from the known emitted product. Divide its existing emitted power out before multiplying its actual component to bound the tail; use `<= B` at the inclusive endpoint. The packed split at `v67=156` has three live children and first raw overflowing exponent 23. No assertion that a supplied child list is complete is accepted without comparison to regenerated cases. Higher tails need no factoring.
2. For `Q^12,T²`, `σ(T²)` forces 3 and `σ(Q^12)` forces 13. If 5 occurs, the exact rational bound using `7^12·3²·5` exceeds 2. If 11 occurs and `v3≥4`, the bound from `7^12·3⁴·11²·13` exceeds 2. If 11 occurs and `v3=2`, `σ(3²)=13` **adds** an inflow to that from `Q^12`; using `7^12·3²·11²·13²` again exceeds 2. Since 3 is compulsory and ordinary, these exhaust its possibilities. In the other two domains the only ban is 19.
3. Reviewed the [frozen forest evaluator](../../Nov25/Compose/Compose.py#L54-L141) and [second arithmetic evaluator](../../Night2400/A/MaskedForest.py#L6-L59) on the issued scope. Root charges come from the independent stripped fixed output, and child labels are outside its support. An activated child has a single source parent; terminal anonymous emissions are stripped of fixed, prepaid and candidate supports and come from distinct exact components, so their product divides the available odd sigma product even if some anonymous factors overlap. Actual exponent choices follow ordinary and eligible Euler arithmetic progressions; every tail is bounded by a monotone bare power. At most one activation may receive an Euler reduction; Euler outside the forest is included by the all-ordinary mode. If Euler is fixed by an exact prefix, no Euler discount is available at any vertex. No Hensel enumeration, floating lower endpoint, or guessed cofactor prime is used.

## Separately accepted second packet

[Forest438b](../Seven/Forest438b.json.gz) adds exactly the 37 listed exponents in [the proof table](../Seven/Proof.md#L9-L16). All lie in the original frozen active list, and their intersection with 438a is empty. The same independent domain reconstruction and both integer recurrences passed: 37 strict terminal forests, no nested split, and 515 validated ECPP labels. The weakest scaled lower bound is `3227368>10^6`. Thus 51/78 values of the `t^10` sibling are excluded jointly; this count does not close the sibling or the key.

## Actual replays

```sh
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/VerifyForest.py Research/AstraFinalAfternoon2400/Seven/Forest438a.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12a.json.gz
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Audit/CheckSevenForestDomains.py
```

Both exit 0. The first command cold replayed both exact integer forest recurrences and all certified bases in 7.169 s. For the 438 packet it verified 16 forest leaves and 125 ECPP labels; for the 12 packet, 13 forest leaves and 253 ECPP labels. Strict per-leaf comparisons passed (in the 438 split the weakest scaled integer lower bound was `floor(10^6·LB/B)=199604667`). The second command imports neither applicant nor historical code: it binds the two certificate hashes, independently proves the exact active branches, validates scope-specific bans, and reconstructs roots, ownership, and the reached large-label roster. It does not claim a third independent ECPP or forest arithmetic implementation.

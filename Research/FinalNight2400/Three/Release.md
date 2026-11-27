# Root-three audit handoff (baseline 1447d41b)

**Priority first-pivot result.** At v3=12, v797161=66 is impossible. The historical 96/97 secondary siblings and the one new missing 5897^6 sibling have both been freshly cold-replayed in this session. New sibling is exhaustive: 294 splits, 7,916 forests, three special arithmetic terminals, 3,578 ECPP, no missing node. The remaining primary valuations are 1 and 96, hence **no root-key or shard closure**. See [complete proof](ProofR.md), [same-emitter lemma](ProofHard66.md), [cold driver](Complete66.py), [new packet](WholeR.json.gz). Run from checkout root:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/Complete66.py --replay-old

The --replay-old option is not a whole-history replay. It adds only the specific required Fiber66 witness. New receipt: 7916 forests, 294 splits, 3578 ECPP, 1 each hard, pair and four-parity. Historical: 644 forests, 13 regular splits, one supplier split, 8 order-budget, one joint-valuation, 5338 ECPP. New SHA e7a078323af59eb79f0ff1c82b10de2aad62e7e2c3340e50d7d8bd735ad65beb. Distinct fallback [atom tradeoff](ProofAtoms.md) on the two open h102,108 subpaths of v797161=1 proves lower bounds on anonymous internal suppliers; no completion credit.

**Overnight update:** [the second tranche](ProofNext.md) and [full fixed-Euler first 1](F1Handoff.md) supersede the original first-pivot counts and h1 partial below. All firsts 1,5,8,16,18,22,96,102,106,126,130,148,166,180,190,192,196,226,240,250 have been cold verified. Therefore among the original 182 live primary valuations, **179 are excluded, leaving just 2,156,256**. See the [156/66 reverse-price proof](Inv156Proof.md) for the further partial reduction under the middle first.

**Original first-tranche full results.** At v3=6, v1093 cannot be any of 16,18,22,96,126; all were among the 23 historically open. Totals 164/182 excluded, 18 remain. [Proof](ProofFullSix.md), [verifier](Full.py) and Full{16,18,22,96,126}.json.gz are the release inputs. The f126 proof needs GeneralPair.py, whose stock historical cap_two helper and Hensel enumeration are shared with the f66 proof. The five complete proofs respectively contain 141,31,116,81,396 forests; 8,2,8,3,28 nodes; 439,202,176,319,635 ECPP; three nonforest pair leaves only at 126.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/Full.py 16 18 22 96 126

**Low exact subbranch.** The older 132/160 and 148/160 checkpoints are fully superseded by the [complete 160/160 proof](FirstOne.md). Intermediate forest discovery packets are not required in a release checkout.

    python -I -S -B Research/FinalNight2400/Three/Six.py
    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/JoinOne.py OneComplete.json.gz
    python -I -S -B Research/FinalNight2400/Three/AtomTradeoff.py

**Reviews for other owners.** [Global support](SupportReview.md), [four 19^618 credit fibers](CreditReview.md), and [19^618 nested anchor f16,14,12,10](NestedReview.md). The presence of exploratory scratch packets, native logs or unsealed D*.json.gz in this folder means nothing for acceptance: they are not proof dependencies.

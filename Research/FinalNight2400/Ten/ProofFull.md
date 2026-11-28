# Full exact reduction: (19,58), singleton P19_I00015

**Theorem.** No odd perfect N ≤ 10^2400 has 19^58 exactly dividing N. In the 1447d41b baseline [shard map](../../GeminiFrontier/ShardToKeys.json) this eliminates the sole key of P19_I00015; it appears nowhere else. This is one full key and one shard, not the global 2400-digit bound. No reduction of any other v₁₉(N) is claimed.

## Complete union

1. Write Q=σ(19^58) and T=(Q+1)/6; both are certified primes. The [first-fiber receipt](../../Night2400/Receipts/Review19x58.md) gives exactly eleven viable Q valuations 1,2,4,5,6,8,9,10,12,13,14 and excludes all but 1. At Q¹ the Euler slot is occupied and T is forced.
2. The [C10 receipt](../../Night2400/Receipts/Review19x58Low.md) partitions the T valuations; its live list is 2,4,6,8,10,12,14. Every explicit non-null leaf is rejected. Its eleven old nulls have the following partition: two at T², eight at T⁶, one at T¹⁰. The [reviewed T¹⁰ proof](../../GeminiFrontier/VerifyT10.py) rejects the latter. The [new T² proof](ProofTwo.md) rejects both its leaves at their common prefix by abundancy.
3. Let U=3291622576015727423. Of the eight T⁶ nulls, [ordinary twofold prices](ProofSix.md) reject all three under U¹² and both under U¹⁶. The three others are listed below; [the weighted verifier](VerifyWeighted.py) rejects all of them. This accounts for the *exact* null set rather than merely its cardinality. Hence the Q¹ fiber closes, as do the other ten Q fibers, proving the key.

|T⁶ continuation (W=48650484525259)|Witness|Explicit terminals / splits / exhaustive tails|Smallest floor(log10 bound)|
|---|---|---:|---:|
|U¹⁰|[3](Weight3.json)|1/0/0|2675|
|U⁶,W¹²|[9](Weight9.json)|1/0/0|2576|
|U⁶,W⁶|[10](Weight10.json)|29/15/15|2400 (strict >10^2400)|

## Weighted valuation and completeness

Use the notation and forced-base rules of [the unweighted proof](ProofSix.md), but give U weight w_U=6 and every other non-Euler fixed target weight 2. The choice was motivated by order 7 modulo U; **no presumed order exclusion is needed**, since all possible orders are enumerated. Set H=Σw_p. For each unseen exact r^f let m_w(r,f)=∏p^{w_p v_p(σ(r^f))}, and let M_w=∏p^{w_p c_p}. Now N=XM_w∏(r^f/m_w(r,f)), identically. Assign E_r≥max(1,m_w(r,f)/r^f) over admissible f; starting lower bound V0=XM_w/∏E_r. Every distinct compulsory r contributes the additional net factor E_r times a lower bound on r^f/m_w(r,f). This accounting is valid even if r is one of the exceptional suppliers; E_r cancels exactly once.

In [Weighted](Weighted.py), for 2≤f<H the CRT table enumerates all target orders and levels as before, but the cutoff is the product of their *individually weighted contributions*, not a uniform power. Each progression is exhausted until r^f is at least the cutoff. In the high-f loop the single-target cutoff uses **H times the valuation**, uniformly for each target. This is sufficient because if r^f≥p^{H v_p} for every p, raising each inequality to w_p/H and multiplying gives r^f≥∏p^{w_p v_p}. Contraposition covers every deficient candidate. The Hensel/valuation/cap/LCM/primality exclusions are those in the unweighted proof. For forced components the tail uses r^f/M_w, so the minimum over every even exponent is rigorous. This is not a heuristic extension that only changes the numerator without changing the search windows.

All three certificates are checked on the very same prefix, roots prime, and all descendants verified distinct new factors by exact divisibility. For the last tree, floor 2400 is **only a display truncation**; every terminal and tail passes an exact fraction >10^2400, with equality rejected. Raw decimal approximations are not used for decisions.

## Offline replay

From repository root, standard-library CPython 3.11, no approvals, factorization, network or third-party packages required:

~~~text
python -I -S -B Research/FinalNight2400/Ten/VerifyFull.py
~~~

[VerifyFull](VerifyFull.py) pins the historical first and second packets, checks the union and shard incidence, then replays the two first-pivot checks, C10, historical T¹⁰ arithmetic and all three incremental verifiers. With `--incremental` it deliberately skips those first/second historical tree replays (but still checks T¹⁰), and explicitly labels that mode. The claims in this report concern only the exact bound B and key given above.

# Canonical (3,6): certified exact secondary exclusions

Assume N is odd perfect, N≤10^2400=B, v_3(N)=6, and 19,7,11,31,13 are absent. σ(3^6)=1093, prime. The historical [wave-four report](../../FinalSprint/LowBranches/Wave4/README.md) leaves 23 exact exponents of 1093 including 1,16,18,22,102,192. Our claims are conditional on those exact values; no divisibility lift, full root exponent or shard closure.

**Euler 1093.** If v_1093=1, σ(1093)=2·547 forces 547 and all unassigned components have positive even exponent. For each candidate even h=v_547(N), set X=3^6·1093·547^h, S=σ(X)/2, D=S/gcd(S,X). Necessary conditions are gcd(X,D)=1, no forbidden factor in D, XD≤B, S≤X. X itself exceeds B at h=876 and thereafter. The verifier gives 160 survivors, maximum h=436. The unassigned ordinary components r^f satisfy ∑u=h−1, where u=v_547(σ(r^f)), since the only fixed supply is from 1093. For an unseen prime r define E_r≥max(1,547^(2u)/r^f) uniformly across all these h. Thus N≥X·547^(2(h−1))/∏E_r.

To compute the product safely, write q=547. Only even f with 5^f<q^(2·436) can lose mass, because 3 is fixed. If r≡1 mod q, u=v_q(f+1). Otherwise let k>1 be its order mod q; it must divide gcd(f+1,q−1) to supply anything. Then u=v_q(r^k−1)+v_q(f+1) by LTE. Enumerate all such exact-order root classes by Hensel lifting through the residual cap, scan positive representatives with r^f<q^(2u), and recompute exact capped valuations before updating the loss. The derivative k r^(k−1) is a unit. Small prime factors, impossible forbidden outputs, and failed Fermat tests only remove impossible prime rows. Over-included composites do not strengthen the price. The scan returns just one discounted base. The rational strict threshold excludes all 52 live h≥294. Check independently with

    python -I -S -B Research/FinalNight2400/Three/Six.py

**Disjoint forests.** The second verifier re-derives the compelled secondary pivot in each row (the largest new one in the f=22 row is 59 decimal digits), enumerates the complete exact candidate interval with its direct filters, and checks the specifically claimed leaves, never treating missing branches as excluded. Each forest root divides D. Owned children activate only when their unique parent emits them, owned primes are excluded from the anonymous outgoing blocks, and the one global Euler slot is assigned at most once. Both old independent integer forest recursions are run with head 96 and a monotone full tail. Elliptic primality chains are recursively checked to deterministic 64-bit termini for all large roots and children. Strict size >B is tested directly. The verifier prints exact pivot identities and lists of valuations.

| v1093 | live secondary | forests | exact secondary excluded |
|---:|---:|---:|---|
| 1 | 160 | 37 | 37 disjoint below h=294; with the 52 priced, 89/160 |
| 16 | 14 | 7 | 6,13,16,21,24,25,30 |
| 18 | 11 | 6 | 13,25,28,30,33,36 |
| 22 | 7 | 3 | 6,16,18 |
| 102 | 9 | 2 | 14,22 |
| 192 | 10 | 2 | 20,26 |

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/VerifyForests.py

No factor database or discovery tool is needed for either replay. Total 109 exact secondary subbranches (52+57). All six first-pivot fibers remain open.

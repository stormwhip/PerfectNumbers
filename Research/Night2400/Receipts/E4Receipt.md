# E4 complete root-seven 420 — independent reviewer-a receipt

## Provenance and replay

Candidate `78744f67339140524e96fdceaa4b9bdb4b310af4`, initially clean and detached in `E:\PerfectNumbers-Night2400-reviewa`; sparse excludes only `Research/NightOrder/ECPP/`. The author candidate lacks `Research/Night2400/VerifyFibers.py`. The only non-receipt addition is that file, byte-materialized from integration `850bee532621cdf5aca0fea142ef4364015007ad`, Git blob `851e597b656f8c0db640e07409d7aebee7b86742`, and checked with `git hash-object --no-filters`. Its transitive repository dependencies (PivotCheck, Compose, ForestReplay, PrimeCheck, JointValuation) are identical across the two commits. No authored caches, external prime index, reserved ECPP tree or third-party packages were used.

SHA-256:

```text
0425676e7b43125d1b1369b9dba1b128347575ddabb6d0caeacc2428c4ef97d0  Research/Night2400/E4/Fibers7x420Complete.json.gz
6e5d4c19f0b353f5a80998e120fe6b00c7f5dc285c42a241461f762db1987b6c  Research/Night2400/VerifyFibers.py
7912ce7b43c60de736793b71500d0608e08e733d28cc55b3ff82acfe7383a115  Research/FinalSprint/JointValuation.py
ff47c354d6e5c47f6daff26bdd37b3b2922ff1cfcc0ce6af91487432f9a0c4e2  Research/Session20261126/Delta.json
52ffca5524c51b4b3f98ad0534a6c974fe3165f5b5d9996410ebc2253f56aa03  Research/Night2400/Receipts/E4DomainAudit.py
69b4ffec7a174f4285943e09ee8f2fa2afe039df327a5573b59d84d0f7304ad7  Research/Night2400/Receipts/E4PriceAudit.py
5eb2bae91c6af467329d19929cd3c19c8a882de925e0ab2a81e957d9d70f6d2b  Research/Night2400/Receipts/E4Domains.txt
```

From root, with Python 3.11.9:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E4/Fibers7x420Complete.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/E4DomainAudit.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/E4PriceAudit.py 22
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/E4PriceAudit.py 6 30
```

Cold run UTC+08:00 2026-11-27 02:37:55.5320414 → 02:40:56.6250339, stopwatch **181.083618 s**, exit **0**. Verifier returned `key=[7,420]`, `domain=covered=[2,4,6,10,12,14,16,18,20,22]`, `open=[]`, `first_out_of_size=48`, `counts_forest_split_direct_price=[1076,30,1119,2]`, `price_receipts=[[18,[36827,38953,0]],[0,[8,0,14]]]`, and the matching packet SHA-256 above. Packet has 6,730 ECPP chains; verifier requires all supplied chains to be used.

## Independent scope, domain, and tails

The frozen baseline's remaining-shard list contains exactly one shard admitting actual exponent 420 for canonical root seven: `P7_I00081`, index 81, `remaining_actuals=[420]`. The root scope is `v_7=420`, `19∤N`, odd perfect `N≤10^2400`; no divisibility lift and no root-19 credit. [Independent domain transcript](E4Domains.txt) derives the forced outgoing component divisors from raw sigma products, independently verifies each exact sibling key, and proves each monotone tail by consecutive integer budget inequalities. It completed with exit 0, stopwatch 0.868250 s, UTC+08:00 2026-11-27 02:39:28.5824028 → 02:39:29.4596066. It does not import candidate modules; forest and ECPP arithmetic is checked in the cold run.

First pivot `Q=1169407471026387018305554817094515359` has valuation 1 in `σ(7^420)`; budget tests exponents 1–47, tail begins at 48, and exact live exponents `[2,4,6,10,12,14,16,18,20,22]` all have corresponding certificates. Independently counted 30 inner splits, 1,076 forests, 1,119 direct contradictions including root, and two price leaves. The deepest cited pivot `284860058207025151` has exactly even children 2–22 and size tail from 45. This gives one exact root exponent and one unique remaining shard, subject to integrating this proof against the stated baseline only.

## Two independent price replays

The second fixed pivot is `R=120298224779693`. The replay script imports no candidate code: lifts just the subgroup generator with modular Newton doubling, enumerates primitive powers, uses CRT on all constrained coordinates for small exponents and a one-coordinate weighted bound for large exponents. It rechecks exact capped valuation and excludes only demonstrably composite relaxed bases; it uses one maximal rational loss per base. For the exponent-one Euler windows, it rechecks the exterior integer lower bound, and the interior progression using `2m−1` as its own inverse mod `4m`; the residue-theoretic block skip follows quadratic reciprocity. Both prefixes have only even fixed exponents, so Euler remains unrestricted until partitioned. Primality of fixed bases comes from the cold run. UTC+08:00 on 2026-11-27:

| Exact prefix after `(7,420)` | Targets | Remaining valuations | Exceptions | Euler windows | Stopwatch seconds | Clock start → end | Exit |
| --- | --- | --- | ---: | --- | ---: | --- | ---: |
| `(Q,22)` | `Q` | `[21]` | 0 | `[8,0,14]` | 6.034590 | 02:40:31.3008773 → 02:40:37.3455649 | 0 |
| `(Q,6),(R,30)` | `7,Q,R` | `[420,5,29]` | 18 | `[36827,38953,0]` | 122.195388 | 02:40:31.3563462 → 02:42:33.5644725 | 0 |

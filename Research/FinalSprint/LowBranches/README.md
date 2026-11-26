# Twelve additional first-pivot exclusions (wave 1)

Let N be an odd perfect number at most 10^2400 with canonical root 3 (none of 19,7,11,31,13 divides N). At v3(N)=6, sigma(3^6)=1093; at v3(N)=12, sigma(3^12)=797161. Both are prime. The following exact valuations of the corresponding forced prime are impossible:

|v3(N)|compelled prime|newly excluded exact valuations|historical exclusions|combined exclusions|remaining|
|---:|---:|---|---:|---:|---:|
|6|1093|21,30,33,36,46,52,60,120,150,222|142|152/182|30|
|12|797161|46,106|90|92/100|8|

**Neither root exponent nor canonical shard is closed.** All cases are disjoint from the pinned historical LowBranches packet. The domain is all size/Euler/admissibility-compatible exponents after the original initial contradiction tests; the exclusion numbers are not the numbers of raw integers up to a size limit.

Run the two standard-library checks from the repository root:

```
python -I -S -B Research/FinalSprint/LowBranches/Verify.py . Research/FinalSprint/LowBranches/Branches.json.gz
python -I -S -B Research/FinalSprint/LowBranches/Delta.py .
```

`Verify.py` exhaustively splits each specified primary fiber. Each certified leaf builds a graph of actual-divisibility forced components, validates all imported labels with ECPP chains or deterministic 64-bit primality, and passes both integer lower-bound recurrences (`Compose.Forest` and `PivotCheck.exact_leaf`). Unlimited exponents and the unique Euler exception are covered by these established routines. At a fixed component a known divisor exceeding its exact valuation, excess abundancy, a forbidden factor, or size above 10^2400 is a genuine contradiction. The underlying graph is a discovery witness, not a factorization assumption. Local ECM was useful in breaking the exceptional v797161=106 leaf: divisors of sigma(314801379535122745392309983684197278767041^10) include 12388949,15774991,175742579,463399026006929,7299671561324862618911,11258825351027604261407. Independent checker rejected four preliminary leaves of the v797161=46 tree before exact-guided repair. No paid API or network is needed for replay.

The frozen packet (1,091,272 bytes; SHA-256 `f9545a514eb6db321302d5090663b42d108babcf1497a9a0f780df3c4c604fc6`) uses 1,618 distinct bound ECPP labels. The 12 rows (in table order) have forest leaf counts 1,3,1,1,1,1,1,1,26,24,442,59; complete split counts 0,1,0,0,0,0,0,0,3,3,20,10; minimum floor(log10 N) 2412,2400,2428,2406,2569,2403,2431,2406,2405,2401,2400,2401. A floor 2400 is accepted only after the strict integer comparison proves N>10^2400. Delta.py checks both frozen hashes and prints all surviving obligations explicitly.

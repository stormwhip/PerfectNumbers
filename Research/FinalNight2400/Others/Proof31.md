# Complete canonical exact exponent (31,310)

Suppose N is odd perfect, N<=10^2400, 19,7,11 do not divide N, and 31^310 exactly divides N. The certified prime q=5691933643219 divides sigma(31^310) at valuation one; since sigma(N)=2N, q must divide N. Exact enumeration has 26 live exponents f, with 25 direct contradictions, 65 incompatible valuations and a strict raw size tail starting at 117. Four disjoint groups of packets cover the domain:

| Source | First exponents |
|---|---|
| Historical Fibers31x310 | 2,10,12,14,20,22,24,28,30,32,34,36,38,40,42,46,48,50,52,54,56 |
| Historical C12: Minimum31x310 and Fiber16 | 6,16,58 |
| New Root31x310F18 | 18 |
| New Root31x310F4 | 4 |

First 18: forced r=707818236468853019281602309439653890995043, all four live exponents 2,8,10,12 have strict outgoing forest bounds. SHA256 680539a9f43d372b26816eab8a110e741db2ba2c5b461418bb270d9c3986374d; 502 ECPP chains.

First 4: forced r=512738348529648177663331017165682915269207241, all eight even exponents 2 through 16 covered. Last difficult exponents 6,10 give decimal floors 2408,2417 with two separately implemented strict lower-bound recurrences. The packet contains 50 terminal forests, 8 internal splits (not counting the first), 89 direct contradictions (including the root siblings), zero open, and 1221 ECPP chains. SHA256 78a4177a7ca376d9294f810beb822f2c78f2c10c1534c9d58ad65bc7fefd25e4. A partial development packet of a different hash is not part of this result.

Cold replay from repository root with standard Python, no network, no discovery tools:

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Others/Full31.py
~~~

The checker recomputes each historical receipt, verifies exact equality and disjointness of the combined domain, requires both new packets to have no internal OPEN node, and recomputes every required prime chain and integer forest bound. A complementary data-only exact partition can be reproduced by running Research/Night2400/Receipts/FiberPartition.py on each new packet. The historical Night2400 ShardToKeys and KeyToShards maps identify P31_I00062 as having exactly this one remaining exponent; therefore the closure supplies one new canonical shard, not 26. No divisibility lift or exclusion of N outside the canonical class is claimed.

# Complete canonical 7^36: exact forest union

Assume N is odd perfect, N≤10^2400, 19∤N, and 7^36 ∥ N. σ(7^36)=223·2887·4805345109492315767981401; the last prime q is compelled with incoming valuation one. Its exact first exponent f has 31 compatible live values, raw size tail 96. Two independently accepted historical packets cover 24 + 4 firsts, the second exactly {1,4,6,18}. Their disjoint remainder {2,12,16} is covered by three new standard stock packets. No mask projection, incomplete discovery tree, unproved factor hint or divisibility lift enters this full proof.

| New first | Terminal forests | Internal splits (not counting the first-domain split) | ECPP chains | Compressed SHA-256 |
|---|---:|---:|---:|---|
| 2 | 207 | 10 | 3200 | 24a9dcdd2a557ae9b2644196d79547300df0e124aca092715f1393fa5e2f784f |
| 12 | 230 | 4 | 5636 | 7c2c330187077dffc61c9998f9dac5b469ec0c56f97f01e73c3beb67cb3b4236 |
| 16 | 113 | 1 | 2124 | 225a7d03320844e9b49ae031a7b64e011fa789ab4ba25e6e7c3f35ea2104259e |

First 2 used forced 194307774563247050351722816730060368686862477 with all 17 exact secondary exponents. Its initially hard exponent 10 splits on 5659, with its low child 2 finally handled by a strict canonical forest, not an Euler-placement hypothesis. First 12 uses the already compelled 2887, exactly 128 live even exponents; the most difficult child 2 required a 9,000-plus-edge forest. At 16 and 88 where a direct forest is not needed, one can use the complete extra splits in the packet, including the 73-child split at 223. First 16 also splits on 2887, proving all 113 live children, raw size tail 456. Validated local forests use only data-carried witnesses, rebuild their compelled roots and single-parent graph, check prime64 or elliptic primality chains and enforce two separate exact strict lower bounds. Floors of 2400 do not replace the integer comparisons.

The frozen historic primary packet SHA-256 is 9880c5fd9846aab21f995c57360430d57adfdacc8774e9d3a9cce0ed56ef67d6. The E8 four-first packet SHA-256 is 5ae6d109c9c4440db0bd4c4a71e07f59b921e87f97f3b162c7cb7ae1af1d3227. Full36.py replays both plus Seven36Two.json.gz, Seven36Twelve.json.gz and Seven36Sixteen.json.gz. It insists the five domains equal one another, verifies the three singleton first sets and disjoint complete equality to the historical domain. Standard CPython only:

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/ShortSeven/Full36.py
~~~

Complete isolated Full36.py replay returned exit 0 in 2009.394 s (epoch ms 1795814328651–1795816338045), reporting all 31 firsts and P7_I00011. The frozen shard P7_I00011 has singleton remainder [[7,36]]; the complete disjoint union certifies one canonical shard, not 31. Standalone FiberPartition.py reproduced the final primary first12 tails 96,513,32,88,296 with no internal open path, 230 forest leaves, 267 direct/489 incompatible, and 5636 ECPP labels. Earlier partial FirstCheckpoint and SecondCheckpoint are not part of the complete union.

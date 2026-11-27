# FULL canonical (7,430), P7_I00082 — complete cold receipt

The complete isolated command below finished with exit 0 in 1342.762 seconds wall time (UTC epoch milliseconds 1795795629821 to 1795796972583). The check performs both historical C3/G5 replays and all three new first-valuation proofs. It uses only stock Python and immutable historical arithmetic, no network or native factoring software.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Seven430/Full430.py
~~~

* Raw first-pivot domain: v_Q even 2,4,…,16. The first monotone tail starts at 36. C3 discharges firsts 14 and 16; G5 discharges 6,8,10 and returns open masked paths exactly where advertised. Across all 64 canonical support masks, the Q² remnant is five exact cells.
* Q² five cases: (mask,z-exponent,viable Euler identities,remaining exact-exponent replacement forests) = (50,2,35,26), (58,2,38,17), (178,2,41,12), (50,6,26,17), (58,6,23,14). Every complementary Euler class and every exponent of those identities is covered. See Proof2.md.
* Q¹²: all eight w exponents [1,2,4,5,6,8,9,10] excluded by simultaneous cubic prices and forced emitter bounds. See Proof12.md.
* Q⁴: 30 complete pivot splits, 529 strict forest leaves, one fixed-Euler three-target price and one exact nonsquare obstruction, zero open. Its exceptional nonsquare branch has six compulsory pairwise-coprime nonsquare blocks with no factors ≤1000, forcing five uncompensated distinct primes in a budget of 10368506209179. See Proof4.md.

Final stdout: **FULL canonical exact 7^430, P7_I00082, every first Q valuation 2,4,6,8,10,12,14,16; no mask holes.** Exactly one new canonical pair and its singleton shard; no divisibility lift. The archived generic G5 “open” lists describe its own partial historical output, not the final union.

The minimal 24 new proof inputs (including three explanatory notes and all eight JSON proof/certificate assets) and their per-file SHA-256 values are listed by Inventory.py. Primary packets: Q2J2.json ad63fd1db54c8eae36653c4359bf4f901ba812120729680b2197b7c4b8340844, Q2J6.json 9d0c0131368f2fb33e86c0cead69c5ec81202b918a04bce60c78a42cd8f363c3, Packet12.json cdcdfadb8e276ad6af0981040e6073f08896c930a97a03dbdcaf4c0ea18b48d5, Pack4.json 74e6c9c8f3afc590bab30a6e3adc6c0c87aeccb0f5bad3a9e269cb1160ca52dc. Historical packet C3 and G5 are checked directly, not trusted based on hashes. No guessing or negative factor-search result is used in the proof.

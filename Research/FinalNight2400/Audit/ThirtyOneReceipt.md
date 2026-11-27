# Independent full-key audit: canonical (31,310)

**Accepted** for odd perfect N ≤ 10^2400, v₃₁(N)=310, and 19,7,11 ∤ N. This is not an unconditional exclusion of v₃₁=310 outside that canonical root. Both frozen Gemini maps were parsed independently: this key occurs only in P31_I00062, whose sole member it was. Credit one full canonical key and exactly one shard.

[Integrated cold checker](../Others/Full31.py), SHA-256 c23307dae0600aa160f23635cca13d9c6ee756d4d57b15407f8041b0a56bf116; independent run exit 0 in **63.005 s**. [Transcript](FullThirtyOne.txt). Replays original first-domain certificate, full historical C12 first 6,58,16, and both new complete first 4,18 packets. In particular it does not simply add results from the partial historical first-4 and first-18 packets. The prime pivot is 5691933643219, 26 live firsts, 25 direct contradictions, 65 illegal, raw size tail 117. Code checks equality of regenerated root domains, disjointness of the 21+3+1+1 complete sets, and emptiness of open descendants. For historical 16 one hard child uses all sixteen possible masks, not just a projection.

[New first 4](../Others/Root31x310F4.json.gz), SHA-256 78a4177a7ca376d9294f810beb822f2c78f2c10c1534c9d58ad65bc7fefd25e4: separately reran [independent geometric-sum domain reconstruction](../../Night2400/Receipts/FiberPartition.py), 0.216 s. Nine splits including root, tails 117,33,41,30,50,50,22,58,14, eighty-nine direct, 234 illegal, 50 forest endpoints, 1221 ECPP entries, **no first-4 open child**. Each endpoint is checked by the unmodified historical arithmetic verifier in the full run. [First-18 receipt](OtherReceipt.md) independently records another strict four forests and tail 26. No incomplete branch, repeated first, or partial mask credited.

~~~sh
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Others/Full31.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/FinalNight2400/Others/Root31x310F4.json.gz
~~~

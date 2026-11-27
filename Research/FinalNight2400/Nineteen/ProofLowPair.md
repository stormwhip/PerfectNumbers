# r^14 and r^16 excluded under the last t fiber of (19,282)

N odd perfect, v_19(N)=282 and v_1735317810514627(N)=10. For r=8383027, two additional disjoint exact second valuations, 14 and 16, are excluded. These are applications of the [same strict outgoing-forest proof](Proof282.md); local cyclotomic factor discovery was used only to propose additional prime labels, each tested by ECPP or deterministic 64-bit arithmetic. The sealed verifier reconstructs r's 50 directly live powers, tail 202, then replays both entire represented subtrees. Complete union: two interior splits, 18 terminal forests, 39 ECPP chains. Both integer lower bounds are required to exceed B on every terminal. With earlier additions this is 32 of 50 initial r powers, leaving 18. No complete first-pivot or root-key claim.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyLowPair.py

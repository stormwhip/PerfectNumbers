# Complete canonical exact exponent (31,352)

Within the canonical class 19,7,11 absent and odd perfect N≤10^2400, 31^352 ∥ N is impossible. The forced prime is q=1797674429773, with v_q(σ(31^352))=1. The first split has 31 live exponents, 33 direct eliminations, 47 incompatible exponents and strict size tail 112. Its disjoint partition is:

* Historical C8: 2 by all sixteen support masks; 4,6,10,30,33,45,48,50,54 by complete trees; 25,37,38,40,42,46,52 by prefix incoming price (17 exponents).
* New ThirtyOne352Thirteen.json.gz: 12,13,14,16,18,20,21,22,24,28,32,34,36 by thirteen direct outgoing forests, each recomputed twice with strict >B. Compressed SHA-256 c83ed8210c73de47d04232334f4b0be9284fbc2988439f940c67b4358b1fc032.
* New ThirtyOne352One.json.gz: first 1, the fixed Euler case, compressed SHA-256 48705e23207216c6a89269270b356e92d3215d2c686fa522f3531bc3b12849e3; 352 ECPP chains.

At first 1 the odd part of σ(q) is 151·5952564337, and the latter z is forced at valuation one. The node recomputes the full split including all direct siblings and monotone raw tail at 138. Exactly 24 children survive: 2,6,10,12,16,18,20,22,28,30,32,36,38,40,42,46,48,50,52,56,58,60,66,68. For 23 children the packet gives ordinary exact forest certificates; the fixed Euler row bars a second special component. At z-exponent 30, the frozen prefix-price checker excludes simultaneous deficits in targets [0,2] with receipt (25,[0,0,0]): 31 and z receive zero and one units from the fixed sigmas, hence their demands are 352 and 29. There is no unassigned Euler window. No OPEN nodes or support assumptions occur in this packet.

Run the complete C8 baseline and both new packets, checking exact set equality and disjointness, from repository root:

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Others/FullMore.py
~~~

Independent component replay: run Research/Night2400/FrontierTree.py on either packet. Neither discovery tools nor online factors are required. The frozen shard P31_I00069 has precisely [[31,352]] remaining; no other exponent or canonical root is implied.

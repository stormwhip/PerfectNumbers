# Full exact key (19,282): final precision-branch union

**Theorem.** There is no odd perfect N≤10^2400 with v_19(N)=282. This statement concerns the exact valuation only; no lift to exponents divisible by 282 or to another root is claimed. The global 2400 frontier is a separate problem.

Let t=1735317810514627. Its primality is checked deterministically and v_t(σ(19^282))=1, so the first forced t exponent is positive even (t≡3 mod4). For each assigned row, the product X of exact powers and odd emitted product S imply XD|N, with D the part of S outside assigned bases. The two historical cold packets independently recompute the 27 directly live t powers, even 2..54, and the monotone cap at 112. They cover distinct 19+7=26 live powers (see [F4 historical proof](../../Night2400/F4/README.md)). The sole missing t exponent was 10. There r=8383027 is a forced prime in D; its directly live exponents are exactly the 50 evens 2..100 and the size tail begins at 202. We now eliminate all 50. The aggregate entry establishes the following disjoint whole-r subsets from isolated arithmetic verifiers; cross-covering internal or repeated subcases are never double counted:

| Whole r exponents | Evidence |
|---|---|
|20,32,34,38,44,46,48,50,54,56,62,64,68,74,76,80,84,86,90,92,94,96,98,100|[24 direct forest fibers](Proof282.md)|
|28|[Compelled 193-digit Q², 35/37](ProofInner.md); [23773^1](ProofInnerOne.md); [23773^4](ProofInnerFour.md)|
|82,88|[Additional forests](ProofHigh.md)|
|66,70,78|[Conditional Euler-fixed exact joint price](ProofHighThree.md)|
|14,16|[Native-seeded certified forests](ProofLowPair.md)|
|2,8,26|[Abundance progression](ProofAbundance.md); the other 14 members of its 17-value progression already accounted for elsewhere|
|10,30,72|[Abundance and forest](ProofMidThree.md)|
|58|[Locally proved absence masks](ProofMasked58.md)|
|18,24,60|[Additional masked forests](ProofMaskedMore.md)|
|6,36,40,42,52|[Five complete masked-forest fibers](ProofFiveMore.md)|
|4|[Full r^4](ProofFourth.md)|
|12|[Full r^12](ProofTwelfth282.md)|
|22|[Every one of 94 directly live 23773 exponents, including final exact-power rule](ProofR22Full.md)|

The final verifier has no dependence on the many discovery checkpoints. It authenticates every obligatory prime label before use; tests exact incoming constraints, parity and direct size on all compatible exponents including the complete infinite tail; requires strict integer bounds with independent forest evaluations; and proves any additional absence or exact-power restriction locally by overabundance before using it. Native ECM / PARI or lookup tables are never needed to check a sealed certificate. Neither of the two giant unfactored cofactor remnants used during discovery is assumed prime. The two-target or three-target prices used at a few leaves only involve unassigned ordinary prime powers because the Euler prime is already fixed at an exact prefix.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyAll282.py

The isolated individual final-r22 replay passed, as did every newer earlier component. The aggregate command additionally replays **both** actual historical first-pivot packs and then all remaining r fibers, under this exact key only (not all historical global work). Audit and aggregate wall times are recorded separately after completion.

**Serial receipt.** The full command above exited 0 in 3360.000 seconds of measured script wall time (3361.229 process seconds under concurrent load). It actually revalidated historical 19 and 7 fibers, their disjointness, every new provider, the three complementary r^28 subdomains and the full 94-child r^22 packet. Final output: “complete r-values 50 of 50”; “FULL KEY (19,282): all 27 first-pivot values and strict tail; all 50 second pivot values under first 10.” This is a full replay of this key, not an all-repository historical cold/reproduction claim.

**Independent acceptance.** A second reviewer ran the full aggregate in 3327.483 s and obtained the same complete-key result; this includes independent examination of the final 14 exact-power deductions. The auditor reported the result to the lead.

# Independent audit: (19,618), f=16 and f=14 primary closures; f=12 partial

PASS. I independently ran the following isolated programs in sequence (job pwsh-2fea2c7b661e4a9f, 70.018 seconds total, exit 0):

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyAnchorMore.py
    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyNested.py

Observed direct h sets: f=16 evens 2..8 left empty; f=14 evens 2..20 left [2]; f=12 evens 2..10 left [4]. Nested f=14 passed complete, 32 visited nodes. Acceptance scope: complete f=16,14; only conditional at f=12, where anchor v_z=4 still is not excluded by these witnesses. No full (19,618) claim.

Checked file SHA-256 values independently:

    VerifyAnchorMore.py 340eab52ba3d79885702f55da7d775331f3fcd5df8a5b144fdac497ad3fc7ec7
    AnchorMore.json    1b1d56be5fd5a9b9c6978ae52bbfc94210fa8fb14f7775f180d8313179cf2d7d
    VerifyNested.py     ecad36f39c374711f1e7558d35265d1d40fcc9a2345fb83f4f1f0ce8e61db030
    Nested618.json     8f23b0a23910dc6f34997dcf08412b8e8085769d2f86496b911e03cd91a92296
    AnchorKernel.py     4d82a3ca79fc74fa20df2412ac905682720c190a24d4748ce75106429f72ef70
    InverseMore.py      24190ffea086be5c28d512d8ec75fe1fd43efcf951661ed6e4b28f3c67bcc16f

The base credit/large-Euler argument was reviewed separately. For these extensions I checked the following new issues. Certification binds each hint to a prime dividing the actual prefix emission; completeness is demanded only for the claimed complete low sigma supports, not for optional added credits. Nested splits use a compulsory r|D which either cannot be Euler by 3 mod4 or does not satisfy the forced Euler residue class. Scanning starts at the least even ≥v_r(D), and the upper size tail recomputes X(D/r^v)r^k at each prefix. K.run returning False cannot discharge an omitted node. Each extra prime was proved ordinary before its even h was added. The 32-node count includes directly contradictory assignments; it should not be called a forest count.

For an unpruned prefix, A is retained only if coprime to every additional fixed prime; D/A=H is checked integral. At s=0 a credited prime is used only from C0, which was shown to exclude Euler, or from a base inconsistent with the required residue. At s>0 the early X0 A C0 lower bound needs q∤A,C0 only: even when q divides a new emission it is sound. The stronger X D bound and all the remaining credit claims are attempted only after independently ruling q out of every stripped extra emission Eo as well. Their cofactor residue classes nest because each new modulus is an odd multiple of its predecessor; if absence was proved at one s it persists to larger s, justifying the early monotone break. The costs for u≤MG and u>MG remain separately repriced; any positive parity credit F is on distinct labels only, disjoint from a supplier whenever counted.

Checked the stronger inverse test: for u≥308, existing budget forces the LTE lift contribution at most one, leaving ord 3 or 9 and an eighth-root-list of **eight nontrivial ninth roots** (not roots of order eight) modulo 19^307. If r|A then ord_r(19)=619, hence r≡1 mod1238. CRT for r modulo 1238·19^307 and A/r modulo the same modulus has positive lower representatives R,J; RJ>A in every class, a contradiction. Thus r∤A; the H-only bound is valid even if gcd(A,H)>1. The prior square reimbursement requires coprimality and is guarded by it. All lower log terms use floor(K log2), subtracting an extra unit for the denominator; thresholds are rounded up. The initial binary sweep need only eliminate all s up to the last successful comparison, which follows from monotonicity of the **exact** underlying simple price independent of rounded monotonicity. Supplier size increases and opposing price decreases within each u slice. No issue identified.

## Subsequent f=12 completion (separate witness)

PASS for the independent run of VerifyTwelve.py, which calls the same verified nested kernel and asserts a sole exact f=12 root. Output: complete 618 f=12, 37 visited (job pwsh-5605c48224eb48fb, exit 0). I independently reconstructed the two raw bounds: z=3321227264918952026382327955981619089 has forced multiplicity exactly 1 and candidates 2,4,…,20 (tail at 22); under its exact exponent 4, y=1464917891 also has forced multiplicity one and positive even exponents 2,…,52 (tail at 54). y is 3 mod4; z already cannot be Euler by the C0 cofactor test. Thus 1+10+26=37 nodes are required without filtering; they were visited, and every one closes directly or recursively. y²+y+1=2145984428836805773 agrees with the validated emission witness. This new packet, unlike AnchorMore by itself, closes the full f12 first fiber. No other f inferred.

## Subsequent f=10 completion (separate witness)

PASS independent isolated VerifySmallTen.py (job pwsh-5b5f43c84e2b4527, exit 0). The entry point pins exactly f=10 and calls the identical nested verification kernel, including complete certificate replay. Independently enumerated raw rows: 378187870792379499171334894532489 occurs exactly once in the obligatory D, admitting the twelve even exponents 2..24 before tail 26. At its exact valuation 2, the required 27589344910238346484326937 occurs exactly once, yielding thirteen even exponents 2..26 before tail 28. Both violate the compulsory Euler progression (so cannot be special). Visited 1+12+13=26. All descendants closed; full f=10 only. The primary key (19,618) itself is not thereby closed.

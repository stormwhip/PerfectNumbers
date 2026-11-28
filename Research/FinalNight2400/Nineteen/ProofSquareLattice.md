# An even-source with u≥98 cannot have its square paid by A

Refinement of [ProofLattice.md](ProofLattice.md) for repeated prime divisors. If u=v_19(σ(y^h))≥98, h even, then as before v_19(h+1)≤2, so y is a nontrivial ninth root mod 19^96. If y²|A, y≡1 mod 1238 again and y≤isqrt(A). It suffices to enumerate 8 CRT classes directly with M=1238·19^96; the cofactor classes are not needed. For a putative divisor b=R+Mx with b²|A use the same c≡R/M mod A. The integer lattice basis of degree <n this time consists of

    x^(l−j) (x+c)^j A^(k−floor(j/2)),   j=min(l,2k),   0≤l<n.

At the putative x every such value is a multiple of b^(2k), since b|(x+c) and b²|A. Thus if a short integer coefficient combination H satisfies Σ|H_j|X^j < lo^(2k) throughout the candidate divisor band [lo,hi], then H(x)=0. As in the simple-divisor certificate, two such polynomials with coprime reductions mod 65537 cannot have a common integer root. Strict coefficient sums checked on **264** class/band pairs, complete contiguous coverage from each R through isqrt(A), and x=0 separately ruled out. No reliance on the quality of LLL or on factorization of A. Standard-library replay:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifySquareLattice.py

Replacing the earlier 206 activation by 98 is therefore valid in all anchored square-reimbursement bounds. Simultaneously [the earlier certificate](ProofLattice.md) makes u≥185 sufficient for no overlap whatsoever with A. Neither standalone lemma excludes a first-pivot case without further pricing/tree checks.

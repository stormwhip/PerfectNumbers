# Anonymous root factors: exact pricing, square-divisor depth cap and scalar witness

Let N be odd perfect ≤10^2400; p^e||N at (p,e)=(7,906),(7,738),(7,456),(13,612),(13,618), with canonical forbidden roots. Put A=σ(p^e), n=e+1 prime. Since n∤A and gcd(p−1,A)=1 for these n, every prime r|A satisfies ord_r(p)=n and r≡1 mod 2n. For ordinary r^f||N with b=v_p(σ(r^f)) and r of order 3 mod p, b>0 requires 3|(f+1), and b=t+j, t=v_p(r³−1)≤e, j=v_p(f+1).

## Supplier price independent of factoring A

For t=1,…,e, lift each nontrivial mod-p cube root x to its unique representative modulo p^t. Combine r≡x mod p^t and r≡1 mod 2n. Check all representatives in [1,10^5 p^t] of exact valuation t by gcd(A,product representatives). `ExceptionalCube.py 100000` finds no factors. Thus any such actual supplier r exceeds 10^5 p^t. Therefore

    r^f/p^(2b) ≥ r²/p^(2t) · r^(3(p^j−1))/p^(2j) > 10^10.

If r≡1 mod p, b=v_p(f+1)>0 implies f≥p^b−1≥(p−1)b; direct progression exclusion below 10^6 gives the same price. If b=0, r^f>10^12. These exhaust ordinary r for p=7,13 because no other nontrivial odd order divides p−1. This proves an unconditional >10^10 multiplicative valuation premium **per distinct ordinary r|A**, not a speculative squarefree assumption. Existing general U_e covers all other deficits. In the Euler exponent≥5 or Euler-one with s=0 case, `CountGuard.py` implies maximum number of ordinary A-primes 10,53,124,35,33 respectively. At p=7,e=456 the count guard can be redundant given separate size bounds. Do not claim all cases are equally tight.

## Integer square-factor exclusion

For the same targets, in the given order, set h=183,150,94,124,125. The simultaneous conditions r²|A and ord_p(r)=3 and v_p(r³−1)≥h are impossible. For each of the two nontrivial cubic residues lift to x mod p^h; CRT with 1 mod 2n gives z mod T=2n p^h. All r lie in [z,isqrt(A)]. The ten `Anon-*.json.gz` receipts tile each complete interval; 268 integer lattice leaves in total (66,54,32,58,58). The archived `LatticeLeaf.verify` tests polynomial divisibility and strict magnitude, exact rational roots and Sturm exclusion. FLINT is *only* a discovery tool. Replay:

```
python -I -S -B parity-lab/AnonymousGuard.py unpack/PerfectNumbers-HEAD verify
python -I -S -B parity-lab/ExceptionalCube.py 100000
python -I -S -B parity-lab/ManySuppliers.py
python -I -S -B parity-lab/CountGuard.py unpack/PerfectNumbers-HEAD
python -I -S -B parity-lab/Bottlenecks.py
```

The valuation price and square-depth constraints are usable jointly, subject to separate accounting of mass and valuation ledgers. In particular no higher-level A-prime source can hide its entire even exponent f in A: r has v_r(A)=1 and must pay at least r outside that copy of A.

## What the five branches still lack

`Bottlenecks.py` constructs explicit **scalar relaxation parameters only**, not putative odd perfect N or realized sigma emitters. Each example has s=i=e/2, external b=0, no remaining external 3-supply (more generally p-supply). The chosen q=2m p^s−1 is proved prime, not just tested probable: exhibit a norm-one g in the quadratic algebra modulo q for which g^(q+1)=1 and g^((q+1)/p) differs from 1 modulo every prime ell|q (coordinate gcd=1). Mod ell, the norm-one group in the split/non-split quadratic algebra has order ell−1 or ell+1. Hence p^s|ell±1, forcing ell≥p^s−1>sqrt(q). The model retains lower prices H≥A·10^13, H≥p^(2i) and minimal r^f>2q/3, realizing both mass bounds as abstract square heights. It does **not** assert the synthetic square H is divisible by A, r yields q, or the internal supplier primes exist. Its purpose is to disprove sufficiency of the *scalar* bounds: log10 floors are 2317,1889,1174,2063,2084; not even primality checking q rescues these bounds. The new >10^10 price is a per-prime count: few medium-level suppliers can remain feasible unless actual factor classes or abundant auxiliaries are ruled out. No full exponent or shard credit.

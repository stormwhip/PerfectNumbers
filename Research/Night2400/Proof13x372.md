# Canonical (13,372): exact disjoint fiber proof

Assume an odd perfect number \(N\le B=10^{2400}\) with \(v_{13}(N)=372\) and earlier canonical roots \(19,7,11,31\) absent. Let \(Q=438552673580231875649\). The ordinary exact checker proves its primality and its forced occurrence in \(\sigma(13^{372})\); it reconstructs 25 live first-pivot exponents through the monotone size tail at 78. The [whole-key replay](Verify13x372.py) requires each of four disjoint parts and verifies their union equals this live domain:

1. [18 ordinary exact fibers](Fibers13x372.json.gz) by two integer forest evaluations, with every internal sibling re-enumerated.
2. [Five more complete fibers](C5/README.md) (1,4,6,8,16) by exact tree or exhaustive support partition. The same replay supplies five masks at pivot value 2.
3. [Three complementary masks](Masked13x372V2.json.gz) at value 2. Together the two mask packs exhaust all eight canonical supports, with one Euler component and all tail bounds checked. No historical support verdict is a premise.
4. [The complete tree at value 12](Frontier13x372V12Complete.json.gz): 375 forests, 14 downstream split nodes, 418 direct exclusions (including the first split), one stock price, one LCM prefix price and two refined interior price leaves. Earlier open ancestors are not ignored.

## The last two Euler-one interior leaves

For a fixed branch, write \(X\) for the product of the fixed exact prime powers, \(C\) for the part of their odd divisor sums coprime to \(X\), and let \(m\) be the incoming Euler-one prime-power product for two selected targets. The [LCM refinement](C7/README.md) checks an exact joint lower bound \(V\) and yields \(N\ge Vq/m^2\) for a free Euler-one prime \(q\). Thus \(q\le U=\lfloor Bm^2/V\rfloor\) in addition to \(q\equiv 2m-1\pmod{4m}\). The existing exterior and large-Euler tests remain in force.

If \(q\) is interior, it divides a known odd divisor-sum block \(Z\). For an odd prime index \(n=e+1\) with \(n\nmid Z\), Euler's prime \(q\mid\sigma(r^e)\) cannot divide \(r-1\) (otherwise \(q=n\)). Hence \(r\) has exact order \(n\) modulo \(q\), and \(q\equiv1\pmod{2n}\). The [new checker](InteriorPrice.py) combines this with the Euler congruence using exact CRT, or skips this extra restriction if its hypotheses fail. If the resulting modulus is \(T\) and residue \(a\), a possible cofactor \(k=Z/q\) must satisfy

\[
\lceil Z/U\rceil\le k\le\lfloor Z/a\rfloor,\qquad k\equiv Za^{-1}\pmod T.
\]

The cofactor interval also gives a tighter interval for \(q\). For short windows the checker exhausts the smaller progression; equality at the upper size endpoint is included. For longer windows it checks supplied integer polynomial witnesses with the [frozen lattice verifier](../NightMerge/LatticeLeaf.py). Removing prime factors common with \(T\) on the prime side is legitimate because \(\gcd(a,T)=1\); on the cofactor side the verifier requires \(\gcd(Z,T)=1\) instead. LLL is only a discovery tool; arithmetic replay checks divisibility, strict polynomial magnitude and root exclusions without FLINT. Each window and each used witness is bound by its block index and by both exact incoming levels.

The two terminal branches share \(2239^2,128599^{60}\). Their extra fixed components beyond \(13^{372},Q^{12}\) are, respectively, \(756749110661077^4\cdot463891^{22}\) and \(756749110661077^{12}\). The two refinements exhaust 620,429 and 2,033,549 direct divisions, plus 240 lattice windows in the second branch. The common 1019-bit cyclotomic cofactor was not assumed prime or squarefree, and was not factored.

```sh
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Verify13x372.py
```

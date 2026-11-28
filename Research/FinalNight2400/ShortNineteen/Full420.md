# Complete canonical key (19,420), P19_I00080

Assume N odd perfect, N<=10^2400 and 19^420 exact. The prime t=28174642921954703272833689609691232580811241064837460583 is compulsory; the [baseline C arithmetic](../../Night2400/C/README.md) reconstructs its entire direct domain {2,4,6,8,10,12} and excludes 8,10,12. There is no assumption of a historical certificate for any other first value. The present package completes all three outstanding values.

* **First 6:** [weighted price and ordinary forest](FirstSix420.md). Explicit Euler-on-vertex alternatives and the ordinary case exhaust all Euler rows.
* **First 2:** [giant mandatory r and three secondary forests](DeepProof.md). All second valuations 2,4,6 checked. The integration uses only e=420 in the dual-key helpers.
* **First 4:** the [direct 29 secondary exclusions](Four420.md) force the exponent of r=72688845161 to lie in {1,2,4}. Exact r^1 is closed by [disjoint-order pricing](One420.md), exact r^4 by [six tertiary forests](SecondaryFour.md). Finally, when r² is exact, prime a=200433813211 divides sigma(r²) and is 3 mod4, hence its exponent j is positive even. Exact first raw size overflow and ordinary prefixed checks leave j=2,4,...,40. The [last verifier](SecondaryTwo.py) and [twenty-forest witness packet](SecondaryTwo.json.gz) handle every such value. At j=10,12,18,22 use V from the same integer square-price as the preceding proof on targets (19,t,a), with zero weight at r: V>B rules out high Euler exponents, and for every eligible Euler-one vertex q the strict Vq>B gcd(M,q+1)^2 inequality is recomputed. Mark only the occupied Euler slot to use the ordinary forest. In all other j the cheaper unrestricted-Euler forest is enough. The 559 large prime chains and forest-vertex checks are mandatory; native seeds and output scores are not proof inputs. The minimum decimal floor equal to 2400 is used only if the underlying integer exceeds B strictly.

[Integrated verifier](Full420.py) runs the baseline checker and all the above new scoped checks, from repository root:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/ShortNineteen/Full420.py

This is a single-key argument; the separately investigated (19,330) is not implied. No transfer to multiples of exact exponents.

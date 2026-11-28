# Full canonical (31,352) independently accepted

Assumptions are 31^352 exact, prior roots 19,7,11 absent, odd perfect N≤10^2400. Both frozen maps independently checked: [31,352] is the sole member of P31_I00069 and appears nowhere else. No divisibility lift or unconditional statement outside its canonical class.

Cold targeted [full union](../Others/FullMore.py), SHA-256 32cb8c31f4dc425805bd0463fa4786d8312cd339e580bd5ba9a8a0a3cb1ab79d, passed in **240.628 s**, exit 0. [Transcript](FullMore.txt) confirms C8 returned the advertised 17 complete firsts and the correct 14 actual gaps. Independent [arithmetic root partition](../../Night2400/Receipts/FiberPartition.py) of both new packets found the same pivot 1797674429773, 31 first exponents, 33 directly dead, 47 incompatible, strict tail 112.

* [Thirteen complete firsts](../Others/ThirtyOne352Thirteen.json.gz), SHA-256 c83ed8210c73de47d04232334f4b0be9284fbc2988439f940c67b4358b1fc032, 175 ECPP chains, thirteen separate forest leaves, no split or OPEN under any of them.
* [The last first](../Others/ThirtyOne352One.json.gz), SHA-256 48705e23207216c6a89269270b356e92d3215d2c686fa522f3531bc3b12849e3, 352 ECPP chains. Q¹ fixes Euler and (Q+1)/2=151·5952564337. Independent second-domain reconstruction: tail 138, 24 live even exponents, exactly 23 forests and one joint price child at 30. The integrated verifier rechecks all prime chains and arithmetic, not just stored counts.
* [Independent price implementation](CheckMore.py), **36.248 s**, uses no candidate imports. It reconstructs CRT lifts, tests candidate powers with full geometric-sum gcds, targets exactly 31 and 5952564337, with caps 352 and 29. Since Q is already Euler, all other components are even. All 25 exception labels yielded a strict rational lower bound with decimal floor **2426**, not just a text receipt of the historical checker.

Hence 17+13+1=31 disjoint complete firsts and no open key remainder. Historical C8 runs all 16 support masks on its first 2, as well as independent complete split/price proofs. No all-history cold replay is claimed.

~~~sh
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Others/FullMore.py
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Audit/CheckMore.py
~~~

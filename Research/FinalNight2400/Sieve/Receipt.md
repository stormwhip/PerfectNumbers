# Cofactor and conditional-pricing receipts

Scope: mathematical data for owners, **no new full key claimed by this packet**. No network required for replay. For each command run at repository root.

## Certified complete factor supports

~~~powershell
python -I -S -B Research/FinalNight2400/Sieve/Verify.py
python -I -S -B Research/FinalNight2400/Sieve/VerifySecond.py
~~~

The first checker divides the exact geometric sum to one and verifies each prime by elliptic chain and/or deterministic 64-bit endpoint. Passed for base 2477 and exponents 2,4,6,8,10,12,14,16,18,20,22,24,28 (thirteen exact sums) under (19,618); [Factors.json](Factors.json) SHA-256 f33b9a97b44ff3eecd05655b473431d0d07e4b2d910633c612e421bb2e7ab83b. For f=22, the remaining 58-digit composite splits into 3279121011156085019219 and 2910663903693459821418615885907423943. For f=24 the residual splits into 107045341301 and 5806302004356865348891295520696229532070268151. For f=28 the residual splits into 1250780918410681433123567567 and 1417627032949179712274552162834432419373601027296933818227413. These are exact factorizations, not proof of any incompatibility of exponents. Discovery: PARI/GP 2.17.3 and offline author table. No PARI for verification.

The second checker passed complete sigma(8383027^h), h=4,6,10,28 with 3,6,3,2 prime factors at the (19,282), t^10 prefix. For h=28 the full 193-digit residual after division by 59 has a verified ECPP chain. [SecondProof.json](SecondProof.json) SHA-256 947c52efe07f0fea6ffa753f22f9578a3363c6b0903726e3ad9fb211f34f2b35. No claim about the other second exponents.

## Reproducible negative search on (19,282), f=10

C = (t^11−1)/(23(t−1)), t=1735317810514627, a 152-digit block. Offline author index for (t,11) supplied only 23. In addition to exact-key lookup, [TableGCD.cpp](TableGCD.cpp) tested every sufficiently large factor token in the entire WSL offline index, recovering record boundaries from byte offsets. 41,322,879 records; 106,206,170 tokens; all 15,680,419 decimal tokens of length ≥11 processed; no nontrivial gcd with C (8.79 s CPU). Shorter tokens were already harmless by the direct sieve. [Order.cpp](Order.cpp) sieved all primes r=1 (mod 22) up to 10^10, precisely 45,504,543 trials (2.03 s). No divisor. For primes dividing Phi_11(t), the only exception to order 11 could be 11 itself; by direct substitution it is not a divisor.

* SymPy ECM 48 curves, B1=10000,B2=200000, seeds 24002701…24002708 (6 curves per seed), 41.55 s.
* GMP-ECM 7.0.6: 220 curves, distinct sigma 8700121…8700340, B1=250000 and requested B2=50000000, 124.84 s. All exit 0; no factors. See [C152Native.jsonl](C152Native.jsonl).
* P−1 base 3, P+1 bases 5,7,11; B1=50 million, actual B2=5565147196 on all four passes, 6.89+13.62+13.81+13.19 s. No factors; [C152Groups.jsonl](C152Groups.jsonl) includes exact native stdout.

There is **no primality or closure conclusion** from ECM or P±1 failures. Analogous negative search on (7,882) 339-bit sigma(30201838022902600352247769^4): all 113,761,519 candidate primes 1 (mod 10) to 10^10 (4.45 s); 48 SymPy curves (25.53 s); 120 GMP-ECM curves B1=180000,B2=36 million (30.77 s). No divisor. For (13,262) first46, A and C had no candidate divisor to 10^11 and 10^10 respectively; branch later closed by pricing independently of either factorization. (19,58) computation was not started after its owner obtained a proof without new factors.

Additional owner-requested results: [Emissions.json](Emissions.json), SHA-256 f7fdba0234c475c645789046a8e80c374af9bf80a772609b0ba8002290da0c3b, plus [VerifyEmit.py](VerifyEmit.py), prove complete prime factorizations of z²+z+1 at z=151297224100319027205239 (8 primes; f18) and 380135001457350914720133393511759489 (5 primes; f20). For (19,46) sigma(q^12) at q=70169234660105574400577005075855017842743056666917902427141, base-2 Fermat fails, so the 707-digit block is certainly composite. No factor found through 2·10^10 (73,516,714 candidate primes; 9.61 s); no gcd throughout the offline table (15,680,419 large tokens, jointly checked with 7,882; 12.45 s CPU); 80 native ECM curves B1=50000, requested B2=8 million, sigma=8701401…8701480, 191.09 s, all exit 0.

## Independent mathematical and arithmetic review of conditional pricing

The separate [OneReview.md](OneReview.md) independently audits the exceptional first 2477^1 at (19,618): 149 states, 33 internal splits, 99 price prunes, 10 abundance prunes and seven valuation conflicts.

~~~powershell
python -I -S -B Research/FinalNight2400/Sieve/AuditPricing.py
python -I -S -B Research/FinalNight2400/Sieve/Audit42.py
~~~

**(13,262) first46 PASS.** Independent lift of x²+x+1, inverse orientation of CRT, true gcd net-budget filter, square-Euler separate admissibility, capped high orders and exhaustive Euler windows reproduce 23 bases and upward rounded U=2247129787084402954; of 12098 windows 4984 close by price, 5320 mandatory size, 1794 emitter. For the latter, Euler q is exterior to the fixed blocks; overlap of its distinct ordinary emitter with their product is at most the larger block since the blocks are coprime. Removing the emitter from the priced set lets its p,t supply cancel between the two inequalities; no repeated charge. SHA-256 62198eeca1b898e60778fa722f9c8f4ab4eabd1c876c503fc3edfffb031c343f.

**(13,310) first42 PASS.** Independently lift primitive roots by x→x^s from s^k to s^(k+1), preserving root order; compute exact p-power caps on each emitter. Disjoint odd order/length factors for 13 and t ensure the two weighted price budgets fit in actual atom exponent. Six 13-loss labels, no t-loss label, U=4016; 13062 windows partition [11596,930,536]. SHA-256 4ba9f6130cd6c99449d28d208e81c721661644c8ff2a7093b5b27bc48f87580a. Neither script alone verifies a full canonical key, and neither verifies the historical forests or their union.

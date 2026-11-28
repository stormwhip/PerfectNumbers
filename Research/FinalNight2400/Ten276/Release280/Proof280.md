# (19,280), first valuation 2: eleven exact residual paths excluded

For B=10^2400 assume N odd perfect, 19^280 || N, and s² || N at s=353998162545967. Let t=5967366623139106062930976717, y=16208389663, r=4465757330217695897641, z=167887043133006663319040440782979, k=132001981879. Every row below is an *exact* valuation condition, not a divisibility lift. No full key, no shard and no unconditional full first fiber is claimed.

Fully rejected prefixes after 19^280 s²:

|Additional exact components|Number of paths|
|---|---:|
|t⁴ r² z² or z⁴|2|
|t⁴ r⁸ or r¹⁰|2|
|t⁶ y¹² k²²|1|
|t⁶ y³⁶, y⁴⁰, or y⁴²|3|
|t¹⁰ y²², y²⁸, or y³⁶|3|

These are eleven of the fifteen unresolved paths in the earlier [C13 scout gap list](../../../Night2400/C13/README.md). The other four scout gaps are t⁶ y^18,^22,^28,^30. Note particularly that C13's deep supplement did not verify every already-rejected scout leaf; therefore **even resolving the fifteen by itself would not prove the whole fiber.** The exact prefix sequence is checked from its first row using actual divisibility, as are all dynamically supplied primes in the new trees.

## Proof

Let X be the product of the assigned distinct exact powers, S equal to the product of their odd σ parts and I their exact abundancy. Then S divides N and X divides N. Put Y=S/gcd(S,X). If gcd(X,Y)>1 the fixed exponent is overfilled. Otherwise XY|N. All members of the set F of distinct *proved* prime divisors of Y, with h=v_l(Y), are compulsory. At most one additional prime can be Euler; if an assigned exponent is odd the slot is already occupied. Never assume that the smallest allowed exponent of a 1 mod4 compulsory prime is automatically even.

For each l in F consider the normal case (even exponents g≥h) and, if l≡1 mod4 and the Euler slot is free, the exceptional case g≡1 mod4. In each class take the first g for which l^g≤B and no presently proven absent prime divides σ(l^g). If exhausted, this class is impossible. Since σ(l^g)/l^g increases with g, it is safe to take the minimum of I∏σ(l^g_l)/l^g_l with either *all normal* or exactly one exceptional l. The all-normal option also covers Euler outside F. An option with a missing valid index on any constituent is discarded. If every option is impossible or has abundancy >2, the node closes. Otherwise use this common lower bound L. For every small u distinct from all assigned and compulsory nodes, if L·σ(u^a)/u^a>2, then u is absent, with a=1 for a possible Euler (and a=2 for ordinary). Adding the union of such absences and repeating is safe: each ban is a logical consequence of this current prefix, not a global assumption. All tests use exact rationals. As an example the three shallow t⁴ leaves close immediately with strict lower abundancies >2.0600,2.0523,2.0541, respectively, even allowing the most favorable Euler component.

At the fixed point apply the same minimum over Euler placements to XY∏l^(g_l−h_l). This is the mandatory mass plus *only* the missing exponents on each compulsory prime; there is no overlap. All genuine solutions exceed or equal this mass. Strictly above B closes. A remaining branch fixes the exact exponent of a certified member l of F, visiting all positive g≥h through the first strict raw tail X(Y/l^h)l^g>B, including every admissible odd Euler case. Recheck the ban and conditional output factors exactly, update X,S,I, occupied Euler status and compulsory labels, and recurse. Distinct labels are stored in sets; new compulsory valuations are recomputed from the whole S, not the sum of arbitrarily selected lower bounds. Higher g excluded by monotone size, no depth cut is accepted. No input tree Boolean or externally generated score suffices to close a leaf.

## Replay and provenance

~~~text
python -I -B -S Research/FinalNight2400/Ten276/Release280/Verify280.py
~~~

[Verify280](Verify280.py) uses exactly the eleven [explicit paths](Paths280.py), eleven small compressed trees, a deduplicated two-part deterministic ECPP book, and the existing 64-bit/elliptic checker. Prime candidates generated offline from the published factor index or by local factoring were certified with locally cached PARI; no external software enters verification. Complete cold run 97.590 s: 2,055 ECPP certificates used; 11,281 splits, 33,307 raw/conflict, 16,764 parity-size, 1,942 abundance terminals. Beyond these terminals, each split checks incompatible exponents and its infinite monotone size tail. The two generating packages are [book one](AbBook0X1X2X3X14.json.gz) and [book two](AbBook4X9X10X11X12X13.json.gz). This receipt does not claim any broader historical cold replay.

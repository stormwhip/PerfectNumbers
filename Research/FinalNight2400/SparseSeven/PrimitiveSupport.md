# Factorization-independent upper Euler window: s≤681 at canonical 7^906

This strengthens [AllSupport.md](AllSupport.md) without any assumption about the unknown support of A beyond the proved minimum count of three. If s≥682, the Euler component must be linear and every q-emitter internal. Let z^h be such an ordinary component, c=v_z(A). For s in the tested range q≥Q0=2·7^s−1>5100. If z≡1 mod q then q|h+1 by LTE, impossible since 3^5100>B; z=q cannot emit q. Otherwise o=ord_q(z)>1 divides the odd length h+1. If o is a proper divisor, h+1≥3o, and σ(z^(o−1))≥q implies z^(o−1)>2q/3. Hence z^h>(2q/3)^3, contradicting X q (2q/3)^3>B, checked for every tested s. Thus **o=h+1 and h+1|q−1**. In particular 7∤h+1 since q=−1 mod7; the h=6,m=4 possibility that remained in the 685..698 range is *entirely impossible*.

For completeness recalculate all signed A0/B0 bounds from the preceding theorem using a better lower endpoint for every (s,h): q=2mY−1, Y=7^s, m odd, gcd(m,7·19)=1 and mY≡1 mod(h+1). A bounded small-divisor sieve may skip up to eight *proved* incompatible m in that progression. The final tested endpoint is still a lower bound whether prime or composite. Thus all prior strict inequalities remain valid at the improved Q. Across 682≤s≤710, the sole surviving shape is (h,c)=(4,2) at 682,683,684. In these three cases z^h>2q/3 and z^(h−c)≤B/(XAq) imply

    q^(2h−c) ≤ floor(B/(XA))^h · (3/2)^(h−c).

The bound here uses **floor(B/(XA))** legitimately: the integer q·z^(h−c) divides N/(XA), so q·z^(h−c)≤floor(B/(XA)). Taking the exact integer (2h−c)th root gives m≤300,42,6 respectively. Enumerate each admissible odd multiplier with h+1|q−1 and gcd(m,133)=1; every candidate is demonstrably composite by a failed base-2 Fermat congruence. No probable-prime success or unknown factorization is assumed. Therefore these three s are also impossible. The old proof covers s>710, so the unrestricted s= v_7(q+1) must satisfy s≤681. The gap s=0..681 remains open in general; this is not a canonical key closure.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/SparseSeven/PrimitiveSupport.py

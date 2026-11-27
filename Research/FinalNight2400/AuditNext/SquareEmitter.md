# A short congruence eliminates both residual square-emitter factorizations of Φ907(7)

**Lemma.** Let A=(7^907−1)/6=z²w, with z,w positive integers, z≥3. Suppose q divides z²+z+1, q is an Euler prime, q≡−1 modulo Y=7^s and 605≤s≤906. Then this allocation is impossible. No factorization or squarefreeness of w is needed.

Set k=(z²+z+1)/q≥1. Since q≡−1 (mod Y), z²+z+1≡−k. Since 6A≡−1 (mod Y), multiplication by 6w and substitution of 6wz²≡−1 give **6w(k+1)−1≡−6wz (mod Y)**. Squaring, (6wz)²=6w·6A≡−6w. Consequently

    Z = (6w(k+1)−1)² + 6w

is a strictly positive multiple of 7^s. But wk=(A/q)(1+1/z+1/z²)<3A/(2q); also w≤wk. Therefore 6w(k+1)−1<18A/q and 6w<9A/q. Since q≡1 mod4, q≥2Y−1. The [integer check](SquareEmitter.py) gives (18A)²+9A(2Y−1)<Y(2Y−1)² at s=605 and for all higher s. Thus 0<Z<Y, contradiction.

This applies whether z is the high-7-supplier r or its companion b: whenever the final sparse analysis yields A=z²w and ordinary exact z² emits q, the same argument applies. The [sealed four-pattern enumeration](../SparseSeven/VerifyPatterns.py) reports s≥633 for every remaining ω(A)≤2 pattern, strictly within scope. Given the separate signed A0 elimination of the other two patterns, this closes the **entire ω(A)≤2 branch**, without assuming A squarefree; this summary is subject to independent verification of those predecessor eliminations. The lemma alone does not eliminate ω(A)≥3 or the whole (7,906) key.

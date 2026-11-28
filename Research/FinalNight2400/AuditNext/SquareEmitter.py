"""Factor-free modular contradiction for BOTH remaining sparse patterns A=z²w with emitter z² at s>=605."""
A=(7**907-1)//6;Y=7**605;Q=2*Y-1
# Z=(6w(k+1)-1)^2+6w; k=(z²+z+1)/q>=1, z>=3, w=A/z², s<=906.
# wk=(A/q)(1+1/z+1/z²)<(3/2)A/q, w<=wk. Hence Z<(18A/q)^2+9A/q < 7^s.
assert (18*A)**2+9*A*Q<Y*Q**2
assert all((18*A)**2+9*A*(2*7**s-1)<7**s*(2*7**s-1)**2 for s in range(605,907))
assert (18*A)**2+9*A*(2*7**604-1)>=7**604*(2*7**604-1)**2
print('PASS: A=z^2*w, q divides z^2+z+1, q = -1 mod 7^s, s>=605 incompatible; both sparse s=633..665 residual patterns excluded.')

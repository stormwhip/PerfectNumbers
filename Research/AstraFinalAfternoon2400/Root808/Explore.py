"""Exact exploration of high Euler windows; reports remaining emitter shapes."""
from functools import cache
from math import gcd, prod

P, E = 7, 808
D = E + 1
X, W, B = P**E, P**D, 10**2400
A = (W-1)//6
L = 2*D
C = 10**7
SMALL = prod((2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97))


@cache
def iroot(n, e):
    if e == 1 or n < 2:
        return n
    x = 1 << ((n.bit_length()+e-1)//e)
    while True:
        y = ((e-1)*x+n//x**(e-1))//e
        if y >= x:
            return x
        x = y


def smallest_q(Y, h):
    m = pow(Y, -1, h+1)
    m += (h+1)*((1-m) % 2)
    for j in range(80):
        q = 2*m*Y-1
        if gcd(m, 133) == 1 and gcd(q, SMALL) == 1:
            return q
        m += 2*(h+1)
    return 2*m*Y-1


def remaining(s):
    Y = P**s
    Q0 = 2*Y-1
    # Check high Euler, exterior emitters and nonprimitive order excluded.
    assert X*A*Q0**5 > B and 3*B < 2*X*A*Q0**2
    assert X*Q0*(2*Q0)**3 > 27*B and Q0 > 5031
    h = 0
    out = []
    while X*Q0*C**(h+2) <= B:
        h += 2
        if (h+1) % P == 0:
            continue
        Q = smallest_q(Y,h)
        T = B//(X*A*Q)
        if not T:
            continue
        lo = max(C+1, iroot((2*Q)//3,h)+1)
        for c in range(1,h+1):
            if lo**c > A:
                break
            hi = iroot(A,c)
            if h > c:
                hi = min(hi,iroot(T,h-c))
            if c == h:
                # w=A/z^h, k=sigma(z^h)/q, M=6*w*k < 9*A/Q.
                # D'(M+D')^h+(M-1)^h is a positive multiple of Y.
                M = (9*A-1)//Q
                if M*(2*M)**h + M**h < Y:
                    continue
            if 3*W*T < Y*Q and 3*T < 2*Y:
                hi = min(hi,2*(W//Y)+1)
            if hi < lo:
                continue
            d = h+1-c
            z = hi**d
            V = 6*(A//lo**c)
            pos = ((W-1)*z-1)//(Q*Y)
            neg = (Q*z+(Q+1)*V)//(Q*Y)
            J = (-1-6*A)*pow(Y,-1,L)%L
            if (J or L) > pos and ((-J)%L or L) > neg:
                continue
            # Compose r^h>2q/3 and r^(h-c)<=T original (non-rounded q relation).
            cap = iroot((B//(X*A))**h*3**(h-c)//2**(h-c),2*h-c)
            if cap < Q:
                continue
            m_max = (cap+1)//(2*Y)
            out.append((h,c,m_max))
    return out


if __name__ == '__main__':
    assert __debug__
    assert all(D % k for k in range(2, 29)) and D == 809
    assert A % D and A % P and A % 2 and A % 3
    assert 3**5030 <= B < 3**5031
    candidates = range(L+1, C+1, L)
    assert all(pow(P,D,r) != 1 for r in candidates)
    for s in range(708, 809):
        assert remaining(s) == [], s
    assert {shape[:2] for shape in remaining(707)} == {(8,3), (10,5), (12,7)}
    print('PASS canonical (7,808): prohibit v7(q+1) in 708..808; 707 still open under this test')

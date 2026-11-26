"""Two-centre balanced internal emitter lower bound for an odd cyclotomic block."""
from fractions import Fraction


def lower(center, odd_index, s, qmin, d):
    """Lower bound for r^(f-c) where r^c|sigma(center^(odd_index-1)) exactly.

    Hypotheses: r!=center, q Euler one, q|sigma(r^f), c<=f,
    center^s|q+1, 0<=s<=d=v_center(N), and
    v_center(sigma(r^f)) <= d-s. qmin<=q.
    """
    assert 0<=s<=d and d<=odd_index-1 and qmin>=3 and odd_index%2==1
    W=center**odd_index;Y=center**s;Delta=W//Y
    assert W%Y==0
    # Set a=center-1 and u=(W-1)/r^c. Then sigma(center^(odd_index-1))= (W-1)/a.
    # See the derivation in HardAtomRoute.md. Integer coefficients for r>=3.
    # w= sigma(r^f)/q, H=max(1,W/q), uw < 3Ht/2.
    return Fraction(Y*qmin, max(W,qmin)*(Delta+4))

"""Sealed exact exterior-Euler and two-source cuts in the 1093^256 fiber."""
from Prices import *
from Emitters import certificate,inside_euler,first_not_rejected
from CleanPrice import price2
from hashlib import sha256


def verify():
    assert __debug__
    p=1093;rows=((3,6),(p,256));R,Fx,odd,X,S,A,blocks=certificate(rows)
    assert not odd and sig(3,6)==p and blocks==[(p,257,A)] and Fx[p]-vp(S,p)==255
    V,E=price2(rows,p);assert V<B and len(E)==1
    cuts=[];remain=[]
    for j in range(256):
        y=p**j;a=2*y-1;q=first_not_rejected(a,4*y,blocks)
        if X*A*q>B or V*q>B*y*y:cuts.append(j);continue
        if inside_euler(a,y,A):remain.append(j);continue
        if X*A*q*R>B:cuts.append(j);continue
        # Let r^h be any ordinary source of the external Euler prime q.
        # For r outside A, the mandatory support has extra parity R, and is
        # disjoint from r^h>2q/3. For r in A charge the balancing amount,
        # not that same parity again. Uniform price contradiction on N^2 is
        # also valid for the interior source.
        ex=2*X*A*R*q*q>3*B or 4*V*X*A*R*q**4>9*B**2*y*y
        ins=4*V*X*q**4>9*B**2*y*y or X*A*q*q*y>B*max(p**257,q)*(p**(257-j)+4)
        (cuts if ex and ins else remain).append(j)
    d=sha256(repr(cuts).encode()).hexdigest()
    print('1093^256, Euler exponent one',len(cuts),d,'remaining bounds',remain[0],remain[-1],flush=True)
    assert cuts==list(range(198,256)) and remain==list(range(198))
    return cuts
if __name__=='__main__':verify()

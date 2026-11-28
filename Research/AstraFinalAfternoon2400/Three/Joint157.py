"""High-order secondary supplier allocation for the hard 1093^156 Q^46 prefix.
This is a conditional finite-bound exploration, not a closed subtree.
"""
from Prices import *
from Explore import CASES
from CleanPrice import price2
from Emitters import certificate,inside_euler,first_not_rejected
from Heavy import heavy
from sys import argv

p=1093;q=2035349

def mass_root(n,e):
    a,b=0,1<<((n.bit_length()+e-1)//e)
    while a+1<b:
        t=(a+b)//2
        if t**e<=n:a=t
        else:b=t
    return a

def orders():
    ro=CASES['6-156'];R,F0,odd,X,S,D,spec=certificate(ro)
    assert (q-1)==4*7*157*463 and all(prime(r) for r in (7,157,463))
    assert (p-1)==4*3*7*13 and all(prime(r) for r in (3,7,13))
    cp,cq=F0[p]-vp(S,p),F0[q]-vp(S,q)
    # Every atom with positive q and nontrivial order has basic order from this
    # exact set; target q is too large for index valuation.
    hmax=0
    while 5**(hmax+1)<=B//X:hmax+=1
    assert q>hmax+1
    os=[o for o in divisors(q-1) if o>1 and o%2 and o<=hmax+1]
    return ro,R,X,S,D,spec,cp,cq,hmax,os

if __name__=='__main__':
    ro,R,X,S,D,spec,cp,cq,hmax,os=orders()
    print('orders',os,'cap',cp,cq,'hmax',hmax,flush=True)
    for w in (6,):
        c,M,L=heavy(ro,q,w,even_only=True)
        print('q scalar',w,'V',floor10(X*q**(w*c)/M[-1]),'losses',sum(map(len,L)),flush=True)

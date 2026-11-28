"""Scalar high-price majorant: count the cheapest bases in every congruence class.
Unlike least-residue-only loss tables, it bounds all translates at arbitrary weight.
"""
from Prices import *
from heapq import heappush, heapreplace
from hashlib import sha256

@cache
def order_classes(p,o,cap):return root_levels(p,o,cap)

def log2_fraction_hi(A,den):
    # An upward dyadic ceil of A/den, represented as exponent. For quick diagnostics.
    d=A.bit_length()-den.bit_length();return d+(A>(den<<d)) if d>=0 else 0

def class_seeds(z,m,h,p,j,s,room,forbid,others,count,squares=False):
    # Return at most count cheapest bases of this class. Location of a possible
    # actual base beyond the retained prefix only improves every size bound.
    z+=((5-z+m-1)//m if z<5 else 0)*m
    if z%2==0:z+=m
    step=2*m
    for _ in range(2400):
        if (z.bit_length()-1)*h>=room.bit_length() or z**h>room:break
        if z not in forbid and all(z==d or (squares and z==d*d) or z%d for d in SMALL) and all(not exact_supply(z,h,d,0) for d in others):
            yield z
            count-=1
            if count==0:break
        z+=step
    else:
        # After 2400 sampled reps, keep a conservative bound for every unseen
        # possible base. No primality, distinctness or existence is presumed.
        yield from (z,)*count

def heavy(rows,p,w,max_cap=None, *, even_only=False, square_atoms=False):
    fixed,odd,X,S,D,blocks=get_context(rows); c=fixed[p]-vp(S,p)
    if max_cap is not None:c=min(c,max_cap)
    others=tuple(set(BAN)|{t for t,h in rows if t!=p and h==vp(S,t)})
    odd=odd or even_only
    lim=B//X;hm=0
    while qpow(5,hm+1)<=lim:hm+=1
    Z=[[] for _ in range(c+1)]
    # If an actual component's ratio is >1, the class candidate with its
    # ordinal rank within the class has ratio at least as large. Distinct
    # true bases inside the same class imply distinct ordinal ranks.
    def add(j,z,m,h,typ):
        if not 1<=j<=c:return
        A=qpow(p,w*j)
        # Upper envelope uses the cheap necessary filters only, no gigantic pow.
        for r in class_seeds(z,m,h,p,j,0,min(lim,A-1),fixed,others,c//j,square_atoms):
            den=r**h
            if den>=A:break
            item=(F(A,den),h,r,typ)
            heap=Z[j];k=c//j
            if len(heap)<k:heappush(heap,item)
            elif item>heap[0]:heapreplace(heap,item)
    admissible=lambda h:h%2==0 or (not odd and h%4==1)
    smax=0
    while p**(smax+1)<=hm+1:smax+=1
    for h in range(2,hm+1):
        if admissible(h) and (s:=vp(h+1,p)):add(s,1,p,h,1)
    for o in divisors(p-1):
        if o==1 or o>hm+1 or (odd and o%2==0) or qpow(5,o-1)>=qpow(p,w*c):continue
        for j,m,zs in order_classes(p,o,c):
            A=qpow(p,w*min(c,j+smax))
            for z in zs:
                for h in range(o-1,hm+1,o):
                    if not less(max(5,z),h,min(A,lim+1)):break
                    if admissible(h):add(j+vp(h+1,p),z,m,h,o)
    # Independent upper envelope for each available aggregate capacity via 0/1
    # knapsack over the retained per-level representatives; cross-class overlap
    # is intentionally not subtracted. Repeats across exponent classes increase
    # the discount, thus cannot mis-certify a price.
    M=[F(1)]*(c+1)
    def digest_row(row):return [(item[1],item[2],item[3]) for item in sorted(row,reverse=True)]
    for j,heap in enumerate(Z):
        if j:
            for ratio,_,_,_ in heap:
                for i in range(c,j-1,-1):M[i]=max(M[i],M[i-j]*ratio)
    return c,M,[digest_row(z) for z in Z]

if __name__=='__main__':
    from Explore import CASES
    from sys import argv
    k=argv[1];p=int(argv[2]); w=int(argv[3]);rows=CASES[k];c,M,E=heavy(rows,p,w)
    print(k,p,w,c,'loss',floor10(M[-1]),'price',floor10(get_context(rows)[2]*p**(w*c)/M[-1]),'counts',sum(map(len,E)),flush=True)
    for j,a in [(0,M[0]),(1,M[1]),(c//2,M[c//2]),(c,M[c])]:print(j,floor10(p**(w*j)/a),flush=True)

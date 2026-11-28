"""Use an independent scalar price and complete Euler/source partitions at 398581^150."""
from Prices import *
from CleanPrice import price2
from Explore import CASES
from Emitters import certificate,inside_euler,first_not_rejected,min_additional_abundance_lower
from hashlib import sha256


def capped_power(n,p):
    lo,hi=0,n.bit_length()
    while lo+1<hi:
        k=(lo+hi)//2
        if p**k<=n:lo=k
        else:hi=k
    return lo


def check_solve():
    assert __debug__
    rows=CASES['6-2-150'];R,fixed,odd,X,S,D,spec=certificate(rows);p=398581;z=1093
    assert odd==0 and len(spec)==1 and spec[0]==(p,151,D)
    assert sig(3,6)==1093 and sig(1093,2)==3*p
    assert fixed[z]-vp(S,z)==1 and fixed[p]-vp(S,p)==149 and fixed[3]-vp(S,3)==5
    V,E=price2(rows,p);assert V==X*p**298 and not E and V>B
    counts={};rem=[];cases=[]
    for i in (0,1):
      for j in range(150):
        mp=p**j;m=mp*z**i;a=2*m-1;q=first_not_rejected(a,4*m,spec)
        why=None
        if V*q>B*mp**2:why='plain price'
        elif X*D*q>B:why='forced mass'
        else:
          can_int=inside_euler(a,m,D)
          # If q|D, ordinary factors comprise D/q and must emit all required
          # target units except q. Without knowledge of q, drop the mass, not
          # any logical branch. Conditionally give q at least q0 in the price.
          if not can_int:
            FC=min_additional_abundance_lower(X,S,D,R,q)
            if X*D*q*R*FC>B:why='parity outside'
            elif 4*V*X*q**4>9*mp**2*B**2:why='two N inequalities'
            elif (X*D*q*q*mp>B*max(p**151,q)*(p**151//mp+4) and 2*X*D*q*q>3*B):why='emitter balance'
          # Source issue: q|D means the root q itself need not have an outside emitter.
        if why is None:rem.append((i,j,can_int))
        else:counts[why]=counts.get(why,0)+1
        cases.append((i,j,why or 'open'))
    print('PASS local Euler split 398581^150:',counts,'remaining',len(rem),'interior-possible',sum(t[2] for t in rem),'by i',[(i,min(j for a,j,b in rem if a==i),max(j for a,j,b in rem if a==i)) for i in (0,1)],'sha256',sha256(repr(cases).encode()).hexdigest(),flush=True)
    return rem,cases
if __name__=='__main__':check_solve()

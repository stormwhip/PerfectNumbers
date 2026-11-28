"""Integer side constraint from the supply of the exact small root 3."""
from Prices import *
from Explore import CASES
from CleanPrice import price2
from Emitters import certificate,inside_euler
from math import gcd,prod

# For the precise 3^6/1093^2/p^150 prefix, 3 needs exactly five unknown
# units. In a free-high-Euler power q^(4k+1), the parameter n=(q+1)/2
# holds its linear contribution; all even-index geometric atoms contribute
# ordinary 3-units. For q^1 exactly, route each exact a=0,...,5 among these.
def lower_euler(m,a,J=500):
    # q+1=2*m*l, v3(l)=a. Lifting does not replace the legal quotient l.
    C=3**a; k=1
    for _ in range(J):
        q=2*m*C*k-1
        if k%3 and all(k%p for p in BAN) and all(q==r or q%r for r in SMALL):
            return q
        k+=2
    return 2*m*C*k-1


def run(k):
    rows=CASES[k];R,fixed,odd,X,S,D,spec=certificate(rows);p=rows[-1][0];z=1093
    V,E=price2(rows,p);F0=fixed[3]-vp(S,3)
    assert not odd and (k!='6-2-150' or V>B)
    stats={};res=[]
    for i in range((fixed.get(z,0)-vp(S,z)+1) if len(rows)==3 else 1):
      for j in range(fixed[p]-vp(S,p)+1):
        m=z**i*p**j
        for a in range(F0+1):
          q=lower_euler(m,a);M=m*3**a;qq=2*M-1
          W=p**(2*j)
          if V*q>B*W or X*D*q>B:typ='basic'
          elif not any(inside_euler(qq,M,b) for _,_,b in spec):
              if X*D*R**len(spec)*q>B:typ='parity'
              else:
                # Exterior q requires external source or one internal to a block.
                # Check component disjointness separately in each role.
                allcut=True
                for c,d,b in [*spec,(None,0,1)]:
                    rhs=B;U=R**(len(spec)-int(c is not None))
                    if 4*V*X*D*U*q**4>9*B**2*W*b:continue
                    if c==p and j and X*D*U*q**2*p**j>B*max(p**d,q)*(p**(d-j)+4):continue
                    if c is None and 2*X*D*U*q**2>3*B:continue
                    allcut=False;break
                typ='source' if allcut else 'open'
          else:typ='open'
          stats[typ]=stats.get(typ,0)+1
          if typ=='open':res.append((i,j,a))
    print(k,stats,[(a,min(j for i,j,t in res if t==a),max(j for i,j,t in res if t==a)) for a in range(F0+1) if any(t==a for i,j,t in res)])
if __name__=='__main__':
    import sys
    for k in sys.argv[1:] or ('6-2-150','6-256','12-96'):run(k)

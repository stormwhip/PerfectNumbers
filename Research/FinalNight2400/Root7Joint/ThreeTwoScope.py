"""Bind the three individually cold-replayed 3^6 subtrees without inferring closure from absent rows."""
from pathlib import Path
from math import gcd,prod
import gzip,json
H=Path(__file__).resolve().parents[1]/'Three';B=10**2400
G=lambda q,h:(q**(h+1)-1)//(q-1)
if __name__=='__main__':
 assert __debug__ and G(3,6)==1093 and G(1093,2)==3*398581
 p=398581;allowed=set();X0=3**6*1093**2;S0=G(3,6)*G(1093,2);n=1;Y=X0*p*(S0//gcd(S0,X0*p));
 while Y<=B:
    if n%2==0 or n%4==p%4==1:
        X=X0*p**n;S=S0*G(p,n);D=(S//(1+n%2));D//=gcd(X,D)
        if gcd(D,X*7*11*13*19*31)==1 and X*D<=B and S<=2*X:allowed.add(n)
    n+=1;Y*=p
 assert len(allowed)==79
 def cover(z):return z is not None and (all(cover(v) for v in z['cases'].values()) if z['type']=='split' else z['type'] in ('forest','sqratom','fastpair','triple2'))
 union=set()
 for file,expected in [('SecondaryTwo',70),('DeltaTwo',4),('LateTwo',2)]:
    data=json.loads(gzip.decompress((H/(file+'.json.gz')).read_bytes()));tree=data['tree'];assert tree['q']==p and set(map(int,tree['cases']))==allowed
    complete={int(h) for h,z in tree['cases'].items() if cover(z)};assert len(complete)==expected and not complete&union;union.update(complete)
 assert allowed-union=={102,108,150};print('PASS 79 live, disjoint 70+4+2; remain 102,108,150')

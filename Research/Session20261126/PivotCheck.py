"""Complete one-pivot covers. New leaves are exact-only, never divisibility-lifted."""
import sys,gzip,json
from pathlib import Path
from functools import cache
from math import gcd,prod
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'Nov25/Compose'));import Compose as C
B=10**2400

def independent(p,e,q,f,roots,owners,head):
    ban=prod(C.ORDER[:C.ORDER.index(p)]);X=p**e*q**f
    S=(p**(e+1)-1)//(p-1)*((q**(f+1)-1)//(q-1))//(1+f%2)
    D=S//gcd(X,S);assert gcd(X,D)==1 and gcd(D,ban)==1
    pool=X*D*prod(z for z,_ in owners);kids={z:[] for z in [*roots,*(z for z,_ in owners)]}
    for z,t in owners:kids[t].append(z)
    def val(n,z):
        c=0
        while n%z==0:n//=z;c+=1
        return c
    @cache
    def cell(z,c):
        ordinary=anyslot=B+1
        for odd in (False,True):
            if odd and (f%2 or z%4!=1 or gcd(z+1,ban)>1):continue
            step=4 if odd else 2;j=c+((1-c)%4 if odd else c%2);count=0
            while count<head and z**j<(anyslot if odd else ordinary):
                n=z**j;G=(z*n-1)//(z-1)
                if gcd(G,ban)==1:
                    count+=1;G//=1+int(odd);u=G
                    while (g:=gcd(u,pool))>1:u//=g
                    sub=[cell(y,val(G,y)) for y in kids[z] if G%y==0];v=n*u*prod(a for a,b in sub)
                    if not odd:
                        ordinary=min(ordinary,v);v=min([v]+[v//a*b for a,b in sub])
                    anyslot=min(anyslot,v)
                j+=step
            tail=z**j;anyslot=min(anyslot,tail)
            if not odd:ordinary=min(ordinary,tail)
        return ordinary,anyslot
    hs=[val(D,z) for z in roots];assert all(hs);pairs=[cell(z,h) for z,h in zip(roots,hs)];v=X*(D//prod(z**h for z,h in zip(roots,hs)))*prod(a for a,b in pairs)
    ans=min([v]+[v//a*b for a,b in pairs]);cell.cache_clear();return ans

def verify(path):
    d=json.loads(gzip.decompress(path.read_bytes()));assert set(d)=={'p','e','q','cases','ecpp'};p,e,q=d['p'],d['e'],d['q'];assert type(p)==type(e)==int and p in C.ORDER and 2<=e<=7000 and e%2==0
    seen=set()
    @cache
    def prime(z):
        assert type(z)==int and z>2;t=z
        if t>=2**64:
            for a in d['ecpp'][str(z)]:assert a[0]==t;t=C.pc.level(*a)
            seen.add(str(z))
        assert C.pc.prime64(t);return True
    assert prime(q);A=C.sigma(p,e);assert A%q==0 and q not in C.ORDER[:C.ORDER.index(p)+1];c=C.valuation(A,q);f=c;used=set();floors=[]
    while p**e*(A//q**c)*q**f<=B:
        if f%2==0 or q%4==f%4==1:
            s=C.State([(p,e),(q,f)]);S=A*C.sigma(q,f)
            if not s.conflict and S<=2*s.X and s.base<=B:
                row=d['cases'][str(f)];assert set(row)=={'roots','owners','head'};k,o,h=row['roots'],row['owners'],row['head'];C.validate_forest(s,k,o,h,prime);a=C.Forest(s,k,o,h).lower()[0];b=independent(p,e,q,f,k,o,h);assert min(a,b)>B,(p,e,q,f);used.add(str(f));floors.append(len(str(min(a,b)))-1)
        f+=1
    assert used==set(d['cases']) and seen==set(d['ecpp']);return p,e,min(floors,default=2400),len(used)
if __name__=='__main__':
    if not __debug__:raise SystemExit('assertions required')
    for name in sys.argv[1:]:print('PIVOT',verify(Path(name)),flush=True)

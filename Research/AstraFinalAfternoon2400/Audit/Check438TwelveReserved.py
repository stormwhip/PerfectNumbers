"""Independent arithmetic/graph and no-double-charge audit for the six reserved subfibers."""
import gzip,json,sys
from pathlib import Path
from functools import cache
from hashlib import sha256
from math import gcd,prod,lcm
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CheckSevenForestDomains import sig,split

R=Path(__file__).resolve().parents[1]
T=572749682520506652634407616247
Y=T**11; Q=2*Y-1; M=4*Y
B=10**2400; BAD=19
EXPECTED={12,14,16,18,20,24}


def val(n,q):
    d=0
    while n%q==0:
        n//=q;d+=1
    return d


def avoid(n,support):
    while (g:=gcd(n,support))!=1:n//=g
    return n


def main():
    assert __debug__
    assert Q**2%M==1
    raw=(R/'Propagation/Reserved438x12-12-14-16-18-20-24.json.gz').read_bytes()
    assert sha256(raw).hexdigest()=='5b915bd08ba74aa1fa41ec25fc0afdf3a5e77946a9c819da07ade57fd7e570ef'
    obj=json.loads(gzip.decompress(raw)); pivot=27431
    pref=[(7,438),(T,12)]; live,tail=split(pref,{19},pivot)
    assert EXPECTED<=live.keys() and EXPECTED<=set(range(2,27,2)) and 22 not in EXPECTED
    seen=set(); certified=set(); total=0; weakest=None
    for row in obj['records']:
        p=[tuple(x) for x in row['P']]; h=p[-1][1]
        assert h not in seen and p==live[h]; seen.add(h)
        X=prod(z**f for z,f in p); S=prod(sig(z,f) for z,f in p)
        D=lcm(X,S)//X
        assert gcd(X,D)==1 and D%19 and all(f%2==0 for z,f in p)
        node=row['tree']; roots=set(node['roots']); own=dict(node['owners']); head=node['head']
        assert node['type']=='reserve' and 0<head<=4096 and len(roots)==len(node['roots']) and len(own)==len(node['owners'])
        V=roots|own.keys(); assert not roots&own.keys()
        assert not V & set(dict(p)) and 19 not in V and all(z%M!=Q for z in V)
        assert all(D%z==0 for z in roots) and all(D%z for z in own)
        children={z:[] for z in V}
        for z,anchor in own.items():children[anchor].append(z)
        visited=set(); stack=list(roots)
        while stack:
            z=stack.pop();assert z not in visited;visited.add(z);stack.extend(children[z])
        assert visited==V
        certified|={str(z) for z in V if z>=2**64 and z!=T}; total+=len(V)
        pool=D*X*prod(V)
        @cache
        def rebate(n):
            # Congruence representative via ordinary divmod (LOW is self-inverse).
            k=divmod(n*Q,M)[1] or M
            limit=n//Q
            if k>limit:return n
            return k if (limit-k)//M>=1 or n%k==0 else n
        @cache
        def bound(z,req):
            e=2*((req+1)//2); done=0; price=B+1; power=z**e
            while done<head and power<price:
                G=sig(z,e)
                if G%19:
                    done+=1
                    rest=rebate(avoid(G,pool))
                    for w in children[z]:
                        if G%w==0:rest*=bound(w,val(G,w))
                    price=min(price,power*rest)
                e+=2;power*=z*z
            return min(price,power)
        lower=X*Q*rebate(avoid(D,prod(roots)))*prod(bound(z,val(D,z)) for z in roots)
        assert lower>B
        floor=lower*10**6//B
        weakest=floor if weakest is None else min(weakest,floor)
        print('independent reserved terminal',h,floor,flush=True)
    assert seen==EXPECTED and total==2464 and certified==obj['ecpp'].keys()
    assert weakest==4994662
    print('PASS 6 disjoint active secondary fibers; 2464 vertices, 247 ECPP labels verified by author; weakest scaled exact bound',weakest)

if __name__=='__main__':main()

"""Independently check all three support cases and their parity-capacity forests."""
import gzip,json,sys
from hashlib import sha256
from fractions import Fraction
from functools import cache
from math import gcd,lcm,prod
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Forest import PR
from Check31Domains import state, split, vp
from CheckSevenForestDomains import sig
B=10**2400
T=6106505825833677713
P=[(7,48),(T,8)]


def dp(prefix, roots, owners, head, bans, must):
    x,s,ok=state(prefix,bans);assert ok
    d=lcm(x,s)//x;assert gcd(x,d)==1
    pool=x*d*prod(roots)*prod(owners)
    edges={p:[] for p in set(roots)|owners.keys()}
    for child,parent in owners.items():edges[parent].append(child)
    def add(a,b):return (min(B+1,a[0]*b[0]),min(B+1,a[1]*b[0],a[0]*b[1]))
    @cache
    def visit(q,lo):
        ordinary=special=B+1
        for parity in (0,1):
            if parity and q%4!=1:continue
            step=2 if parity==0 else 4; e=lo+((parity-lo)%step);seen=0
            while seen<head and q**e<(special if parity else ordinary):
                power=q**e;g=sig(q,e)
                if gcd(g,prod(bans))==1:
                    seen+=1;y=g//(g&-g);res=y
                    while (v:=gcd(res,pool))>1:res//=v
                    cur=(power*res,)*2
                    for p in edges[q]:
                        if y%p==0:cur=add(cur,visit(p,vp(y,p)))
                    if parity:special=min(special,cur[0]);
                    else:ordinary=min(ordinary,cur[0]);special=min(special,cur[1])
                e+=step
            if parity==0:ordinary=min(ordinary,q**e)
            special=min(special,q**e)
        return ordinary,special
    ans=(1,1)
    for q in roots:
        old=vp(d,q); k=max(old,must.get(q,1)); assert old or q in must
        ans=add(ans,visit(q,k))
    return x*(d//prod(q**vp(d,q) for q in roots))*ans[1]


def main():
    assert __debug__
    live,_=split(P[:1],T,(19,)); assert list(live[8])==P
    I=lambda p,e:Fraction(sig(p,e),p**e)
    z=I(7,48)*I(29,1)*I(61,1)
    assert sig(7,48)%29==sig(T,8)%61==0
    assert z*I(3,2)*I(5,1)>2
    assert sig(11,2)%19==0 and 11%4==3
    assert z*I(3,4)*I(11,4)>2 and z*I(3,2)*I(11,4)*I(13,1)>2
    assert sig(3,2)==13 and sig(3,4)%11==0 and 3%4==3
    b=(H.parent/'Seven/Forest48Eight.json.gz').read_bytes();assert sha256(b).hexdigest()=='55319c6bf427872e94ec6f69139e9a17c59f090c9139dfe77998d0ac9e8a5e11'
    x=json.loads(gzip.decompress(b)); primes=set();cases=set();chains=set()
    for rec in x['records']:
        pp=[tuple(z) for z in rec['P']]; bans=tuple(rec['bad']); present=tuple(rec.get('present',())); lo=dict(rec.get('lo',[]))
        if pp==P and bans==(19,3) and not lo and not present:k=0
        elif pp==P+[(3,2)] and bans==(19,5,11) and not lo and not present:k=2
        else:
            assert pp==P and bans==(19,5,11) and lo=={3:6} and present==(3,);k=6
        assert k not in cases and not rec['unresolved'];cases.add(k); node=rec['tree']
        roots=node['roots']; mg=dict(node['owners']); V=set(roots)|mg.keys()
        assert len(V)==len(roots)+len(node['owners']) and V.isdisjoint(dict(pp)) and V.isdisjoint(bans)
        assert 0<node['head']<=1024 and set(lo)<=set(roots)
        for p in mg:
            path=set()
            while p not in roots:
                assert p in mg and p not in path
                path.add(p);p=mg[p]
        primes|=V|dict(pp).keys()
        X,S,ok=state(pp,bans);D=lcm(X,S)//X;assert ok and all(D%p for p in mg)
        lower=dp(pp,roots,mg,node['head'],bans,lo);assert lower>B
        print('independent case',k,'strict, vertices',len(V),flush=True)
    for q in primes:
        if q>=2**64:
            key=str(q); chains.add(key);rows=x['ecpp'][key];assert rows
            for step in rows:
                assert step[0]==q;q=PR['level'](*step)
        assert PR['prime64'](q)
    assert cases=={0,2,6} and chains==x['ecpp'].keys() and len(chains)==443
    print('PASS independent 3 support domains with Euler capacity, mandatory v3 floor 6 and all 443 ECPP labels')

if __name__=='__main__':main()

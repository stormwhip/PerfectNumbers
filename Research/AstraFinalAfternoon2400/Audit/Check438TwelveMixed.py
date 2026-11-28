"""Independent exact domain walk for five newly proved second fibers in t^12."""
import gzip,json,sys
from hashlib import sha256
from math import gcd,lcm,prod
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckSevenForestDomains import sig,split

B=10**2400
T=572749682520506652634407616247
P=[(7,438),(T,12)]; r=27431; Y=T**11; Q=2*Y-1; MOD=4*Y
CASES=(('Seven/Forest438t12a.json.gz',{4,6},(0,2,0),'564fcefa64ed6d1d0413d8cc2196b73a270bd99d970f7765b6095c84e3f952cd'),
       ('Seven/Forest438t12b.json.gz',{8},(4,34,0),'8f8fdac3c7c7e2d374b5bfc5365690e6eb2762a3f451ea8d81555033abe1a372'),
       ('Propagation/Reserved438x12-10.json.gz',{10},(4,8,51),'e60377ca9694c5d7d88c75a1216e6e2622c9d8363f303517ce1f151cc8e542a8'),
       ('Propagation/Reserved438x12-26.json.gz',{26},(1,0,6),'fc325585a55085567280fdbe9a3bd613384d27aed22266bd62e151582ec435c0'))


def val(n,p):
    h=0
    while n%p==0:n//=p;h+=1
    return h


def state(rows):
    assert len(rows)==len(dict(rows)) and all(h%2==0 and p%MOD!=Q for p,h in rows)
    x=prod(p**h for p,h in rows); s=prod(sig(p,h) for p,h in rows); d=lcm(s,x)//x
    assert s%2 and (s%T**13!=0)
    ok=(s<=2*x and d%19!=0 and x*d<=B and gcd(x,d)==1 and all(val(s,p)<=h for p,h in rows) and val(s,T)==1)
    return x,d,ok


def outside(d,x):
    ceiling=B//x;assert ceiling>=1
    first=d*Q%MOD or MOD
    lower=(d+ceiling-1)//ceiling
    top=d//Q
    start=lower+(first-lower)%MOD
    # The q interval and its complementary cofactor interval are equivalent.
    # Reconstruct both; when both exceed the candidate proof's quota, this is
    # unknown and the checker cannot charge an extra Euler factor here.
    scans=(range(start,top+1,MOD),range(Q,min(ceiling,d)+1,MOD))
    def count(rg):return max(0,(rg.stop-rg.start+MOD-1)//MOD)
    best=min(scans,key=count)
    return count(best)<=64 and all(d%a for a in best)


def main():
    assert __debug__ and Q*Q%MOD==1
    parents,tail=split(P,{19},r)
    assert set(parents)==set(range(2,111,2)) and tail==221
    for name,required,totals,digest in CASES:
        raw=(H.parent/name).read_bytes();assert sha256(raw).hexdigest()==digest
        data=json.loads(gzip.decompress(raw)); used=set();seen=set();counts=[0,0,0]
        mixed=name.startswith('Propagation/')
        def touch(p):
            if p>=2**64 and (not mixed or p!=T):used.add(str(p))
        def walk(rows,node):
            x,d,ok=state(rows);assert ok
            kind=node['type']
            if kind in ('split','split-q1'):
                a=node.get('q',node.get('anchor')); assert a not in dict(rows) and d%a==0 and a%MOD!=Q and a!=19
                touch(a); counts[0]+=1
                if not mixed:
                    branches,_=split(rows,{19},a)
                    c={h:z for h,z in branches.items() if h%2==0}
                else:
                    g=val(d,a);paid=x*d//a**g; h=g+g%2;c={}
                    factor=Q if outside(d,x) else 1
                    while paid*a**h*factor<=B:
                        y=rows+[(a,h)]; xx,dd,ok=state(y)
                        if ok and (xx*dd*Q<=B or not outside(dd,xx)):c[h]=y
                        h+=2
                assert set(map(int,node['cases']))==c.keys()
                for h,y in c.items():walk(y,node['cases'][str(h)])
                return
            if kind=='credits':
                assert mixed; labels=node['labels']; assert len(set(labels))==len(labels)
                assert all(z<Q and d%z==0 and z not in dict(rows) for z in labels)
                for z in labels:touch(z)
                counts[2]+=1
                return
            assert kind=='reserve' and node['head']>0
            counts[1]+=1
            roots=set(node['roots']);own=dict(node['owners']);V=roots|own.keys()
            assert len(V)==len(node['roots'])+len(node['owners']) and V.isdisjoint(dict(rows))
            assert all(d%z==0 for z in roots) and all(d%z for z in own)
            assert all(z!=19 and z%MOD!=Q for z in V)
            for z in V:touch(z)
            for z in own:
                route=set()
                while z not in roots:
                    assert z in own and z not in route
                    route.add(z);z=own[z]
        for rec in data['records']:
            rows=[tuple(x) for x in rec['P']];h=rows[-1][1]
            assert h in required and h not in seen and rows==parents[h];seen.add(h)
            for p,_ in rows:touch(p)
            walk(rows,rec['tree'])
        assert seen==required and used==data['ecpp'].keys() and tuple(counts)==totals
        print('PASS independent complete exact domains',name,'splits/forests/price',counts,'ECPP',len(used),flush=True)

if __name__=='__main__':main()

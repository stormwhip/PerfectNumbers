"""Cold checks for the last delegated fibers of (19,280)."""
from functools import cache
import gzip,json
from hashlib import sha256
from math import prod
from pathlib import Path
import sys
H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path.insert(0,str(R/'Session20261126'))
from PivotCheck import C,B,exact_leaf,floor10
KEY=(19,280);Q=353998162545967;T=1822778365160689


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X


def split(p,q):
    s=C.State(p);assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    h=C.valuation(s.D,q);scale=s.base//q**h;f=h;k={};ds=[];il=[]
    while scale*q**f<=B:
        if not s.possible(q,f,h):il.append(f)
        elif dead(C.State(p+[(q,f)])):ds.append(f)
        else:k[str(f)]=p+[(q,f)]
        f+=1
    return k,ds,il,f


def reader(name):
    raw=(H/name).read_bytes();a=json.loads(gzip.decompress(raw)); assert (a['p'],a['e'],a['pivot'])==(*KEY,Q)
    book=a['ecpp'];used=set()
    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if n>=2**64:
            used.add(str(q));x=book[str(q)];assert x
            for row in x:
                assert row[0]==n and n>=2**64
                n=C.pc.level(*row)
        assert C.pc.prime64(n);return True
    assert prime(KEY[0]) and prime(Q) and Q.bit_length()==49
    top,d,i,t=split([KEY],Q)
    assert len(top)==29
    print('DOMAIN',list(top),'direct',len(d),'incompatible',len(i),'tail',t,flush=True)
    return a,prime,used,sha256(raw).hexdigest(),top


def forest(p,t,prime):
    assert t['type']=='forest' and set(t)=={'type','roots','owners','head'}
    s=C.State(p); assert not dead(s)
    k,o,h=(t[z] for z in ('roots','owners','head'));C.validate_forest(s,k,o,h,prime)
    a=C.Forest(s,k,o,h).lower()[0];b=exact_leaf(p,k,o,h);assert min(a,b)>B
    return floor10(min(a,b))


def full22():
    d,prime,used,sha,top=reader('Fiber22.json.gz')
    assert set(d)=={'p','e','pivot','cases','ecpp'} and set(d['cases'])=={'22'}
    t=d['cases']['22'];assert t['type']=='split' and set(t)=={'type','q','cases'} and t['q']==T and T.bit_length()==51 and prime(T)
    c,dc,il,tail=split(top['22'],T);assert len(c)==26 and tail==71 and set(c)==set(t['cases'])
    floor=min(forest(p,t['cases'][f],prime) for f,p in c.items());assert used==set(d['ecpp'])
    print('COMPLETE 22',list(c),'direct',len(dc),'incompatible',len(il),'tail',tail,'forest minimum',floor,'SHA256',sha,flush=True)


def deep2():
    d,prime,used,sha,top=reader('Paths2.json.gz');assert set(d)=={'p','e','pivot','paths','ecpp'}
    k=set();f=[]
    for key,r in d['paths'].items():
        p=list(map(tuple,r['parts'])); t=tuple(e for q,e in p)
        assert set(r)=={'parts','tree'} and p[:2]==top['2'] and t not in k and key==','.join(map(str,t))
        assert all(prime(q) for q,_ in p)
        for j in range(1,len(p)):
            c,*_=split(p[:j],p[j][0]);assert c[str(p[j][1])]==p[:j+1]
        k.add(t);f.append(forest(p,r['tree'],prime))
        print('CONDITIONAL 2',t,'floor',f[-1],flush=True)
    assert used==set(d['ecpp']) and len(k)==77
    print('CONDITIONAL 2',len(k),'strict leaves, minimum',min(f),'SHA256',sha,flush=True)


if __name__=='__main__':
    assert __debug__
    if sys.argv[1:]==['--deep2']:deep2()
    else:
        assert not sys.argv[1:];full22()

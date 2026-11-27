"""Cold partial tree for (19,58), only the exact first Euler fiber."""
from functools import cache
import gzip,json
from hashlib import sha256
from math import prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126')]
from PivotCheck import C,B,exact_leaf,floor10
from PrefixPrice import excludes

KEY=(19,58)
Q=155306613932666028670208812450645212905178047040045530562317564121001023821
T=25884435655444338111701468741774202150863007840007588427052927353500170637
U=3291622576015727423
V=804577


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,e) for q,e in s.rows.items())>2*s.X


def split(p,q):
    s=C.State(p); assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    f=h=C.valuation(s.D,q); scale=s.base//q**h; kids={}; direct=[]; forbidden=[]
    while scale*q**f<=B:
        if not s.possible(q,f,h):forbidden.append(f)
        elif dead(C.State(p+[(q,f)])):direct.append(f)
        else:kids[str(f)]=p+[(q,f)]
        f+=1
    return kids,direct,forbidden,f


def verify():
    assert __debug__ and Q.bit_length()==247 and T.bit_length()==244
    raw=(H/'EulerF1.json.gz').read_bytes(); d=json.loads(gzip.decompress(raw)); used=set(); book=d['ecpp']
    assert set(d)=={'p','e','pivot','tree','ecpp'} and (d['p'],d['e'],d['pivot'])==(*KEY,Q)
    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if n>=2**64:
            used.add(str(q)); chain=book[str(q)]; assert chain
            for a in chain:
                assert a[0]==n and n>=2**64
                n=C.pc.level(*a)
        assert C.pc.prime64(n);return True
    assert prime(KEY[0]) and prime(Q) and prime(T)
    pre,direct,illegal,tail=split([KEY],Q)
    assert list(pre)==['1','2','4','5','6','8','9','10','12','13','14'] and (len(direct),len(illegal),tail)==(12,8,32)
    print('FIRST LIVE',list(pre),'direct',direct,'incompatible',illegal,'tail',tail,flush=True)
    assert d['tree']['q']==T and C.State(pre['1']).fixed_euler
    sub,ds,il,tail=split(pre['1'],T)
    assert (list(sub),len(ds),len(il),tail)==(['2','4','6','8','10','12','14'],8,15,31)
    print('SECOND LIVE',list(sub),'direct',ds,'incompatible',len(il),'tail',tail,flush=True)
    results={}; opens=[]; prices={}; floors=[]
    def walk(p,t):
        s=C.State(p); assert not dead(s) and s.fixed_euler
        ex=tuple(f for _,f in p)
        if t is None:opens.append(ex);return False
        if t['type']=='split':
            assert set(t)=={'type','q','cases'} and prime(t['q'])
            ks,_,_,_=split(p,t['q']); assert set(ks)==set(t['cases'])
            return all([walk(pp,t['cases'][f]) for f,pp in ks.items()])
        if t['type']=='price':
            assert set(t)=={'type','targets'} and all(prime(q) for q,_ in p)
            ans=excludes(p,s.bad,t['targets']);assert ans[1]==[0,0,0]
            prices[ex]=ans[0];return True
        assert t['type']=='forest' and set(t)=={'type','roots','owners','head'}
        k,o,h=(t[a] for a in ('roots','owners','head')); C.validate_forest(s,k,o,h,prime)
        a=C.Forest(s,k,o,h).lower()[0];b=exact_leaf(p,k,o,h);assert a>B and b>B
        floors.append(floor10(min(a,b)));return True
    assert d['tree']['type']=='split' and set(d['tree'])=={'type','q','cases'} and set(d['tree']['cases'])==set(sub)
    for f,p in sub.items():results[int(f)]=walk(p,d['tree']['cases'][f])
    assert used==set(book)
    full=sorted(f for f,done in results.items() if done)
    assert full==[4,8,12,14] and len(opens)==11 and len(prices)==32
    assert prices[(58,1,12)]==4
    print('SECOND FULL',full,'price leaves',len(prices),'dual forests',len(floors),'forest minimum floor',min(floors),'SHA256',sha256(raw).hexdigest(),flush=True)
    print('OPEN EXACT PATH EXPONENTS',opens,flush=True)

if __name__=='__main__':verify()

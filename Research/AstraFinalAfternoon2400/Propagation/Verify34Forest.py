"""Canonical (7,34) exact-first forests, with fresh finite domain and dual arithmetic."""
from functools import cache
from hashlib import sha256
from math import prod
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(H.parent/'Seven'),str(R/'RootFiveNext'),str(R/'Session20261126'),str(R/'Night2400/A')]
from VerifyForest import child_domain, exact_state, C, B
from MaskedForest import exact_absence_bound
from PrimeCheck import prime64,level
from Propagation import sigma,val

q=77192844961; P=[(7,34)]; F=(29,2801,4733,2127431041,q)
PACKS={'orbit48root34a':(69,73,74,76,77,80,81,84,85,86,88,90,92,93,94,96,97,98,100,101,102,104,105,106,108),
       'orbit48root34b':(5,13,20,25,29,33,38,41,44,49,50,56,57,61,62,64,65,68),
       'orbit48root34c':(32,37,45,70,82),
       'orbit48root34d':(26,48),
       'orbit48root34e':(12,),
       'orbit48root34f':(54,)}


def replay(path,exponents):
    assert __debug__
    assert all(prime64(p) for p in (7,19,*F)) and prod(F)==sigma(7,34) and val(sigma(7,34),q)==1
    cases,tail=child_domain(P,(19,),q)
    assert len(cases)==78 and tail==217 and max(map(int,cases))==108
    raw=path.read_bytes();obj=json.loads(gzip.decompress(raw));assert set(obj)=={'records','ecpp'}
    cert=obj['ecpp']; reached=set(); done=[]; weakest=None
    @cache
    def prime(p):
        if p<2**64:return prime64(p)
        x=p;k=str(p);reached.add(k)
        for row in cert[k]:assert x==row[0];x=level(*row)
        return prime64(x)
    for z in obj['records']:
        assert set(z)=={'P','bad','tree','unresolved'} and not z['unresolved'] and z['bad']==[19]
        rows=list(map(tuple,z['P']));assert len(rows)==2 and rows[0]==P[0] and rows[1][0]==q
        f=rows[1][1];assert rows==cases[str(f)] and f not in done
        done.append(f)
        s=C.State(rows); ok,X,D,n=exact_state(rows,(19,)); assert ok and not s.conflict and (s.X,s.D)==(X,D)
        t=z['tree'];assert set(t)=={'type','roots','owners','head'} and t['type']=='forest'
        roots,edges,head=(t[k] for k in ('roots','owners','head'))
        C.validate_forest(s,roots,edges,head,prime)
        u=C.Forest(s,roots,edges,head).lower()[0]; v=exact_absence_bound(rows,roots,edges,head,(19,),B)
        value=min(u,v);assert value>B
        weakest=value if weakest is None else min(weakest,value)
        print('PASS first',f,'roots / owners',len(roots),len(edges),'floor',len(str(value))-1,flush=True)
    assert tuple(done)==exponents and reached==set(cert) and weakest is not None
    print('PASS (7,34)',len(done),'of',len(cases),'strict tail',tail,'ECPP',len(reached),
          'scaled minimum',weakest*10**6//B,'sha256',sha256(raw).hexdigest(),flush=True)
    return set(done)

if __name__=='__main__':
    all_done=set()
    for tag in sys.argv[1:] or PACKS:
        r=replay(H/f'Reserved438x12-{tag}.json.gz',PACKS[tag]); assert not all_done&r;all_done|=r
    dom,tail=child_domain(P,(19,),q)
    remainder=sorted(set(map(int,dom))-all_done)
    if not sys.argv[1:]:
        assert len(all_done)==52 and remainder==[1,2,4,6,8,9,10,14,16,18,21,22,24,28,30,34,36,40,42,46,52,58,60,66,72,78]
    print('REMAINING exact firsts',remainder,flush=True)

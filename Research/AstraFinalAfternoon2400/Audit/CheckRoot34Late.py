"""Independent disjoint range/abundance and two new first forests for canonical (7,34)."""
from hashlib import sha256
from fractions import Fraction
from math import prod
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import split,B
from Check31Forest import PR,forest
from CheckSevenForestDomains import sig
D=H.parent/'Propagation';T=77192844961;P=((7,34),); earlier=set()

def packet(name,digest=None):
    v=(D/f'Reserved438x12-orbit48root34{name}.json.gz').read_bytes()
    if digest:assert sha256(v).hexdigest()==digest
    return json.loads(gzip.decompress(v))

def main():
    assert __debug__
    dom,tail=split(P,T,(19,));assert tail==217 and len(dom)==78
    for tag in 'abcd':earlier.update(r['P'][1][1] for r in packet(tag)['records'])
    for tag,f,primecount,digest in [('e',12,1000,'6410824091d7f8fbbb13ea2103d104aae720b395d2f6fbdae33e3e72668c0145'),('f',54,1177,'d91367f01a44788df07baca430724c232955e6ed950c0a9dd0f4009b31fc10c5')]:
        k=packet(tag,digest);r,=k['records'];assert tuple(map(tuple,r['P']))==dom[f] and f not in earlier and r['bad']==[19]
        assert forest(dom[f],r['tree'],(19,))>B
        assert len(k['ecpp'])==primecount
        earlier.add(f)
    f=(29,2801,4733,2127431041,T)
    assert prod(f)==sig(7,34) and all(PR['prime64'](p) for p in f)
    fixed_min=lambda ps:prod(Fraction(sig(p,e),p**e) for p,e in ps.items())
    for e,labels in ((9,(5,17,31,811)),(14,(5,61,151,907,4723)),(21,(11,17,23,89))):
        assert all(PR['prime64'](p) and sig(T,e)%p==0 for p in labels)
        z=dict(dom[e]);z[3]=2
        for p in set(f)|set(labels):z.setdefault(p,2 if p%4==3 else 1)
        assert fixed_min(z)>2
    assert all(sig(T,e)%3==0 for e in (2,8,14))
    d=packet('m','eae4b5ec6b4ebdc8c5b354f1f75d171744c449824fada8f857c13f6d46b60787')
    bins=set()
    for a in d['records']:
        p=tuple(map(tuple,a['P']));e=p[1][1]; assert p[:2]==dom[e]
        lo=dict(a['lo']);z=dict(p);k=0 if 3 in a['bad'] and e in (9,21) else z[3] if 3 in z else lo[3]
        assert (e,k) not in bins;bins.add((e,k))
        for r in a['roots']:
            assert r not in z and prod(sig(i,j) for i,j in p)%r==0
            z[r]=2 if r%4==3 else 1
        z.update(lo)
        for q in set(a['bad'])-{19}-({3} if k==0 else set()):
            assert q not in z and fixed_min(z|{q:(2 if q%4==3 else 1)})>2
    assert bins=={(2,2),(2,4),(8,2),(8,4),(9,0),(21,0)} and len(d['ecpp'])==1579
    later={2,8,9,14,21};assert not later&earlier
    all_done=earlier|later;assert len(all_done)==57 and len(dom.keys()-all_done)==21
    print('PASS independent compulsory parity/abundance scopes for 5 support splits and strict DP for first12/54; 57/78 union')

if __name__=='__main__':main()

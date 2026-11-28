"""Independent exact (7,48) second-fiber forest/price union and certificate domains."""
from hashlib import sha256
from pathlib import Path
from math import gcd,lcm,prod
from fractions import Fraction
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import state,split,B
from Check31Forest import PR,forest
from CheckSevenForestDomains import sig
T=6106505825833677713
A={2:518019223567,10:531983}
first={2:set(range(76,97,2)),10:set(range(104,171,2))}
second={2:{74},10:{92,98,100,102}}
PACKS=(('orbit48sq',2,tuple(range(32,73,2)),1299,'6e15628e47f40b77b9be338808ea7de296bd441b8b694d028e0bccd382d9c437'),
       ('orbit48sqmid',2,(14,20,24,26,28,30),1180,'14d863e14df2f448059cf3e13b37b38f6bd885a145aa8edd852e15b1d1a460ce'),
       ('orbit48',10,(84,86,88,90,94,96),1167,'50cd57b092351d72b2a85cde87a6dd832eccf5580cad3f472980a3eb475520dc'),
       ('orbit48ten',10,(38,44,48,50,54,56,60,62,64,66,68,70,72,74,76,78,80,82),1183,'3c920b0b7a74aec6b7fd840d211b9ff1fc0c8d6a5e3a0303c243e0be7c600014'),
       ('orbit48tenlow',10,(14,20,22,24,26,32,34),1175,'48a3419388bae5eed977223a87c6af414638e6db041f67a6b154380cc86211e7'),
       ('orbit48tenfresh',10,(30,40),1162,'dda375d32a8338e71e791abd1557251d7494c1ecb5e749afd02a222f56ca1efe'))


def packet(tag,digest=None):
    p=H.parent/f'Propagation/Reserved438x12-{tag}.json.gz';b=p.read_bytes()
    if digest:assert sha256(b).hexdigest()==digest
    return json.loads(gzip.decompress(b))


def main():
    assert __debug__
    tails={};domains={}
    for f in A:
        domains[f],tails[f]=split(((7,48),(T,f)),A[f],(19,))
    assert tails=={2:195,10:344} and [len(domains[f]) for f in (2,10)]==[48,85]
    accounted={k:first[k]|second[k] for k in A}
    assert all(first[k].isdisjoint(second[k]) and accounted[k]<=domains[k].keys() for k in A)
    for tag,f,hs,k,digest in PACKS:
        z=packet(tag,digest); seen=set(); vs=set()
        for rec in z['records']:
            row=tuple(map(tuple,rec['P'])); h=row[-1][1]
            assert row==domains[f][h] and rec['bad']==[19] and not rec['unresolved'] and h not in vs
            vs.add(h); x,y,ok=state(row,(19,));M=lcm(x,y);tr=rec['tree']
            assert ok and tr['type']=='forest' and 0<tr['head']<=1024
            roots,own=set(tr['roots']),dict(tr['owners']);v=roots|own.keys()
            assert len(v)==len(tr['roots'])+len(tr['owners']) and v.isdisjoint(dict(row)) and 19 not in v
            assert all(M%p==0 for p in roots) and all(M%p for p in own)
            for p in own:
                loop=set()
                while p not in roots:
                    assert p in own and p not in loop
                    loop.add(p);p=own[p]
            seen|={str(p) for p in v|dict(row).keys() if p>=2**64}
        assert vs==set(hs) and seen==z['ecpp'].keys() and len(seen)==k
        assert not accounted[f]&vs; accounted[f]|=vs
        print('PASS byte-bound exact branch and forest scope',tag,len(vs),'large reached labels',len(seen),flush=True)
    assert len(accounted[2])==39 and len(accounted[10])==71
    assert domains[2].keys()-accounted[2]=={2,4,6,8,10,12,16,18,22}
    assert domains[10].keys()-accounted[10]=={2,4,6,8,10,12,16,18,28,36,42,46,52,58}
    no3=packet('orbit48no3');assert len(no3['records'])==1
    row=no3['records'][0];assert tuple(map(tuple,row['P']))==((7,48),(T,2)) and row['bad']==[19,3] and not row['unresolved']
    node=row['tree']; assert forest(tuple(map(tuple,row['P'])),node,(19,3))>B
    print('PASS independent disjoint condition union 39/48 and 71/85; t^2 no3 support bound strict')

if __name__=='__main__':main()

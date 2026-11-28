"""Independent exact all-domain reconstruction and forest proof for fifty (7,34) firsts."""
from functools import cache
from hashlib import sha256
from math import prod
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import split,geometric,B
from Check31Forest import PR,forest

T=77192844961
KS=((25,995,'746b58fb4ad9843d3e79b57c37cd972e2548bd5405a3e81b8012a62b49c4a143'),(18,1275,'30b0597271f68d4a626b9c9f9f7584e34d2e31d38753d2bce5da38e89a6c6e91'),(5,1300,'2708b79a47909840568f3240ff884e56760efc767226f6340ff925304ad624b9'),(2,1285,'71fca3de26e41821f8a61a08419ee9588ce0156a1637eb535ed23cce4b7ee111'))


def main():
    assert __debug__
    f=(29,2801,4733,2127431041,T)
    assert all(PR['prime64'](p) for p in f) and geometric(7,34)==prod(f)
    domain,tail=split(((7,34),),T,(19,))
    assert len(domain)==78 and max(domain)==108 and tail==217
    union=set()
    for tag,(expected,chains,digest) in zip('abcd',KS):
        name=H.parent/f'Propagation/Reserved438x12-orbit48root34{tag}.json.gz'
        data=name.read_bytes();assert sha256(data).hexdigest()==digest
        d=json.loads(gzip.decompress(data));used=set();vals=set()
        @cache
        def check(p):
            if p>=2**64:
                k=str(p);used.add(k);ct=d['ecpp'][k]; assert ct
                for step in ct:assert step[0]==p;p=PR['level'](*step)
            assert PR['prime64'](p)
        for row in d['records']:
            a=tuple(map(tuple,row['P'])); h=a[-1][1];assert a==domain[h] and row['bad']==[19] and not row['unresolved']
            assert h not in vals; vals.add(h)
            K=row['tree']; assert K['type']=='forest'
            for p in set(K['roots'])|{u for u,_ in K['owners']}|dict(a).keys():check(p)
            L=forest(a,K,(19,));assert L>B
        assert len(vals)==expected and len(used)==chains and used==d['ecpp'].keys() and not union&vals
        union|=vals;print('PASS independent forest packet',tag,expected,chains,flush=True)
    assert len(union)==50 and domain.keys()-union=={1,2,4,6,8,9,10,12,14,16,18,21,22,24,28,30,34,36,40,42,46,52,54,58,60,66,72,78}
    print('PASS exact all-domain at root 7 e34; 50 of 78 first values excluded, raw tail217')

if __name__=='__main__':main()

"""Replay scoped exact trees with explicit unresolved leaves (never a full key by default)."""
from collections import Counter
from functools import cache
import gzip
from hashlib import sha256
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path[:0]=[str(H),str(H/'C7')]
from VerifyFibers import C,B,live,exact_leaf
from JointValuation import excludes as stock_price
from PrefixPrice import excludes as prefix_price
from InteriorPrice import check as interior_price


def replay(path):
    assert __debug__
    raw=path.read_bytes();d=json.loads(gzip.decompress(raw))
    assert set(d)=={'p','e','pivot','cases','ecpp'}
    p,e,q=d['p'],d['e'],d['pivot'];assert p in C.ORDER and type(e)==int and 0<e<=7000 and e%2==0
    used=set();counts=Counter();unresolved=[]

    @cache
    def prime(z):
        assert type(z)==int and z>2
        t=z
        if z>=2**64:
            key=str(z);used.add(key);chain=d['ecpp'][key];assert chain
            for row in chain:
                assert row[0]==t and t>=2**64
                t=C.pc.level(*row)
        assert C.pc.prime64(t)
        return True

    def parts(P,z):
        s=C.State(P);assert live(s) and prime(z) and z not in s.rows and z not in s.bad and s.D%z==0
        a=C.valuation(s.D,z);f=a;size=s.base;out={}
        while size<=B:
            if s.possible(z,f,a):
                Q=P+[(z,f)]
                if live(C.State(Q)):out[str(f)]=Q
                else:counts['direct']+=1
            f+=1;size*=z
        return out,f

    def walk(P,node):
        s=C.State(P);assert live(s);t=node['type'];counts[t]+=1
        if t=='open':
            assert set(node)=={'type'};unresolved.append(P)
        elif t=='split':
            assert set(node)=={'type','q','cases'};cs,_=parts(P,node['q']);assert set(cs)==set(node['cases'])
            for a,J in cs.items():walk(J,node['cases'][a])
        elif t=='forest':
            assert set(node)=={'type','roots','owners','head'}
            k,o,h=(node[x] for x in ('roots','owners','head'));C.validate_forest(s,k,o,h,prime)
            assert C.Forest(s,k,o,h).lower()[0]>B and exact_leaf(P,k,o,h)>B
        elif t=='interior_price':
            assert set(node)=={'type','targets','witnesses'} and all(prime(z) for z,_ in P)
            price, detail=interior_price(P,s.bad,node['targets'],node['witnesses'])
            print('INTERIOR PRICE',[(z,f) for z,f in P],price,detail,flush=True)
        else:
            assert t in ('price','prefix_price') and set(node)=={'type','targets'}
            assert all(prime(z) for z,_ in P)
            checker=stock_price if t=='price' else prefix_price
            checker(P,s.bad,node['targets'])

    domain,tail=parts([(p,e)],q);assert set(d['cases'])<=set(domain) and d['cases']
    for f,node in d['cases'].items():walk(domain[f],node)
    assert used==set(d['ecpp'])
    remaining=set(map(int,set(domain)-set(d['cases'])))|{P[1][1] for P in unresolved}
    return {'key':[p,e],'pivot':str(q),'tail':tail,'domain':sorted(map(int,domain)),
            'covered':sorted(set(map(int,domain))-remaining),'open':sorted(remaining),
            'open_paths':unresolved,'stats':dict(counts),'ecpp':len(used),'sha256':sha256(raw).hexdigest()}


if __name__=='__main__':
    print(json.dumps(replay(Path(sys.argv[1]))),flush=True)

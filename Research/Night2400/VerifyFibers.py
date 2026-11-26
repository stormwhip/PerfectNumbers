"""Independent replay entry point for exact partial or total first-pivot packs.

JSON gzip fields: p, e, pivot, ecpp, cases. A missing compatible fiber is
reported OPEN; never treat a PASS for some fibers as a complete key. Proof
leaf arithmetic uses frozen code from the published GitHub baseline.
"""
import argparse
from functools import cache
import gzip
from hashlib import sha256
import json
from math import prod
from pathlib import Path
import sys

R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'Session20261126'),str(R/'FinalSprint')]
from PivotCheck import C, B, exact_leaf
from JointValuation import excludes


def live(s):
    return not s.conflict and s.base <= B and prod(C.sigma(z,f) for z,f in s.rows.items()) <= 2*s.X


def verify(path):
    assert __debug__, 'assertions are required'
    raw=path.read_bytes(); d=json.loads(gzip.decompress(raw))
    assert set(d)=={'p','e','pivot','ecpp','cases'}
    p,e,q=d['p'],d['e'],d['pivot']
    assert p in C.ORDER and type(e)==int and 0<e<=7000 and e%2==0
    used=set(); stats=[0,0,0,0]; price=[]

    @cache
    def prime(x):
        assert type(x)==int and x>2
        u=x
        if u>=2**64:
            key=str(x); used.add(key)
            for row in d['ecpp'][key]:
                assert row[0]==u
                u=C.pc.level(*row)
        assert C.pc.prime64(u)
        return True

    def children(P,t):
        s=C.State(P); assert live(s) and prime(t) and t not in s.rows and t not in s.bad and s.D%t==0
        c=C.valuation(s.D,t); scale=s.base//t**c
        admissible={}; f=c
        while scale*t**f<=B:
            if s.possible(t,f,c):
                child=P+[(t,f)]
                if live(C.State(child)): admissible[str(f)]=child
                else: stats[2]+=1
            f+=1
        return admissible,f

    def walk(P,node):
        s=C.State(P); assert live(s)
        if node['type']=='split':
            assert set(node)=={'type','q','cases'}
            kids,_=children(P,node['q']); assert set(kids)==set(node['cases'])
            stats[1]+=1
            for v,k in kids.items():walk(k,node['cases'][v])
        elif node['type']=='forest':
            assert set(node)=={'type','roots','owners','head'}
            k,o,h=node['roots'],node['owners'],node['head']
            C.validate_forest(s,k,o,h,prime)
            assert C.Forest(s,k,o,h).lower()[0]>B and exact_leaf(P,k,o,h)>B
            stats[0]+=1
        else:
            assert node['type']=='price' and set(node)=={'type','targets'} and all(prime(z) for z,_ in P)
            price.append(excludes(P,s.bad,node['targets']))
            stats[3]+=1

    kids,tail=children([(p,e)],q)
    assert 0<len(d['cases']) and set(d['cases'])<=set(kids)
    for v,node in d['cases'].items(): walk(kids[v],node)
    assert used==set(d['ecpp'])
    return {'key':[p,e],'pivot':str(q),'domain':sorted(map(int,kids)),
            'covered':sorted(map(int,d['cases'])),'open':sorted(map(int,set(kids)-set(d['cases']))),
            'first_out_of_size':tail,'counts_forest_split_direct_price':stats,'price_receipts':price,
            'sha256':sha256(raw).hexdigest()}


def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('packet',nargs='+',type=Path)
    for path in a.parse_args().packet: print(json.dumps(verify(path)),flush=True)


if __name__=='__main__':main()

"""Rebuild hybrid exact trees. A price leaf is a theorem on its full path, not an oracle bit."""
from pathlib import Path
from functools import cache
from math import prod
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parent/'Session20261126')]
from PivotCheck import C,B,exact_leaf
from JointValuation import excludes

def verify(path,check_prices=True):
    assert __debug__; d=json.loads(gzip.decompress(path.read_bytes()));p,e=d['p'],d['e'];assert p in C.ORDER and type(e)==int and 0<e<=7000 and not e%2
    used=set();counts=[0,0,0,0];receipts=[]
    @cache
    def prime(q):
        assert type(q)==int and q>2;v=q
        if q>=2**64:
            used.add(str(q))
            for row in d['ecpp'][str(q)]:assert row[0]==v;v=C.pc.level(*row)
        assert C.pc.prime64(v);return True
    def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,j) for q,j in s.rows.items())>2*s.X
    def walk(P,r):
        s=C.State(P);assert not dead(s)
        if r['type']=='forest':
            k,o,h=r['roots'],r['owners'],r['head'];C.validate_forest(s,k,o,h,prime)
            assert C.Forest(s,k,o,h).lower()[0]>B and exact_leaf(P,k,o,h)>B;counts[0]+=1;return
        if r['type']=='price':
            assert set(r) in ({'type'},{'type','targets'}) and all(prime(q) for q,_ in P);counts[3]+=1
            if check_prices:receipts.append((P,excludes(P,s.bad,r.get('targets'))))
            return
        assert r['type']=='split';q=r['q'];assert prime(q) and q not in s.rows and q not in s.bad and s.D%q==0;v=C.valuation(s.D,q);scale=s.base//q**v;f=v;seen=set();counts[1]+=1
        while scale*q**f<=B:
            if s.possible(q,f,v):
                P2=P+[(q,f)]
                if dead(C.State(P2)):counts[2]+=1
                else:seen.add(str(f));walk(P2,r['cases'][str(f)])
            f+=1
        assert seen==set(r['cases'])
    walk([(p,e)],d['tree']);assert used==set(d['ecpp']);return p,e,counts,receipts
if __name__=='__main__':
    for fn in sys.argv[1:]:print(verify(Path(fn)),flush=True)

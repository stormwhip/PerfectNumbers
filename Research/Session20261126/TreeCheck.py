"""Replay total multilevel exact exponent trees; never lift exact-state proofs."""
from pathlib import Path
import sys,gzip,json
from functools import cache
from math import gcd,prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from PivotCheck import C,B,exact_leaf

def verify(path):
    x=json.loads(gzip.decompress(path.read_bytes()));assert set(x)=={'p','e','ecpp','tree'};p,e=x['p'],x['e'];assert p in C.ORDER and type(e)==int and 0<e<=7000 and e%2==0
    used=set();stats=[0,0,0]
    @cache
    def prime(z):
        assert type(z)==int and z>2;u=z
        if u>=2**64:
            used.add(str(z))
            for a in x['ecpp'][str(z)]:assert a[0]==u;u=C.pc.level(*a)
        assert C.pc.prime64(u);return True
    def impossible(s):return s.conflict or s.base>B or prod(C.sigma(z,f) for z,f in s.rows.items())>2*s.X
    def walk(parts,node):
        s=C.State(parts);assert not impossible(s)
        if node['type']=='forest':
            assert set(node)=={'type','owners','roots','head'};k,o,h=node['roots'],node['owners'],node['head'];C.validate_forest(s,k,o,h,prime);assert C.Forest(s,k,o,h).lower()[0]>B and exact_leaf(parts,k,o,h)>B;stats[0]+=1;return
        assert set(node)=={'type','q','cases'} and node['type']=='split';z=node['q'];assert prime(z) and z not in s.rows and z not in s.bad and s.D%z==0;h=C.valuation(s.D,z);start=s.base//z**h;f=h;seen=set();stats[1]+=1
        while start*z**f<=B:
            if s.possible(z,f,h):
                new=parts+[(z,f)];sub=C.State(new)
                if not impossible(sub):walk(new,node['cases'][str(f)]);seen.add(str(f))
                else:stats[2]+=1
            f+=1
        assert seen==set(node['cases'])
    walk([(p,e)],x['tree']);assert used==set(x['ecpp']);return p,e,stats
if __name__=='__main__':
    if not __debug__:raise SystemExit('assertions required')
    for f in sys.argv[1:]:print(verify(Path(f)),flush=True)

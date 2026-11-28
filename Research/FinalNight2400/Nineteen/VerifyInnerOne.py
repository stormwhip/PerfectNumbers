"""Exact ordinary three-target price for unique Euler exponent at 23773."""
from pathlib import Path
import sys,gzip,json
P=Path(__file__).resolve().parent;sys.path[:0]=[str(P.parents[1]/'Session20261126'),str(P.parents[1]/'FinalSprint')];from PivotCheck import C;import JointValuation as J
if __name__=='__main__':
    assert __debug__;D=json.loads(gzip.decompress((P/'Packet28Inner.json.gz').read_bytes()));Q=D['Q'];parts=[(19,282),(1735317810514627,10),(8383027,28),(Q,2),(23773,1)]
    for i,(z,h) in enumerate(parts):
        if z>=2**64:
            n=z
            for row in D['ecpp'][str(z)]:assert n==row[0];n=C.pc.level(*row)
            assert C.pc.prime64(n)
        else:assert C.pc.prime64(z)
        if i:assert C.State(parts[:i]).D%z==0
    assert not C.State(parts).conflict
    out=J.excludes(parts,(),[0,2,3]);assert out==(122,[0,0,0]);print('PASS 282 secondary 28, 23773^1 forbidden; exact three-target exceptions:',out[0],flush=True)

"""Additional exact 618 applications of frozen compulsory-credit proof."""
import sys,json
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import Verify618Credit as C

if __name__=='__main__':
    pack=json.loads((P/'Extra618.json').read_bytes()); assert set(pack)=={'22','24','28'}
    def prove():
        for f,zz in pack.items():
            S=C.sig(C.t,int(f));r=1
            for label,chain in zz.items():
                q=int(label);r*=q
                for row in chain:assert row[0]==q;q=C.pc.level(*row)
                assert C.pc.prime64(q)
            assert r==S
    C.Z={int(f):sorted(map(int,zz)) for f,zz in pack.items()};C.primes=prove;C.main()

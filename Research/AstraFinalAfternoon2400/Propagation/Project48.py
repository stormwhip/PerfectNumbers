"""Cold replay and exact disjoint projection for (7,48), t^2 and t^10."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import Verify48Price as V
import Verify48Overlap as C
import Verify48Forest as F
import Verify48Masks as M
import Verify48StrongMasks as S


def domains():
    U={}; blocks={}
    for f in (2,10):
        rows=[(V.P,48),(V.T,f)]; q=V.PIVOT[f]
        h,tail=V.domain(rows,q)
        U[f]=set(h); blocks[f]=[]
        assert h==list(range(2,{2:97,10:171}[f],2)) and tail=={2:195,10:344}[f]
    return U,blocks


def main(cold=True):
    assert __debug__
    domain,A=domains()
    def take(f,values):
        s=set(values); assert s<=domain[f] and all(not s&v for v in A[f]); A[f].append(s)
    if cold:
        V.main()
        for f,hs in C.EXTRA.items():
            for h,zz in hs.items():C.check(f,h,zz)
    for f in (2,10):
        take(f,V.PUBLISH[f]);take(f,C.EXTRA[f])
    for label,values in F.PACKS.items():
        if cold:F.replay(F.forest_file(label),values)
        for f in (2,10):take(f,[h for u,h in values if u==f])
    if cold:M.replay(H/'Reserved438x12-orbit48no3.json.gz',[(0,0)])
    masks=set()
    for tag,expected in S.PACKS.items():
        if cold:S.verify(F.forest_file(tag),expected)
        for h,m in expected:
            assert h in domain[2] and not any(h in a for a in A[2]) and (h,m) not in masks
            masks.add((h,m))
    fully={h for h,m in masks if (h,2) in masks and (h,6) in masks}
    assert fully=={2,4,6,8,10,16,18,22}
    take(2,fully)
    assert masks-{(h,m) for h in fully for m in (2,6)}=={(12,6)}
    assert domain[2]-set().union(*A[2])=={12}
    print('Before final square supplement, h=12 requires exact v_3=2.',flush=True)
    for f in (2,10):
        got=set().union(*A[f]);print('48 first',f,'proof count',len(got),'remaining',sorted(domain[f]-got),flush=True)
    unclosed=domain[10]-set().union(*A[10]);assert unclosed<= {2,10,36,46}
    print('This projection excludes the final square supplement; use Full48Square.py for t^2.',flush=True)

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--sets-only'])
    main(not sys.argv[1:])

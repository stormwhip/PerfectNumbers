"""Replay three complete canonical support masks at exact (19,30).

The masks use only verified ordinary first fibers and their scoped complement;
no historical support projection for this exact key is assumed.
"""
from functools import cache
import gzip,json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from VerifyFibers import C,B,live,verify
sys.path.insert(0,str(H.parent/'Nov25/Compose'))
from IndependentForest import replay as other

MASKS=(21,89,153)
KEY=(19,30)


def replay():
    assert __debug__
    orig=verify(H/'Fibers19x30.json.gz'); assert tuple(orig['key'])==KEY
    root=int(orig['pivot']);domain=set(orig['open'])
    assert domain=={1,2,12,18}
    d=json.loads(gzip.decompress((H/'Masks19x30.json.gz').read_bytes()))
    assert set(d)=={'cases','ecpp'} and set(d['cases'])=={f'{m}:{j}' for m in MASKS for j in (1,12,18)}
    used=set()
    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if q>=2**64:
            key=str(q);used.add(key);rows=d['ecpp'][key];assert rows
            for a in rows:
                assert a[0]==n and n>=2**64;n=C.pc.level(*a)
        assert C.pc.prime64(n)
        return True
    assert all(prime(q) for q in (*C.ORDER,root))
    for m in MASKS:
        yes=tuple(q for i,q in enumerate(C.ORDER[1:],1) if m>>i&1)
        no=tuple(q for q in C.ORDER[1:] if q not in yes)
        p=C.State([KEY],yes,no);assert live(p) and p.D%root==0 and root not in p.bad
        h=C.valuation(p.D,root);f=h;size=p.base;cells={}
        while size<=B:
            if p.possible(root,f,h):
                P=[KEY,(root,f)];s=C.State(P,yes,no)
                if live(s) and f in domain:cells[f]=s
            size*=root;f+=1
        assert f==62 and set(cells)=={1,12,18}
        vals=[]
        for j,s in cells.items():
            t=d['cases'][f'{m}:{j}'];assert t['type']=='forest' and set(t)=={'type','roots','head','owners'}
            k,o,n=(t[name] for name in ('roots','owners','head'));C.validate_forest(s,k,o,n,prime)
            assert C.Forest(s,k,o,n).lower()[0]>B
            labels={root,*k,*dict(o)}
            v=other({'assigned':[KEY,(root,j)],'present':yes,'absent':no,
                     'leaf':dict(kind='forest',roots=k,owners=o,head=n),
                     'ecpp':{str(q):d['ecpp'][str(q)] for q in labels if q>=2**64}})
            vals.append(v)
        print('PASS support',m,'remaining exact first',sorted(cells),'minimum second forest floor',min(vals),flush=True)
    assert used==set(d['ecpp'])
    print('PASS three complete support masks, not a complete canonical key',KEY,len(used),flush=True)


if __name__=='__main__':replay()

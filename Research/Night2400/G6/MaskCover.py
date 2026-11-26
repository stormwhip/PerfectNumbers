"""Rebuild conditional exclusion on the seven handed-off first-pivot values."""
from pathlib import Path
from hashlib import sha256
from functools import cache
from math import gcd,prod
from fractions import Fraction
import gzip,json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
import Verify as V
from Forest import second,legal


def verify():
    if not __debug__:raise RuntimeError('assertions required')
    tree=V.verify(H/'Thirteen262.json.gz'); data=tree['data']
    raw=(H/'Masks262.json.gz').read_bytes(); d=json.loads(gzip.decompress(raw));assert set(d)=={'ecpp','cases','full_masks'}
    seen=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2;n=q
        if n>=2**64:
            k=str(q); chain=data['ecpp'].get(k) or d['ecpp'][k];assert chain
            for lev in chain:assert lev[0]==n;n=V.C.pc.level(*lev)
            if k in d['ecpp']:seen.add(k)
        assert V.C.pc.prime64(n)
        return True
    pending={tuple(map(tuple,r)) for rows in tree['open'].values() for r in rows}
    cases={}; floors=[]; counts={'forest':0,'abundance':0,'direct':0};
    for m,r,leaf in d['cases']:
        assert type(m)==int and m in range(16,256,32)
        row=tuple(map(tuple,r));assert row in pending and (m,row) not in cases
        cases[m,row]=1
        need=tuple(q for i,q in enumerate(V.C.ORDER) if i>=5 and m>>i&1); no=tuple(q for i,q in enumerate(V.C.ORDER) if i>=5 and not m>>i&1); ban=V.BAN+no
        if leaf is None:
            s=prod(V.sig(q,h)//(1+h%2) for q,h in row)
            assert gcd(s*prod(q for q,_ in row),prod(ban))>1
            counts['direct']+=1;continue
        s=V.C.State(row,need,no);assert not s.conflict and s.base<=V.B
        if 'kind' in leaf:
            k=leaf['roots'];assert set(leaf)=={'kind','roots'} and leaf['kind']=='abundance'
            assert k==sorted(set(k)) and all(prime(q) and q not in s.rows and q not in ban and (s.D%q==0 or q in need) for q in k)
            def lower(q,odd):
                h=max(1,V.val(s.D,q));h+=((1-h)%4 if odd else h%2)
                while not legal(q,h,ban):h+=2+2*odd
                return Fraction(V.sig(q,h),q**h)
            a={q:lower(q,0) for q in k};u=Fraction(prod(V.sig(q,h) for q,h in row),s.X)*prod(a.values());opts=[u]
            if not s.fixed_euler:opts.extend(u/a[q]*lower(q,1) for q in k if q%4==1 and gcd(q+1,prod(ban))==1)
            assert min(opts)>2;counts['abundance']+=1;continue
        assert set(leaf)=={'roots','owners','head'}
        k,o,h=map(leaf.get,('roots','owners','head'));V.C.validate_forest(s,k,o,h,prime)
        a,b=V.C.Forest(s,k,o,h).lower()[0],second(row,need,ban,k,o,h)
        assert min(a,b)>V.B;floors.append(V.floor10(min(a,b)));counts['forest']+=1
    assert seen==set(d['ecpp'])
    full=[m for m in range(16,256,32) if all((m,r) in cases for r in pending)]
    assert full==d['full_masks']
    print('CONDITIONAL covered first values',sorted(map(int,data['cases'])),'full masks on that subset',full,'proved leaves',counts,'forest min',min(floors,default=None),'omitted first values',sorted(set(tree['root_domain'])-set(map(int,data['cases']))),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':verify()

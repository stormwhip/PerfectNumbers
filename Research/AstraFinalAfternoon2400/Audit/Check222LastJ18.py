"""Independent mask proofs, exact branches and arithmetic of final (19,222) f2/j18."""
from fractions import Fraction
from functools import cache
from hashlib import sha256
from math import gcd,lcm,prod
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B,geometric as G,split,state,vp
from Check31Forest import PR,forest
D=H.parent/'Nineteen'
P=((19,222),(7579985624053,2),(3705121363,22),(2032322226061,18))
K,W=45031669,5642747947
FILES=(('Root222J18.json.gz','27012a6a365936e0b7a3ebf8138f6fd4963188467f451179b9a3f05979c2c4b9',P,K,47,126,[2]),
       ('Root222J18Low.json.gz','31c89ddfd47a10015dfba559424fbc7e38a3a313696f86c2249c4d716e6841ba',(*P,(K,2)),W,24,97,[]))


def check(spec):
    file,digest,pre,piv,count,tail,remain=spec
    raw=(D/file).read_bytes(); assert sha256(raw).hexdigest()==digest
    d=json.loads(gzip.decompress(raw)); ec=d['ecpp']; used=set()
    @cache
    def prime(q):
        if q>=2**64:
            key=str(q); steps=ec[key]; assert steps
            used.add(key)
            for s in steps:
                assert s[0]==q
                q=PR['level'](*s)
        assert PR['prime64'](q)
    for p,_ in pre:prime(p)
    prime(piv)
    children,raw_tail=split(pre,piv,())
    assert tuple(map(tuple,d['prefix']))==pre and d['pivot']==piv and len(children)==count and raw_tail==tail
    assert d.get('raw_domain',d.get('domain'))==list(children)
    assert sorted(children.keys()-set(map(int,d['children'])))==d['remaining']==remain
    stats={}
    def terminal(row,n):
        X,S,ok=state(row,()); assert ok
        D=lcm(X,S)//X
        if 'abundance_only' in n:
            assert set(n)=={'abundance_only','bans','minima'}
            roots=n['abundance_only']; mode='abundance_only'
        else:
            assert 'forest' in n
            roots,edges,head=n['forest'];mode='forest'
        assert len(roots)==len(set(roots)) and all(D%p==0 and p not in dict(row) for p in roots)
        for p in roots:prime(p)
        fixed_odd=any(h%2 for _,h in row)
        bans=[]; base=prod(Fraction(G(p,h),p**h) for p,h in row)
        def minima():
            mins=[]
            for p in roots:
                h=vp(D,p)
                while (h%2 and (fixed_odd or h%4!=1 or p%4!=1)) or gcd(G(p,h),prod(bans))!=1:
                    h+=1
                mins.append([p,h])
            return mins,base*prod(Fraction(G(p,h),p**h) for p,h in mins)
        for banned,m in n.get('bans',n.get('derive_bans',[])):
            assert banned and len(banned)==len(set(banned)) and not set(banned)&set(bans)
            got,mass=minima(); assert m==got
            for p in banned:
                prime(p); assert p not in dict(row) and D%p!=0
                h=1 if not fixed_odd and p%4==1 else 2
                assert mass*Fraction(G(p,h),p**h)>2
            bans.extend(banned)
        assert state(row,bans)[-1]
        if mode=='abundance_only':
            m,b=minima(); assert m==n['minima'] and b>2
        else:
            for p,_ in edges:prime(p)
            assert forest(row,{'roots':roots,'owners':edges,'head':head},bans)>B
        stats[mode]=stats.get(mode,0)+1
    for f,node in d['children'].items():
        terminal(children[int(f)],node)
    assert used==ec.keys()
    print('PASS independent',file,len(children),'raw tail',tail,'remaining',remain,stats,'ECPP',len(used),flush=True)

if __name__=='__main__':
    assert __debug__
    for z in FILES:check(z)

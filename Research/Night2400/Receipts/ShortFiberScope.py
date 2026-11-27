"""Independent exact-domain and partition check for canonical 19x282 and 31x16."""
from pathlib import Path
from math import gcd,prod
import gzip,json

B=10**2400
ORDER=(19,7,11,31,13,3,5,17)
EXPECTED={(19,282):(19,[2,4,8,10,16,28,30,36],112),(31,16):(14,[16,22],100)}

def val(x,q):
    n=0
    while x%q==0:
        x//=q;n+=1
    return n

def sigma(q,e):return (q**(e+1)-1)//(q-1)

def state(P,ban):
    X=prod(q**e for q,e in P);S=prod(sigma(q,e) for q,e in P)
    D=S>>val(S,2)
    bad=gcd(D,ban)>1 or S>2*X
    for q,e in P:
        a=val(D,q);bad|=a>e;D//=q**a
    return X,D,bad or X*D>B

def domain(P,q,ban):
    X,D,bad=state(P,ban);assert not bad and q not in dict(P) and ban%q and D%q==0
    c=val(D,q);n=c; live=set(); direct=0
    base=(X*D)//q**c
    while base*q**n<=B:
        if (not n%2 or (q%4,n%4)==(1,1) and not any(e%2 for p,e in P)) and gcd(sigma(q,n),ban)==1:
            if state(P+((q,n),),ban)[2]:direct+=1
            else:live.add(n)
        n+=1
    assert base*q**(n-1)<=B<base*q**n
    return live,n,direct

def unique(pairs):
    d=dict(pairs);assert len(d)==len(pairs);return d

if __name__=='__main__':
    assert __debug__
    for p,e in EXPECTED:
        src=Path(f'Research/Night2400/Fibers{p}x{e}.json.gz')
        d=json.loads(gzip.decompress(src.read_bytes()),object_pairs_hook=unique)
        assert (d['p'],d['e'])==(p,e)
        q=d['pivot'];pre=((p,e),); ban=prod(ORDER[:ORDER.index(p)])
        live,tail,direct=domain(pre,q,ban)
        forest=split=0
        def walk(P,t):
            global forest,split,direct
            if t['type']=='forest':forest+=1;return
            assert t['type']=='split';split+=1
            x=t['q']; kids,k_tail,dead=domain(P,x,ban);direct+=dead
            assert set(map(str,kids))==t['cases'].keys()
            print('INNER',P,'pivot',x,'tail',k_tail,'live',sorted(kids))
            for e in kids:walk(P+((x,e),),t['cases'][str(e)])
        keys=set(map(int,d['cases'])); assert keys<=live and len(keys)==EXPECTED[p,e][0]
        for f in sorted(keys):walk(pre+((q,f),),d['cases'][str(f)])
        assert (len(keys),sorted(live-keys),tail)==EXPECTED[p,e]
        print('SCOPE',(p,e),'ban',ORDER[:ORDER.index(p)],'live',sorted(live),'covered',sorted(keys),'open',sorted(live-keys),'tail',tail,'forest/split/direct',forest,split,direct,'ECPP',len(d['ecpp']))

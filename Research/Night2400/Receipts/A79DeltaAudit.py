"""Replay only the exact f=4 delta of A79, without writing a derived packet."""
from collections import Counter
from hashlib import sha256
from math import gcd,prod
from fractions import Fraction
from pathlib import Path
import gzip,json,subprocess,sys

P=Path('Research/Night2400/A')
B=10**2400
Q=16148168401
ROOT=((7,12),)
OLD='ac69476668cc98f8e5b445d39b5ec76d723c0ae2'

def sigma(p,e):return (p**(e+1)-1)//(p-1)

def val(n,p):
    e=0
    while n%p==0:
        n//=p;e+=1
    return e

def state(P,ban):
    X=prod(p**e for p,e in P);S=prod(sigma(p,e) for p,e in P)
    D=S>>val(S,2)
    why=bool(set(dict(P))&set(ban)) or gcd(D,prod(ban))!=1 or sum(e%2 for p,e in P)>1 or any(e%2 and (p%4,e%4)!=(1,1) for p,e in P)
    for p,e in P:
        h=val(D,p);why|=h>e;D//=p**h
    return X,S,D,why or X*D>B or S>2*X

def branch(P,q,ban):
    X,S,D,dead=state(P,ban)
    assert not dead and q not in dict(P) and q not in ban and D%q==0
    h=val(D,q);scale=X*(D//q**h);i=h;kids=set();d=0
    while scale*q**i<=B:
        if (not i%2 or (q%4,i%4)==(1,1) and not any(e%2 for p,e in P)) and gcd(sigma(q,i),prod(ban))==1:
            if not state(P+((q,i),),ban)[3]:kids.add(i)
            else:d+=1
        i+=1
    assert scale*q**(i-1)<=B<scale*q**i
    print('SPLIT',P,'ban',ban,'pivot',q,'tail',i,'live',sorted(kids),'direct',d,flush=True)
    return kids,d

def modes(P,ban,allowed):
    X,S,D,dead=state(P,ban);assert not dead and not set(allowed)&set(dict(P))
    fixed_euler=any(e%2 for p,e in P)
    labels=[None]+([] if fixed_euler else [p for p in allowed if p%4==1 and gcd(p+1,prod(ban))==1])
    for special in labels:
        lower=Fraction(S,X)
        for p in allowed:
            h=max(1,val(D,p)); odd=p==special
            e=h+((1-h)%4 if odd else h%2)
            while p**e<=B and gcd(sigma(p,e),prod(ban))!=1:e+=4 if odd else 2
            if p**e>B:break
            lower*=Fraction(sigma(p,e),p**e)
        else:assert lower>2
    return len(labels)

def unique(a):
    b=dict(a);assert len(a)==len(b);return b

def decode(raw):return json.loads(gzip.decompress(raw),object_pairs_hook=unique)

class InMemoryPacket:
    def __init__(self,d):self.d=d
    def read_bytes(self):return gzip.compress(json.dumps(self.d).encode(),mtime=0)

def main():
    packet=P/'Fibers12.json.gz';raw=packet.read_bytes();d=decode(raw)
    old=decode(subprocess.check_output(['git','show',f'{OLD}:{packet.as_posix()}']))
    assert d['pair']==old['pair']==[7,12] and d['pivot']==old['pivot']==Q and sigma(7,12)==Q
    assert all(t==d['cases'][k] for k,t in old['cases'].items())
    assert all(t==d['ecpp'][k] for k,t in old['ecpp'].items())
    assert d['cases'].keys()-old['cases'].keys()=={'4'}
    live,n=branch(ROOT,Q,(19,))
    assert len(live)==83 and n==84 and sorted(live-set(map(int,d['cases'])))==[1,2,12,42]
    seen=set(); count=Counter()
    def save(q):
        if q>=2**64:seen.add(str(q))
    def walk(P,t,ban):
        typ=t['type'];count[typ]+=1
        X,S,D,dead=state(P,ban);assert not dead
        if typ=='split':
            q=t['q'];save(q)
            kids,n=branch(P,q,ban);count['direct']+=n
            assert set(map(str,kids))==t['cases'].keys()
            for e in sorted(kids):walk(P+((q,e),),t['cases'][str(e)],ban)
        elif typ=='forest':
            for q in [*t['roots'],*(q for q,p in t['owners'])]:save(q)
        elif typ=='abundance':
            forced=t['forced'];assert forced and len(set(forced))==len(forced) and all(D%q==0 for q in forced)
            for q in forced:save(q)
            count['abundance_modes']+=modes(P,ban,forced)
        elif typ in ('no-three','no-five'):
            absent,forced=(3,5) if typ=='no-three' else (5,3)
            assert ban==(19,) and absent not in dict(P) and (forced in dict(P) or D%forced==0)
            assert Fraction(sigma(7,12),7**12)*Fraction(13,9)*Fraction(6,5)>2
            if not state(P,ban+(absent,))[3]:walk(P,t['tree'],ban+(absent,))
        else:
            assert typ=='support-abundance'
            U=(3,5,11,13,17,31)
            for mask in range(64):
                yes={p for i,p in enumerate(U) if mask>>i&1}
                no=tuple(set(ban)|(set(U)-yes))
                if not state(P,no)[3]:count['support_modes']+=modes(P,no,sorted(yes-set(dict(P))))
    walk(ROOT+((Q,4),),d['cases']['4'],(19,))
    assert d['ecpp'].keys()-old['ecpp'].keys()<=seen<=d['ecpp'].keys()
    print('DELTA',dict(count),'ECPP',len(seen),'new',len(d['ecpp'])-len(old['ecpp']),'packet SHA-256',sha256(raw).hexdigest(),flush=True)
    sys.path.insert(0,str(P.resolve()))
    import Verify
    filtered=dict(pair=d['pair'],pivot=d['pivot'],cases={'4':d['cases']['4']},ecpp={k:d['ecpp'][k] for k in seen})
    assert 4 not in Verify.verify(InMemoryPacket(filtered))

if __name__=='__main__':
    assert __debug__
    main()

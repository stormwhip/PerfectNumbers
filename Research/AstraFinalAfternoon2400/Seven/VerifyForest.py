"""Offline root-seven exact-subtree verifier. No factoring or Hensel enumeration."""
import argparse
from functools import cache
import gzip
from hashlib import sha256
import json
from math import gcd, prod
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(R/'Session20261126'), str(R/'Night2400/A')]
from PivotCheck import C, B
from MaskedForest import exact_absence_bound

Q = 16148168401
T = (Q**13-1)//(Q-1)//13
L = 3453283
R173 = 173
S438 = 572749682520506652634407616247
S48 = 6106505825833677713

def sig(p, h):
    return (p**(h+1)-1)//(p-1)

def val(a,p):
    v=0
    while a%p==0: a//=p; v+=1
    return v

def exact_state(P,bad):
    assert len(set(p for p,h in P))==len(P) and all(p>2 and p%2 and h>0 for p,h in P)
    X=prod(p**h for p,h in P); raw=prod(sig(p,h) for p,h in P); n=sum(h%2 for p,h in P)
    S=raw//2**n; D=S
    pool=prod(p for p,h in P)
    while (g:=gcd(D,pool))>1: D//=g
    live=(n<=1 and all(not h%2 or p%4==h%4==1 for p,h in P)
          and gcd(S*pool,prod(bad))==1 and all(S%p**(h+1) for p,h in P)
          and X*D<=B and raw<=2*X)
    return live,X,D,n

def child_domain(P,bad,q):
    live,X,D,n=exact_state(P,bad)
    assert live and q not in dict(P) and q not in bad and D%q==0
    a=val(D,q); h=a; m=X*(D//q**a)*q**a; out={}
    while m<=B:
        if h%2==0 or (n==0 and q%4==h%4==1):
            child=P+[(q,h)]
            if exact_state(child,bad)[0]:out[str(h)]=child
        h+=1; m*=q
    assert m>B
    return out,h

def abgt2(exps):
    return prod(sig(p,h) for p,h in exps)>2*prod(p**h for p,h in exps)

def known_scope(P,bad):
    pref=P[:-1]; q,h=P[-1]
    assert tuple(bad)==(19,) or tuple(bad)==(19,5,11)
    if pref==[(7,48)] and q==S48:
        assert tuple(bad)==(19,) and h in (2,4,8,10)
        name='48'
    elif pref==[(7,438),(S438,10)] and q==67:
        assert tuple(bad)==(19,) and h in range(2,159,2) and h!=148
        name='438'
    elif pref==[(7,12),(Q,42)] and q==R173:
        assert tuple(bad)==(19,) and (h==1 or h in range(2,211,2) and h not in {126,130,136,138,156,158,172,176,180,182,184,192,196,198,200,202,204,206,208,210})
        name='12R'
    else:
        assert pref==[(7,12),(Q,12),(T,2)] and q==L and tuple(bad)==(19,5,11)
        assert h in {2,6,8,10,12,16,18,20,22,26,28,30,36,46,48,52,58,66,70,72,78,82,88,96,100,102,106,108,112,126}
        # 3 and 13 are compulsory, 3 and 11 (if present) always ordinary.
        assert sig(7,12)==Q and sig(Q,12)==13*T and sig(T,2)%(3*L)==0
        assert abgt2([(7,12),(3,2),(5,1)])
        assert abgt2([(7,12),(11,2),(3,4),(13,1)])
        assert abgt2([(7,12),(11,2),(3,2),(13,2)])
        assert sig(3,2)==13
        name='12L'
    # Every component earlier than the final pivot is itself verified to be of a
    # directly compatible exponent. This does not claim closure of its siblings.
    for i in range(1,len(P)):
        kids,_=child_domain(P[:i],bad,P[i][0]); assert str(P[i][1]) in kids
    return name

def verify(path):
    assert __debug__
    raw=path.read_bytes(); obj=json.loads(gzip.decompress(raw)); assert set(obj)=={'records','ecpp'}
    used=set(); seen=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2
        u=q
        if q>=2**64:
            key=str(q); used.add(key)
            for r in obj['ecpp'][key]: assert r[0]==u; u=C.pc.level(*r)
        return C.pc.prime64(u)
    def walk(P,bad,node,stats,low):
        assert exact_state(P,bad)[0]
        if node['type']=='split':
            assert set(node)=={'type','q','cases'} and prime(node['q'])
            kids,tail=child_domain(P,bad,node['q']); assert set(kids)==set(node['cases'])
            stats[0]+=1;stats[2]=max(stats[2],tail)
            for a in kids:walk(kids[a],bad,node['cases'][a],stats,low)
            return
        assert node['type']=='forest' and set(node)=={'type','roots','owners','head'}
        rt,es,head=(node[k] for k in ('roots','owners','head'))
        s=C.State(P,absent=tuple(b for b in bad if b!=19)); assert s.bad==tuple(bad) and not s.conflict
        _,x,d,_=exact_state(P,bad); assert (s.X,s.D)==(x,d)
        C.validate_forest(s,rt,es,head,prime)
        a=C.Forest(s,rt,es,head).lower()[0]
        b=exact_absence_bound(P,rt,es,head,bad,B)
        assert min(a,b)>B,(P,a,b)
        low.append(min(a,b)*10**6//B);stats[1]+=1
    for rec in obj['records']:
        assert set(rec)=={'P','bad','tree','unresolved'} and not rec['unresolved']
        P=list(map(tuple,rec['P'])); bad=tuple(rec['bad']); assert all(prime(q) for q,h in P)
        name=known_scope(P,bad); k=name,P[-1][1]; assert k not in seen; seen.add(k)
        stats=[0,0,0];low=[];walk(P,bad,rec['tree'],stats,low)
        print(name,P[-1][1],'splits, forests, max raw-tail:',stats,'min floor(1e6 * LB/B):',min(low,default=None),flush=True)
    assert used==set(obj['ecpp']) and seen
    print('PASS',path.name,sorted(seen),'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('pack',type=Path,nargs='+');args=a.parse_args()
    for f in args.pack:verify(f)

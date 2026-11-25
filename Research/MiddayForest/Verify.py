"""Independent unweighted-forest replay for the Midday batch. stdlib only.
Recomputes shape, valuations and all exponent classes, with exact integer floors.
No imported search, forest verifier, caches, network, or external arithmetic programs.
"""
from pathlib import Path
from functools import cache
from math import gcd,prod
import gzip,json,sys,hashlib
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'RootFiveNext'))
from PrimeCheck import level,prime64
ORDER=(19,7,11,31,13,3,5,17);B=10**2400

def require(x,why):
 if not x:raise ValueError(why)

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));require(set(d)=={'rows','ecpp'} and len(d['rows'])==1,'packet schema');r=d['rows'][0];require(set(r) in ({'p','e','head','owners','roots'},{'p','e','head','owners','roots','rho','den'}),'forest schema');p,e,n=r['p'],r['e'],r['head'];require(type(p)==int and p in ORDER and type(e)==int and 2<=e<=7000 and e%2==0 and type(n)==int and 1<=n<=512,'range');K=set(r['roots']);o=dict(r['owners']);V=K|o.keys();require(K and not K&o.keys() and len(o)==len(r['owners']) and len(K)==len(r['roots']),'disjoint');require(set(d['ecpp'])=={str(z) for z in V if z>=2**64},'chain coverage')
 for z in V:
    require(type(z)==int and z>2,'node type');q=z
    for c in d['ecpp'].get(str(z),[]):
        require(c[0]==q,'link');q=level(*c)
    require(prime64(q),'primality')
 A=(p**(e+1)-1)//(p-1);bad=ORDER[:ORDER.index(p)];require(all(A%z==0 for z in K) and all(z in V and p*A%q for q,z in o.items()),'ownership scope');kids={z:[] for z in V}
 for q,z in o.items():kids[z].append(q)
 stack=list(K);seen=set()
 while stack:
    z=stack.pop();require(z not in seen,'cycle');seen.add(z);stack.extend(kids[z])
 require(seen==V,'reachability');U=p*A*prod(o);den=r.get('den',1);w=dict(r.get('rho',[]));require(type(den)==int and 1<=den<=8 and len(w)==len(r.get('rho',[])) and all(z in V and type(u)==int and 0<u<den for z,u in w.items()),'weight range');target=B**den
 def val(a,q):
    k=0
    while a%q==0:k+=1;a//=q
    return k
 @cache
 def node(q,h):
    # (all ordinary, one Euler anywhere in this subtree). Enumerate possible parity independently.
    a0=target+1;a1=target+1
    for sp in (False,True):
        if sp and (q%4!=1 or any((q+1)%b==0 for b in bad)):continue
        step=4 if sp else 2;f=h+((1-h)%4 if sp else h%2);cnt=0
        while True:
            if any((f+1)%b==0 if q%b==1 else pow(q,f+1,b)==1 for b in bad):f+=step;continue
            qf=q**f;charge=qf**(den-w.get(q,0))
            if cnt==n or charge>=(a1 if sp else max(a1,a0)):
                if not sp:a0=min(a0,charge)
                a1=min(a1,charge);break
            cnt+=1;S=(q*qf-1)//(q-1)//(2 if sp else 1);t=S;g=gcd(t,U)
            while g>1:t//=g;g=gcd(t,U)
            subs=[node(y,val(S,y)) for y in kids[q] if S%y==0];v=charge*t**den*prod(z**(u*val(S,z)) for z,u in w.items())*prod(x for x,y in subs)
            if not sp:
                a0=min(a0,v);v=min([v]+[v//x*y for x,y in subs])
            a1=min(a1,v);f+=step
    return a0,a1
 hs={q:val(A,q) for q in K};sub=[node(q,h) for q,h in hs.items()];b0=(p**e*(A//prod(q**h for q,h in hs.items())))**den*prod(q**(u*val(A,q)) for q,u in w.items())*prod(x for x,y in sub);b=min([b0]+[b0//x*y for x,y in sub]);require(b>target,'exact comparison failed');fl=2400
 while b>=10**((fl+1)*den):fl+=1
 return p,e,fl,hashlib.sha256(path.read_bytes()).hexdigest()
if __name__=='__main__':
 if not __debug__:raise SystemExit('no -O')
 for f in (map(Path,sys.argv[1:]) if len(sys.argv)>1 else sorted(H.glob('Forest*.json.gz'))):print('PASS',*verify(f),flush=True)

"""Verify recursive exact-exponent partition. Read all graph and ECPP data from one frozen packet."""
import sys,json,gzip,math
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
from collections import Counter
H=Path(__file__).resolve().parent;spec=spec_from_file_location('VM',H/'VerifyMulti.py');V=module_from_spec(spec);spec.loader.exec_module(V)
def verify(path):
 d=json.loads(gzip.decompress(Path(path).read_bytes()));assert d['schema']=='recursive-supply-1';p,e=d['seed'];assert p in (7,11,13,19,31) and e>=2 and e%2==0;A=V.sigma(p,e);ban=V.T.forbidden(p);assert all(A%b for b in ban);entries=d['states'];seen=set();prim=set();counts=Counter();maxdepth=0
 def prime(z):
  if z in prim:return
  x=z;assert type(z)==int and z>2
  if z>=2**64:
   for rr in d['ecpp'][str(z)]:assert rr[0]==x;x=V.PC.level(*rr)
  assert V.PC.prime64(x);prim.add(z)
 def walk(fix,X,S,od):
  nonlocal maxdepth
  assert 0<=od<=1 and S%2;maxdepth=max(maxdepth,len(fix));C=V.peel(S,X);assert X*C<=V.B and S*(1+od)<=2*X and all(V.a.val(S,q)<=g for q,g in [(p,e),*fix]);id=','.join(f'{q}:{g}' for q,g in fix);assert id in entries and id not in seen;seen.add(id);r=entries[id]
  if isinstance(r,int):
   q=r;prime(q);assert C%q==0;h=V.a.val(C,q);g=h;base=X*(C//q**h);counts['split']+=1
   while base*q**g<=V.B:
    if (not g%2 or not od and q%4==g%4==1) and V.ready(q,g,ban):
     od1=od+g%2;X1=X*q**g;S1=S*(V.sigma(q,g)//(1+g%2));f1=fix+[(q,g)]
     if X1*V.peel(S1,X1)<=V.B and S1*(1+od1)<=2*X1 and all(V.a.val(S1,z)<=j for z,j in [(p,e),*f1]):walk(f1,X1,S1,od1)
    g+=1
  else:
   assert fix;K=set(r['roots']);P=dict(r['owners']);Vs=K|P.keys();assert len(K)==len(r['roots']) and len(P)==len(r['owners']) and not K.intersection(P) and all(C%z==0 for z in K) and all(X*C%z for z in P);kids={z:[] for z in Vs}
   for z in Vs:prime(z)
   for y,z in P.items():kids[z].append(y)
   st=list(K);vs=set()
   while st:
    z=st.pop();assert z not in vs;vs.add(z);st.extend(kids[z])
   assert vs==Vs and 1<=r['head']<=512;counts[V.model(p,e,fix,K,P,r['head'])]+=1
 walk([],p**e,A,0);assert seen==set(entries);return {'p':p,'e':e,'states':len(seen),'max_depth':maxdepth,'rules':dict(counts)}
if __name__=='__main__':
 for f in sys.argv[2:] or sorted(H.glob('Recursive*.json.gz')):print(json.dumps(verify(f)),flush=True)

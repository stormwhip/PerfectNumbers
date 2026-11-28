"""Build/replay a pinned high-first manifest; oracle-free proof mode."""
from pathlib import Path
from fractions import Fraction
import sys,json,gzip
from math import prod
from collections import Counter
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from VerifyS2 import compactP,prime
from VerifyT280 import v,old,split,C,exact,B
from Paths280 import paths,s,y
assert __debug__

def payload(name):
 p=H/name
 if p.exists():return json.loads(p.read_bytes())
 return json.loads(gzip.decompress(p.with_suffix('.json.gz').read_bytes()))

def choose():
 ans={}
 for f in [16,18]:
  for i,P in enumerate(paths):
   if len(P)!=3 or P[1]!=(s,f) or P[-1][0]!=y:continue
   e=P[-1][1];res=None
   if (H/f'GrowS{f}y{e}.json').exists():res=['compact',f'GrowS{f}y{e}']
   elif (H/f'Ab280Case{i}.json').exists() or (H/f'Ab280Case{i}.json.gz').exists():res=['abtree',i]
   elif (H/f'Hybrid280Case{i}.json').exists() and payload(f'Hybrid280Case{i}.json')['full']:res=['hybrid',i]
   if res:ans[f'{f},{e}']=res
 return ans

def hybrid(P,i):
 data=payload(f'Hybrid280Case{i}.json');assert P==list(map(tuple,data['path']));book=data['nodes'];used=set();ct=Counter()
 def rec(R):
  key=','.join(str(e) for p,e in R);assert key not in used;used.add(key);n=book[key];kind=n['kind'];ct[kind]+=1;st=C.State(R);assert not st.conflict
  if kind=='split':
   q=n['q'];prime(q);cs,*_=split(R,q)
   for child in cs.values():rec(child)
   return
  if kind=='forest':
   K,O,h=n['R'];C.validate_forest(st,K,O,h,prime);assert min(C.Forest(st,K,O,h).lower()[0],exact(R,K,O,h))>B;return
  F=n['F'];assert kind in ('ab','parity') and len(F)==len(set(F)) and all(prime(q) and st.D%q==0 for q in F)
  hs={q:C.valuation(st.D,q) for q in F};ne={q:h+h%2 for q,h in hs.items()};odd={q:h+(1-h)%4 for q,h in hs.items() if q%4==1 and not st.fixed_euler}
  if kind=='ab':k=lambda q,h:Fraction(C.sigma(q,h),q**h);base=Fraction(prod(C.sigma(q,h) for q,h in R),st.X);limit=2
  else:k=lambda q,h:Fraction(q**(h-hs[q]));base=Fraction(st.base);limit=B
  normal=base*prod(k(q,h) for q,h in ne.items());assert min([normal]+[normal/k(q,ne[q])*k(q,h) for q,h in odd.items()])>limit
 rec(P);assert used==set(book);return ct

def run(fs):
 for z in H.glob('HighBook*.json.gz'):v.book.update(json.loads(gzip.decompress(z.read_bytes())))
 manifest=payload('HighManifest.json'); total=Counter()
 for f in fs:
  P=[(19,280),(s,f)];assert all(prime(p) for p,e in P) and C.sigma(19,280)%s==0
  cs,_,_,tail=split(P,y);proved=[];prime(y)
  for e,pp in cs.items():
   k=f'{f},{e}'
   if k not in manifest:continue
   kind,param=manifest[k];total[kind]+=1
   if kind=='compact':compactP(pp,param)
   elif kind=='abtree':assert paths[param]==pp;v.verify(param)
   else:assert kind=='hybrid';hybrid(pp,param)
   proved.append(int(e));print('PASS s,y',f,e,kind,flush=True)
  assert set(proved)==set(map(int,cs)),('missing',f,set(map(int,cs))-set(proved))
  assert tail=={16:122,18:117}[f] and proved==list(range(2,61 if f==16 else 59,2))
  print('COMPLETE s',f,'raw y tail',tail,'exact children',len(proved),flush=True)
 print('totals',total,flush=True)
if __name__=='__main__':run(list(map(int,sys.argv[1:])) or [16,18])

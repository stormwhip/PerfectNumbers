"""Discover and replay exact support exclusions, using mandatory sigma(q) in an Euler branch."""
import sys,runpy,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from functools import cache
mode,repo,out=sys.argv[1:4];repo=Path(repo);out=Path(out); assert __debug__
def load(path,h):
 b=(repo/path).read_bytes().replace(b'\r\n',b'\n');assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==h;return b
load('Research/SupportSplit/Verify.py','fe82b801b8d39b0c83ccb924b9651965b2a151a6');v=runpy.run_path(str(repo/'Research/SupportSplit/Verify.py'))
d=json.loads(load('Research/Midday/Delta.json','3a7b6812aafed3dddd228c34ed9575324d242887'));pairs=sorted({(r['root'],e) for r in d['remaining_shards'] for e in r['remaining_actuals']});assert len(pairs)==244
old={(p,e,tuple(sorted(s))) for p,e,s,q in v['WITNESSES']}|{(31,8,(3,5,13,31))};roots=v['ROOTS'];a=v['abundance'];B=v['B'];component=v['component'];leaf=v['leaf'];masks=v['masks'];me=v['min_exp'];primes=v['PRIMES'];states=v['states']
# Optional certified large-root factor bank. Baseline leaf is intentionally unchanged.
if '--bank' in sys.argv:
 import gzip
 lab=Path(__file__).resolve().parent; data=json.loads(gzip.decompress((lab/'bank.json.gz').read_bytes()));pc=lab/'PrimeCheck.py';b=pc.read_bytes().replace(b'\r\n',b'\n');assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='c25f9c63bf3497ed60093e9941c7f2be2531fbe5'; kernel=runpy.run_path(str(pc));plain=component
 @cache
 def proved(q):
  z=q
  for row in data['ecpp'].get(str(z),[]):
   assert row[0]==z;z=kernel['level'](*row)
  assert kernel['prime64'](z)
 @cache
 def component(p,e):
  z,small=plain(p,e);fac=dict(small)
  for q in data['rows'].get(f'{p}:{e}',[]):
   assert q>2 and z%q==0;proved(q);t=z;h=0
   while t%q==0:t//=q;h+=1
   fac[q]=h
  return z,tuple(fac.items())
@cache
def half(q):return component(q,1)
def improved(p,e,s,fix,tail):
 fixed=dict(((p,e),)+fix); tails=dict(tail);ban=tuple(q for q in roots if q not in s);have={r:1 for r in s};incoming={};R=N=1;I=F(1);odd=[q for q,f in fixed.items() if f%2];
 if len(odd)>1:return True
 for q,f in fixed.items():
  z,fac=component(q,f);R*=z;N*=q**f;I*=a(q,f)
  if any(z%u==0 for u in ban):return True
  for r,t in fac:incoming[r]=incoming.get(r,0)+t
 for r,t in incoming.items():have[r]=max(have.get(r,0),t)
 # If Euler prime outside the known mandatory support: all known unassigned bases are even.
 opts=[None] if odd else [None]+[q for q in have if q not in fixed and q%4==1]
 for eq in opts:
  hs=have.copy();x,y,z=I,N,R
  if eq is not None:
   z0,fac=half(eq)
   if any(z0%u==0 for u in ban):continue
   z*=z0
   for r,t in fac:hs[r]=max(hs.get(r,0),incoming.get(r,0)+t)
  if any(hs.get(q,0)>f for q,f in fixed.items()):continue
  for q in set(hs)|set(fixed):
   while z%q==0:z//=q
  for q,t in hs.items():
   if q in fixed:continue
   f=me(q,max(t,tails.get(q,0)),eq==q,ban);y*=q**f;x*=a(q,f)
  if x<=2 and y*z<=B:return False
 return True

def run(p,e,s,depth,tree=None,ver=False):
 assert (p,e) in pairs and s in masks(p) and (p,e,tuple(sorted(s))) not in old and not leaf(p,e,s)
 @cache
 def walk(ff,tt,dep,encoded):
  node=json.loads(encoded) if ver else None
  if (all(q in primes for q,f in ff+tt) and leaf(p,e,s,ff,tt)) or improved(p,e,s,ff,tt):
   if ver:assert node==0
   return 0
  if dep==0:return None
  qs=set(s)
  for q,f in ((p,e),)+ff:qs.update(r for r,t in component(q,f)[1]);
  qs=sorted((qs-{p}-set(dict(ff))-set(dict(tt)))&set(primes))
  if ver:assert type(node)==list and node[0] in qs;qs=[node[0]]
  else:qs=qs[:4]
  for q in qs:
   st=list(states(q));children=[None]*len(st)
   if ver:assert len(node[1])==len(st)
   for i in [-1]+list(range(len(st)-1)):
    u,w=st[i];x=walk(ff+u,tt+w,dep-1,json.dumps(node[1][i]) if ver else '')
    if x is None:break
    children[i]=x
   else:return [q,children]
  return None
 return walk((),(),depth,json.dumps(tree) if ver else '')

if mode=='search':
 depth=int(sys.argv[4]); root=int(sys.argv[5]);n=0
 with out.open('x') as of:
  for p,e in pairs:
   if p!=root:continue
   for s in masks(p):
    if (p,e,tuple(sorted(s))) in old or leaf(p,e,s):continue
    t=run(p,e,s,depth)
    if t is not None:print(json.dumps([p,e,sorted(s),t],separators=(',',':')),file=of,flush=True);n+=1
   print(p,e,n,flush=True)
elif mode=='verify':
 seen=set()
 for l in out.read_text().splitlines():
  p,e,s,t=json.loads(l);k=(p,e,tuple(s));assert k not in seen;seen.add(k);assert run(p,e,frozenset(s),100,t,True)==t
 print('verified',len(seen),'pairs',len(set(k[:2] for k in seen)))
else:raise ValueError(mode)

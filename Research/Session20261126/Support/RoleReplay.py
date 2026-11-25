"""Checks (p,e,H,q_Euler) contradictions, including the full infinite Euler progression, not just q^1."""
from pathlib import Path
from fractions import Fraction as F
from functools import cache
import sys,json,runpy,hashlib
mode,repo,out=sys.argv[1:4];repo=Path(repo);out=Path(out);assert __debug__
v=runpy.run_path(str(repo/'Research/SupportSplit/Verify.py'));d=json.loads((repo/'Research/Midday/Delta.json').read_bytes());pairs=sorted({(r['root'],e) for r in d['remaining_shards'] for e in r['remaining_actuals']});old={(p,e,tuple(sorted(s))) for p,e,s,q in v['WITNESSES']}|{(31,8,(3,5,13,31))};roots=v['ROOTS'];a=v['abundance'];B=v['B'];component=v['component'];leaf=v['leaf'];masks=v['masks'];me=v['min_exp'];primes=set(v['PRIMES']);states=v['states']
@cache
def val(q,e):return component(q,e)
def check(p,e,s,q,extra,ft=(),tail=()):
 fixed=dict(((p,e),)+ft);assert q not in fixed and all(h%2==0 for h in fixed.values());ban=tuple(r for r in roots if r not in s);R=N=1;I=F(1);hs={r:0 for r in s};t0=dict(tail)
 for r,f in list(fixed.items())+([(q,1)] if extra else []):
  z,fac=val(r,f);R*=z
  if any(z%b==0 for b in ban):return True
  for u,h in fac:hs[u]=hs.get(u,0)+h
  if r in fixed:N*=r**f;I*=a(r,f)
 for r in set(hs)|set(fixed):
  while R%r==0:R//=r
 for r,h in hs.items():
  if r in fixed:
   if h>fixed[r]:return True
   continue
  f=me(r,max(h,1,t0.get(r,0)),r==q,ban);N*=r**f;I*=a(r,f)
 return I>2 or N*R>B

def mandatory(p,e,s,q,ft=()):return (set(s)|{r for x,y in ((p,e),)+ft+((q,1),) for r,h in val(x,y)[1]})-{p,q}-set(dict(ft))
def tree(p,e,s,q,verify=None):
 ban=tuple(r for r in roots if r not in s);assert q in (set(s)|set(dict(val(p,e)[1]))) and q%4==1 and q!=p
 # Do not count a previously ruled out immediate banned-prime position or singleton base valuation bound.
 if any((q+1)%b==0 for b in ban) or check(p,e,s,q,False):return None
 if check(p,e,s,q,True):return 0
 cand=sorted(mandatory(p,e,s,q));
 if verify is not None:
  assert verify in cand;cand=[verify]
 for r in cand[:6]:
  if all(check(p,e,s,q,True,((r,f),)) for f in (2,4,6,8)) and check(p,e,s,q,True,(),((r,10),)):return r
 return None

def valid(p,e,s):return (p,e) in pairs and s in masks(p) and (p,e,tuple(sorted(s))) not in old and not leaf(p,e,s)
if mode=='search':
 n=0
 with out.open('x') as of:
  for p,e in pairs:
   for s in masks(p):
    if not valid(p,e,s):continue
    for q in (set(s)|set(dict(val(p,e)[1])))-{p}:
     if q%4!=1:continue
     tr=tree(p,e,s,q)
     if tr is not None:print(json.dumps([p,e,sorted(s),q,tr],separators=(',',':')),file=of,flush=True);n+=1
 print('discovered',n)
elif mode=='verify':
 seen=set();keys=set();rs=set();sh=0
 for l in out.read_text().splitlines():
  p,e,ss,q,tr=json.loads(l);s=frozenset(ss);k=(p,e,tuple(ss),q);assert valid(p,e,s) and k not in seen;assert tree(p,e,s,q,tr)==tr;seen.add(k);keys.add(k[:-1]);rs.add((p,e));sh+=tr!=0
 print('role certificates',len(seen),'support cases',len(keys),'root exponents',len(rs),'nontrivial splits',sh)

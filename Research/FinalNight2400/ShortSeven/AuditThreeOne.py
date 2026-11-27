"""Independent exact domain tree enumeration for the conditional Euler-1093 branch."""
from pathlib import Path
from math import gcd,prod
from collections import Counter
from functools import cache
import gzip,json,hashlib
H=Path(__file__).resolve().parent;P=H.parent/'Three/OneComplete.json.gz';d=json.loads(gzip.decompress(P.read_bytes()));B=10**2400;ban=prod([19,7,11,31,13]);assert __debug__
@cache
def sig(q,h):return (q**(h+1)-1)//(q-1)
def val(n,q):
 i=0
 while n%q==0:n//=q;i+=1
 return i
def state(rows):
 assert len(dict(rows))==len(rows) and sum(h%2 for q,h in rows)==1
 X=prod(q**h for q,h in rows);rad=prod(q for q,h in rows);S=prod(sig(q,h) for q,h in rows)//2
 if S>X or gcd(rad*S,ban)>1 or any(val(S,q)>h for q,h in rows):return None
 D=S
 while (g:=gcd(D,rad))>1:D//=g
 return (X,D) if X*D<=B else None
c=Counter();reached=set();maxdepth=0
@cache
def domain(rows,q):
 X,D=state(rows);assert D%q==0 and q not in dict(rows) and gcd(q,ban)==1
 a=val(D,q);f=a+(a%2);n=X*(D//q**a)*q**f;result=[]
 while n<=B:
  if state(rows+((q,f),)) is not None:result.append(f)
  f+=2;n*=q*q
 return result

def walk(rows,t):
 global maxdepth
 assert state(rows);maxdepth=max(maxdepth,len(rows));pairs=set(dict(rows))
 if 'net' in t:
  assert set(t)=={'net','lam'} and t['lam'] in (1,1000,10000);X,D=state(rows);a=t['net'];assert len(set(a))==len(a) and all(D%z==0 and z not in pairs and gcd(z,ban)==1 for z in a);reached.update(a);c['net']+=1;return
 for tag,l in [('pair',4),('weighted',6),('triple',3)]:
  if tag in t:
   assert set(t)=={tag} and len(t[tag])==l
   if tag!='triple':
    z,y,az,ay=t[tag][:4];S=prod(sig(z,h) for z,h in rows)//2;assert z!=y and z in pairs and y in pairs and 0<=dict(rows)[z]-val(S,z)<=az and 0<=dict(rows)[y]-val(S,y)<=ay
   else:assert len(set(t[tag]))==3 and all(0<=i<len(rows) for i in t[tag])
   c[tag]+=1;return
 if t['type']=='forest':
  assert set(t)=={'type','roots','owners','head'};reached.update(t['roots']);reached.update(z for z,y in t['owners']);c['forest']+=1;return
 assert set(t)=={'type','q','cases'} and t['type']=='split';q=t['q'];reached.add(q);ds=domain(rows,q);assert set(ds)==set(map(int,t['cases']));c['split']+=1
 for h in ds:walk(rows+((q,h),),t['cases'][str(h)])
base=((3,6),(1093,1));top=domain(base,547);assert len(top)==160 and max(top)<=436
low=set(map(int,d['cases']));hi=set(top)-low;assert len(low)==108 and len(hi)==52 and low<=set(top) and min(hi)>max(low)
for f in low:walk(base+((547,f),),d['cases'][str(f)])
large={str(q) for q in reached if q>=2**64};assert large==set(d['ecpp']);assert sig(3,6)==1093 and sig(1093,1)==1094
print('PASS independently rebuilt',len(top),'secondary siblings,',len(low),'explicit,',len(hi),'uniform; min high/max low',min(hi),max(low),'terminal/split counts',dict(c),'maximum prefix length',maxdepth,'large labels',len(large),'SHA',hashlib.sha256(P.read_bytes()).hexdigest())

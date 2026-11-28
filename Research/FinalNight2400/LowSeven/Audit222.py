"""Scope-only independent arithmetic audit: 7 serial packet dependencies, no forest-verifier imports."""
from pathlib import Path
from math import gcd,prod
from fractions import Fraction
import json,gzip,hashlib
from functools import cache
H=Path(__file__).resolve().parents[1]/'Root222';B=10**2400;t=7579985624053;r=3705121363;root=((19,222),)
names=['FirstForests','TwoForests','ThirdForests','Twelve','TwentyEight','TwentyTwo','Sixteen'];ds=[]
for name in names:
 b=(H/(name+'.json.gz')).read_bytes();ds.append(json.loads(gzip.decompress(b)));print(name,hashlib.sha256(b).hexdigest(),flush=True)
@cache
def sig(p,h):return (p**(h+1)-1)//(p-1)
def val(n,q):
 a=0
 while n%q==0:n//=q;a+=1
 return a
def state(P):
 odd=sum(h%2 for q,h in P);X=prod(q**h for q,h in P);S=prod(sig(q,h)//(1+h%2) for q,h in P);D=S
 if odd>1 or any(h%2 and (q%4!=1 or h%4!=1) for q,h in P) or any(val(S,q)>h for q,h in P) or (1+odd)*S>2*X:return None
 while (g:=gcd(D,X))>1:D//=g
 return (X,S,D,odd) if X*D<=B else None
@cache
def dom(P,q):
 X,S,D,odd=state(P);v=val(D,q);assert v>0 and q not in dict(P);h=v;size=X*D;ls={}
 while size<=B:
  rr=P+((q,h),)
  if state(rr) is not None:ls[str(h)]=rr
  h+=1;size*=q
 return ls,h
ct=[0]*7;visited=[set() for _ in ds];forced={}
def leaf(idx,P,code):
 X,S,D,od=state(P);k,o=code;assert len(set(k))==len(k) and len(dict(o))==len(o) and all(q not in dict(P) and D%q==0 for q in k) and all(q not in dict(P) and D%q!=0 for q,p in o);visited[idx].update(k);visited[idx].update(q for q,p in o);ct[idx]+=1
rootdom,tail=dom(root,t);assert tail==144 and len(rootdom)==53
first=ds[0]['cases'];assert len(first)==44 and set(first)<=set(rootdom)
for f,v in first.items():leaf(0,rootdom[f],v)
remaining=set(rootdom)-set(first);second=ds[1]['cases'];assert remaining==set(second) and {40,46}<=set(map(int,remaining));pairs={}
for f,v in second.items():
 P=rootdom[f]
 if f in ('40','46'):leaf(1,P,v);continue
 d,_=dom(P,r);assert set(v)<=set(d)
 for g,x in v.items():leaf(1,d[g],x)
 for g in set(d)-set(v):pairs[f+':'+g]=d[g]
assert len(pairs)==42 and ct[1]==229
third=ds[2]['cases'];assert set(third)<=set(pairs);rr3={};full=0
for tag,P in pairs.items():
 if tag not in third:rr3[tag]=None;continue
 a=third[tag]
 if isinstance(a,list):leaf(2,P,a);full+=1;continue
 z=a['q'];d,_=dom(P,z);visited[2].add(z);assert set(a['children'])<=set(d) and set(map(str,a['left']))==set(d)-set(a['children'])
 for k,n in a['children'].items():leaf(2,d[k],n)
 if a['left']:rr3[tag]=(z,{g:d[str(g)] for g in a['left']})
 else:full+=1
assert full==14 and len(rr3)==28
x=ds[3]['cases'];expect={k.split(':')[1] for k in rr3 if k.startswith('12:')};assert expect==set(x)=={'2','16','22'}
for g,y in x.items():
 z,ls=rr3['12:'+g];assert z==50935324949359682417 and set(ls)=={6};P=ls[6];a=371183958661 if g=='2' else 4873207;d,_=dom(P,a);assert set(y)==set(d)
 for k,n in y.items():leaf(3,d[k],n)
 visited[3].update(dict(P));visited[3].add(a)
assert set(ds[4]['cases'])=={'28'};leaf(4,rootdom['28'],ds[4]['cases']['28'])
for pk,fr in [(5,22),(6,16)]:
 index={};U={}
 for k,v in rr3.items():
  f,g=map(int,k.split(':'))
  if f!=fr:continue
  assert v is not None
  z,vs=v;U[g]=z
  for h,P in vs.items():index[f'{g}:{h}']=P
 ca=ds[pk]['cases'];assert set(ca)==set(index)
 for tag,n in ca.items():
  P=index[tag];visited[pk].update(dict(P))
  if isinstance(n,list):leaf(pk,P,n);continue
  a=2677 if pk==5 else 7397067664513;visited[pk].add(a);d,_=dom(P,a);assert set(n['children'])==set(d)
  for h,n2 in n['children'].items():
   if isinstance(n2,list):leaf(pk,d[h],n2);continue
   assert pk==6 and tag=='16:2' and h=='18';a2=7614097;visited[pk].add(a2);r2,_=dom(d[h],a2);assert set(n2['children'])==set(r2)
   for j,n3 in n2['children'].items():
    K,O,ban=n3;pp=r2[j];leaf(pk,pp,[K,O]);
    if ban:
     assert ban==[5] and j=='6';X,S,D,odd=state(pp);I=Fraction(prod(sig(x,k) for x,k in pp),X)
     for q in K:
      v=val(D,q);h=v+(v%2 if (q%4==3 or odd) else 0);I*=Fraction(sig(q,h),q**h)
     assert I*Fraction(6,5)>2 and 5 not in K and 5 not in dict(pp)
for i,d in enumerate(ds):assert set(d['ecpp'])=={str(v) for v in visited[i] if v>=2**64},(i,len(visited[i]),len(d['ecpp']))
rem=set(map(int,rootdom))-set(map(int,first))-{40,46,12,28,22,16};assert rem=={1,2,18} and ct[3]==114 and ct[5]==148 and ct[6]==103
print('PASS 50/53; remaining',sorted(rem),'actual terminal rows by packet',ct,'14 extra completed secondary pairs; no key/shard credit')

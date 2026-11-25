"""Independent replay: enumerate affordable exact powers and use two-state forest DP.
The DP has two states (Euler excluded / Euler permitted), unlike generator's four.
Run: python -I -S -B Check.py packet.json.gz [receipt.json]
"""
import sys, json,gzip,math
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'RootFiveNext'));import PrimeCheck
B=10**2400;order=(19,7,11,31,13,3,5,17)
def require(x):
 if not x:raise ValueError('invalid witness')
def sigma(q,f):return (q**(f+1)-1)//(q-1)
def val(n,q):
 k=0
 while n%q==0:k+=1;n//=q
 return k
def good(q,f,ban):return all((f+1)%b!=0 if q%b==1 else pow(q,f+1,b)!=1 for b in ban)
def first(q,h,s,ban):
 if s and (q%4!=1 or any((q+1)%b==0 for b in ban)):return None
 a=h+((1-h)%4 if s else h%2)
 while not good(q,a,ban):a+=4 if s else 2
 return a

def run(d,split_five=False,support_plan=()):
 p=d['p'];e=d['e'];require(p in (13,19,31) and isinstance(e,int) and e>=2 and e%2==0);ban=order[:order.index(p)];L=d['labels'];O=dict(d['owners']);C=d['chain'];require(len(set(L))==len(L) and len(O)==len(d['owners']) and set(O)|set(O.values())<=set(L));require(set(C)=={str(z) for z in L if z>=2**64});cap=d['cap'];depth=d['depth'];require(type(cap)==int and 0<cap<=512 and 1<=depth<=12)
 for z in L:
  require(type(z)==int and z%2 and z>2);t=z
  for r in C.get(str(z),[]):require(r[0]==t);t=PrimeCheck.level(*r)
  require(2<=t<2**64 and PrimeCheck.prime64(t))
 for z in O:
  seen=set();w=z
  while w in O:require(w not in seen);seen.add(w);w=O[w]
 missing=[];stats=[0,0]
 support_plan=tuple(support_plan) or ((5,) if split_five else ())
 require(all(type(t)==int and t in L and t not in order[:order.index(p)+1] for t in support_plan) and len(set(support_plan))==len(support_plan))
 def go(P,decisions=()):
  X=math.prod(z**f for z,f in P);S=math.prod(sigma(z,f) for z,f in P);D=math.lcm(X,S//math.gcd(S,2))//X;fixed={z for z,f in P};ban=order[:order.index(p)]+tuple(t for t,v in decisions if not v);post=any(f%2 for z,f in P)
  for t,v in decisions:
   require(t not in fixed)
   if v:D=math.lcm(D,t)
  ys={q:val(D,q) for q in L if D%q==0};base=X*D//math.prod(q**k for q,k in ys.items());K={z:[] for z in L};reachable=set(ys)
  for w in L:
   path=[];q=w
   while q not in reachable and q not in fixed and q in O:path.append(q);q=O[q]
   if q in reachable:
    for t in reversed(path):K[q].append(t);reachable.add(t);q=t
  U=D*X*math.prod(reachable-set(ys));T=B//base+1
  @cache
  def cell(q,k,slot):
   best=T
   for odd in range(1+int(slot)):
    a=first(q,k,odd,ban);i=0
    if a is None:continue
    step=(4 if odd else 2)
    while q**a<best and i<cap:
     if good(q,a,ban):
      s=sigma(q,a)//(2 if odd else 1);u=s
      while (g:=math.gcd(u,U))>1:u//=g
      cost=q**a*u;vs=[]
      if cost<best:
       for t in K[q]:
        h=val(s,t)
        if h:
         n=cell(t,h,False);cost*=n;vs.append((t,h,n))
       x=cost
       if slot and not odd:
        for t,h,n in vs:x=min(x,cost//n*cell(t,h,True))
       best=min(best,x)
      i+=1
     a+=step
    best=min(best,q**a)
   return best
  if len(P)>1:
   stats[0]+=1
   if D%2==0 or any(D%z==0 for z in fixed|set(ban)) or S>2*X or X*D>B:return
   total=base;rs=[]
   for q,k in ys.items():n=cell(q,k,False);rs.append((q,k,n));total*=n
   m=total
   if not post:
    for q,k,n in rs:m=min(m,total//n*cell(q,k,True))
   cell.cache_clear()
   if m>B:return
  else:m=X*D
  if len(P)>depth or not ys:
   if len(decisions)<len(support_plan):
    t=support_plan[len(decisions)];go(P,decisions+((t,False),));go(P,decisions+((t,True),));return
   missing.append(dict(parts=[list(x) for x in P[1:]],floor=len(str(m))-1));return
  z=max(ys);c=ys[z];base=X*D//z**c;save=1
  for q,h in ys.items():
   if z==q:continue
   a=first(q,h,False,ban);base*=q**(a-h);b=None if post else first(q,h,True,ban)
   if b is not None:save=max(save,q**max(a-b,0))
  stats[1]+=1;f=c
  while z**f*base<=B*save:
   if good(z,f,ban) and (not f%2 or (not post and z%4==f%4==1 and z**f*base<=B)):go(P+[(z,f)])
   f+=1
 go([(p,e)]);return dict(p=p,e=e,closed=not missing,terminals=stats[0],split=stats[1],opened=missing)
if __name__=='__main__':
 f=Path(sys.argv[1]);d=json.loads(gzip.decompress(f.read_bytes()));r=run(d);expect=Path(sys.argv[2]) if len(sys.argv)>2 else f.with_suffix('');require(r==json.loads(expect.read_bytes()));print('PASS',r['p'],r['e'],'terminals',r['terminals'],'remaining',len(r['opened']),'closed',r['closed'])

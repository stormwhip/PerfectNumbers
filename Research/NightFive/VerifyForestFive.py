"""Second root-five-only forest replay; standard library. Check Euler coupon with rational discounts across children, independently from conditional single-Euler recursion."""
from FiveForestReplay import proof,B
from pathlib import Path
import gzip,json,sys,math
from fractions import Fraction
from functools import cache
H=Path(__file__).resolve().parent

def second(row):
 from Tree import ok,minf
 p=5;e=row['e'];A=(5**(e+1)-1)//4;K=set(row['roots']);E=dict(row['owners']);X=p*A*math.prod(E);L=row['head'];kids={z:[] for z in K|set(E)}
 for q,z in E.items():kids[z].append(q)
 def vp(s,q):
  k=0
  while s%q==0:s//=q;k+=1
  return k
 def stripped(n):
  while (g:=math.gcd(n,X))>1:n//=g
  return n
 @cache
 def comp(z,c,odd):
  f=minf(z,c,odd)
  if f is None:return None
  step=4 if odd else 2;full=flex=B+1
  for _ in range(L):
   if z**f>=max(full,flex):break
   s=(z**(f+1)-1)//(z-1)//(2 if odd else 1);v=z**f*stripped(s);save=Fraction(1)
   for q in kids[z]:
    h=vp(s,q)
    if h:
     n,m=comp(q,h,False);o=comp(q,h,True);alt=min(m,o[0]) if o else m;v*=n;save=max(save,Fraction(n,alt))
   full=min(full,v);flex=min(flex,v//save);f+=step
   while not ok(z,f):f+=step
  return min(full,z**f),min(flex,z**f)
 cs={p:vp(A,p) for p in K};v=5**e*A//math.prod(q**k for q,k in cs.items());vals=[]
 for i in [0]+[q for q,k in cs.items() if comp(q,k,True) is not None]:
  pairs=[comp(q,k,q==i) for q,k in cs.items()];w=v*math.prod(n for n,m in pairs);vals.append(w if i else w//max([Fraction(1)]+[Fraction(n,m) for n,m in pairs]))
 return min(vals)
if __name__=='__main__':
 if not __debug__:raise SystemExit('No -O')
 for arg in (sys.argv[1:] or ['Batch24.json.gz']):
  d=json.loads(gzip.decompress((H/arg).read_bytes()));
  for row in d['rows']:
   a=min(proof(row,d['ecpp']).values());b=second(row);assert min(a,b)>B;print('root 5 forest',row['e'],len(str(a))-1,len(str(b))-1)

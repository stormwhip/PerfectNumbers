"""Independent finite-cell enumeration of the private-source forest with a single Euler coupon. Run at standard library only. Graph edges are trial prime candidates, never assumed to divide unchecked sigma values."""
import json,sys,math,functools
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import PrimeCheck as pc
B=10**2400;R=(19,7,11,31,13,3,5,17)
def check(x,msg):
 if not x:raise ValueError(msg)
@functools.lru_cache(2048)
def sigma(p,f):return (p**(f+1)-1)//(p-1)
def valuation(x,r):
 t=0
 while x%r==0:t+=1;x//=r
 return t
def nonsupport(x,U):
 g=math.gcd(x,U)
 while g!=1:x//=g;g=math.gcd(x,U)
 return x

def proof(row,certs,split,present):
 check(split in (3,5,7,11,13,17,19,31) and split not in R[:1+R.index(row['p'])],'invalid split');forced=split if present else None
 p,e=row['p'],row['e'];check(p in (7,11) and type(e)==int and e>=2 and not e%2,'root');A=sigma(p,e);K=set(row['roots']);edges=row['owners'];parent=dict(edges);check(len(K)==len(row['roots']) and len(parent)==len(edges),'duplicates')
 check(A%2==1 and A%split!=0 and ((split in K)==present),'split root mismatch')
 V=set(parent)|K;check(not (K & parent.keys()),'cross root')
 for q in V:
  t=q
  if q>=2**64:
   for v in certs[str(q)]:check(v[0]==t,'broken ECPP');t=pc.level(*v)
  check(type(q)==int and q>2 and pc.prime64(t),'nonprime')
 for z in K:check(z==forced or A%z==0,'not root sigma divisor')
 kids={q:[] for q in V}
 for q,z in parent.items():check(z in V and A*p%q!=0,'invalid edge');kids[z].append(q)
 seen=set();queue=list(K)
 while queue:
  z=queue.pop();check(z not in seen,'cycle');seen.add(z);queue.extend(kids[z])
 check(seen==V,'unreachable');U=p*A*math.prod(parent)*(forced or 1);ban=R[:R.index(p)]+(() if present else (split,));cs={z:valuation(A,z) for z in K};base=p**e*A//math.prod(z**c for z,c in cs.items());cs={z:max(1,c) for z,c in cs.items()};cap=row.get('head',6);check(type(cap)==int and 1<=cap<=512,'prefix');
 den=row.get('den',1);price=dict(row.get('rho',[]));check(type(den)==int and 1<=den<=8 and set(price)<=V and len(price)==len(row.get('rho',[])) and all(type(u)==int and 0<u<den for u in price.values()),'invalid sharing weights');base=base**den*math.prod(z**(u*valuation(A,z)) for z,u in price.items());target=B**den
 @functools.cache
 def oddpossible(q):return q%4==1 and all((q+1)%b for b in ban)
 @functools.cache
 def evalnode(z,h,kind):
  # kind 0: no Euler in subtree; 1: Euler allowed in the subtree (including z); 2: Euler exactly at z. min over location of one exception via integer products.
  if kind==1:
   return min(evalnode(z,h,3),evalnode(z,h,2)) if oddpossible(z) else evalnode(z,h,3)
  sp=kind==2;f=h+((1-h)%4 if sp else h%2);step=4 if sp else 2
  if sp:check(oddpossible(z),'invalid mode')
  def admissible(a):return all((a+1)%b if z%b==1 else pow(z,a+1,b)!=1 for b in ban)
  best=target+1;n=0;ex=den-price.get(z,0)
  while n<cap:
   if z**(ex*f)>=best:break
   if admissible(f):
    S=sigma(z,f)//(2 if sp else 1);cst=z**(ex*f)*nonsupport(S,U)**den*math.prod(q**(u*valuation(S,q)) for q,u in price.items());used=[]
    for q in kids[z]:
     c=valuation(S,q)
     if c:
      cst*=evalnode(q,c,0);used.append((q,c))
    if kind==3:
     cst=min([cst]+[cst//evalnode(q,c,0)*evalnode(q,c,1) for q,c in used]);
    best=min(best,cst);n+=1
   f+=step
  while not admissible(f):f+=step
  return min(best,z**(ex*f))
 no={z:evalnode(z,h,0) for z,h in cs.items()};total=base*math.prod(no.values());vals={}
 vals[0]=min([total]+[total//no[z]*evalnode(z,h,3) for z,h in cs.items()]);
 for z,h in cs.items():
  if oddpossible(z):vals[z]=total//no[z]*evalnode(z,h,2)
 return vals

def main():
 for field in sys.argv[1:]:
  path=Path(field);path=path if path.is_file() else H/path
  import gzip
  d=json.loads(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes());
  for row in d['rows']:
   p,e,s=row['p'],row['e'],row['split'];ms=[]
   for key,flag in [('absent',False),('present',True)]:
    sub=row[key];check(sub['p']==p and sub['e']==e and sub.get('den',1)==1,'wrong cell');ms.append(min(proof(sub,d['ecpp'],s,flag).values()))
   check(min(ms)>B,'at least one split branch open');print(p,e,s,[len(str(m))-1 for m in ms],flush=True)
if __name__=='__main__':main()

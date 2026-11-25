"""Finite, emitted tree; validate every prime, exact forced multiplicity, legitimate branch, zero-output leaf, and disjoint forest. No dependency on solver or host cache."""
from QuickIndependent import I,B,F,lo,max_ab,opt,block,sigma,prod,gcd
from BankSieve import mentioned
from Rough import H,prime,prime64,level,load_duals,json,hashlib
from RefundCheck import bind
from functools import cache
import gzip,sys

def forest(x,X,D,K,edge):
 parent=dict(edge);K=set(K);V=K|set(parent);assert len(parent)==len(edge) and not K&set(parent) and all(q>2 and q in V and X*D%q!=0 and p in V for q,p in edge);children={p:[] for p in V}
 for q,p in edge:children[p].append(q)
 seen=set();stack=list(K)
 while stack:
  p=stack.pop();assert p not in seen;seen.add(p);stack.extend(children[p])
 assert V==seen
 def vp(n,p):
  k=0
  while n%p==0:n//=p;k+=1
  return k
 W=X*D*prod(parent);v={z:vp(D,z) for z in K};base=X*D//prod(p**c for p,c in v.items());
 @cache
 def node(p,c,mode):
  # 0 none, 1 Euler permitted anywhere, 2 precisely here, 3 only among children.
  special=p%4==1 and all((p+1)%z for z in (3,7,11,13,19,31))
  if mode==1:return min(node(p,c,2),node(p,c,3)) if special else node(p,c,3)
  odd=mode==2
  if odd and not special:return B+1
  f=c+((1-c)%4 if odd else c%2);step=4 if odd else 2;best=B+1;n=0
  while n<24:
   if p**f>=best:break
   if block(p,f):
    Y=sigma(p,f)//(2 if odd else 1);u=Y
    while (g:=gcd(u,W))>1:u//=g
    cost=p**f*u;active=[]
    for q in children[p]:
     a=vp(Y,q)
     if a:cost*=node(q,a,0);active.append((q,a))
    if mode==3:cost=min([cost]+[cost//node(q,a,0)*node(q,a,1) for q,a in active]);
    best=min(best,cost);n+=1
   f+=step
  while not block(p,f):f+=step
  return min(best,p**f)
 full={p:node(p,c,0) for p,c in v.items()};w=base*prod(full.values());wmin=w
 if not any(f%2 for p,f in x):wmin=min([w]+[w//full[p]*node(p,c,1) for p,c in v.items()]);
 return wmin>B

def dual(x,X,S,D,roots,ds):
 # Standalone independent leaf logic with the optimized “max over duals for each known Euler” ordering.
 e=x[0][1];m={};u=D;T=100000;P=set(roots)
 for p,f in x:P.update(mentioned(sigma(p,f),T))
 for p in P:
  h=0
  while u%p==0:u//=p;h+=1
  if h:m[p]=h
 removed=set(m)|{p for p,f in x};n=I.ilog(u,T);ab=I.LN2_LO-sum(map(max_ab,removed))-n*max_ab(T);k=e;t=S
 while t%5==0:k-=1;t//=5
 if k<0:return True
 fees=[]
 for d in ds:
  L=min(4*lo(T),d.lam_p*lo(5)) if u>1 else d.lam_p*lo(5);ev={p:opt(p,h,False,L) for p,h in m.items()};b=lo(X*D)+sum(ev.values())+d.const_no_target+d.mu*ab+sum(d.refund(p) for p in removed if p!=5)-sum(th for p,th in d.theta_map.items() if (X*D)%p==0)-(n*L+3)//4+k*L;fees.append((d,L,b,ev))
 cap=I.LN_B_HI
 if any(f%2 for p,f in x):return max(b for d,L,b,ev in fees)>cap
 for p,h in m.items():
  options=[b-ev[p]+o for d,L,b,ev in fees if (o:=opt(p,h,True,L)) is not None]
  if options and max(options)<=cap:return False
 if u>1 and all(b-L*min(k,I.ilog(u+1,5)+5)<=cap for d,L,b,ev in fees):return False
 return all(any(b-L*j+max(0,j-1)*lo(5)-d.delta_q>cap for d,L,b,ev in fees) for j in range(k+1))

def verify(pack):
 ds=load_duals();bank=json.loads((I.CERT_DIR/'DualP5.json').read_text())['duals'];ds=[bind(d,b) for d,b in zip(ds,bank)];used=set()
 @cache
 def primeok(p):
  if prime(p):return True
  k=hashlib.sha256(str(p).encode()).hexdigest()[:24];rows=pack['ecpp'][k];used.add(k);q=p
  for row in rows:assert row[0]==q;q=level(*row)
  return prime64(q)
 for es,cert in pack['trees'].items():
  e=int(es);assert 0<e<=2400 and not e%2;visited=set();stats={}
  def walk(x,tag):
   assert tag not in visited;visited.add(tag);entry=cert[tag];kind=entry[0];stats[kind]=stats.get(kind,0)+1
   X=prod(p**f for p,f in x);S=prod(sigma(p,f) for p,f in x);D=S//gcd(2*X,S)
   if kind=='basic':assert X*D>B or gcd(X*prod(F),D)>1;return
   if kind=='split':
    p=entry[1];assert primeok(p) and D%p==0 and X%p!=0;v=0;u=D
    while u%p==0:u//=p;v+=1
    f=v
    while X*u*p**f<=B:
     if not(f%2 and (any(g%2 for z,g in x) or p%4!=1 or f%4!=1)) and block(p,f):walk(x+[(p,f)],tag+':'+str(f))
     f+=1
    return
   roots=entry[1];assert len(roots)==len(set(roots)) and all(primeok(p) and D%p==0 and p>2 and X%p!=0 for p in roots)
   if kind=='dual':assert dual(x,X,S,D,roots,ds),(tag,'dual');return
   assert kind=='forest';edges=entry[2];assert all(primeok(q) and primeok(z) for q,z in edges);assert forest(x,X,D,roots,edges),(tag,'forest')
  walk([(5,e)],str(e));assert visited==set(cert);print(e,stats,flush=True)
 assert used==set(pack['ecpp'])
if __name__=='__main__':
 if not __debug__:raise SystemExit('No -O')
 verify(json.loads(gzip.decompress((H/sys.argv[1]).read_bytes())))

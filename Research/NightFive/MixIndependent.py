"""All-Euler branch replay independently enumerating exact, known forced, unknown and outside positions."""
from MixCheck import leaf
from CondIndependent import I,B,F,lo,hi,max_ab,opt,block,sigma,prod,gcd

def check(e,roots,sec,ds,depth=12,limit=10000):
 n=0;T=100000;ps=I.sieve_primes(T);base=list(map(int,roots[str(e)]));cap=I.LN_B_HI
 def rec(xs):
  nonlocal n
  n+=1
  if n>limit:return False
  X=prod(r**f for r,f in xs);s=prod(sigma(r,f) for r,f in xs);D=s//gcd(2*X,s);k=e;tmp=s
  while tmp%5==0:tmp//=5;k-=1
  if D*X>B or gcd(D,X*prod(F))>1 or k<0:return True
  from BankSieve import mentioned
  known=set(base);known.update(p for r,f in xs for p in mentioned(sigma(r,f),T))
  for r,f in xs:known.update(map(int,sec.get(f'{r}:{f}',[])))
  U=D;m={}
  for p in known:
   if U%p==0:
    v=0
    while U%p==0:U//=p;v+=1
    m[p]=v
  if leaf(X,s,m,U,xs,taken if False else any(f%2 for p,f in xs)):return True
  ordinary={p for p,f in xs}|set(m);taken=any(f%2 for p,f in xs);card=I.ilog(U,T);ab=I.LN2_LO-sum(max_ab(p) for p in ordinary)-card*max_ab(T);fees=[]
  for d in ds:
   l=d.lam_p*lo(5);l=min(l,4*lo(T)) if U>1 else l
   baseval=lo(X*D)+d.const_no_target+sum(d.refund(p) for p in ordinary if p!=5)+d.mu*ab-sum(t for p,t in d.theta_map.items() if (X*D)%p==0)-(card*l+3)//4+l*k
   even={p:opt(p,v,False,l) for p,v in m.items()};normal=baseval+sum(even.values());fees.append((d,l,normal,even))
  if taken:
   if max(b for d,l,b,v in fees)>cap:return True
  else:
   # Price each known Euler separately; weaker stored test may aggregate differently, but this is still a rigorous finite conjunction.
   def special(p,v):return all(opt(p,v,True,l) is None for d,l,b,ev in fees) or any((o:=opt(p,v,True,l)) is not None and b-ev[p]+o>cap for d,l,b,ev in fees)
   if all(special(p,v) for p,v in m.items()) and (U==1 or any(b-l*min(k,I.ilog(U+1,5)+5)>cap for d,l,b,ev in fees)) and all(any(b-l*j+max(0,j-1)*lo(5)-d.delta_q>cap for d,l,b,ev in fees) for j in range(k+1)):return True
  if not m or len(xs)>depth:return False
  p=max(m);v=m[p];remaining=B//(X*(D//p**v));f=v;pw=p**f
  while pw<=remaining:
   if (f%2==0 or (not taken and p%4==1 and f%4==1)) and block(p,f) and not rec([*xs,(p,f)]):return False
   f+=1;pw*=p
  return True
 return rec([(5,e)]),n

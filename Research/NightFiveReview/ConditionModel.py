"""Reconstruct root prefilter and recursive conditioned obligations (no NightFive imports).
Use complete exponent range, alternative exact accounting and no origin split (unless needed).
"""
from LocalModel import *
class Condition(Model):
 def run(self):
  x=[(5,self.e)];a=self.state(x);X,D,V,ws,m,u,rows=a
  known=all(all(opt(p,c,True,L) is None for d,L,pr,b in rows) or any((o:=opt(p,c,True,L)) is not None and b-pr[p]+o>LIMIT for d,L,pr,b in rows) for p,c in m.items());rough=u==1 or any(b-L*min(V,iroot(u+1,5)+J,self.e//2+J)>LIMIT for d,L,pr,b in rows);higher=all(any(b-L*s+max(lo(3125),(5*s-5)*lo(5))-d.dq>LIMIT for d,L,pr,b in rows) for s in range(V+1));assert known and rough and higher,(known,rough,higher)
  return self.cond(x,list(range(V+1)),a)
 def cond(self,x,ss,a):
  if a is None:return True
  X,D,V,ws,m,u,rows=a;un=[];O=[math.gcd(w,u) for w in ws];split=(math.prod(O)==u and all(math.gcd(v,w)==1 for i,v in enumerate(O) for w in O[i+1:]));P=self.P
  for s in ss:
   if s>V:continue
   y=5**s;Q=max(5,2*y-1);lq=lo(Q);ll=lq+lo(2)-hi(3);bare=lq+ll;gap=lo(Q*Q*y)-hi(max(P,Q)*(P//y+4)); bbs=[(d,L,pr,b-L*s-(min(d.dq,d.mu*ab(Q)) if Q>=10**18 else d.dq)) for d,L,pr,b in rows]
   def permits(w):return (s==0 or w>=Q*((-w)%(2*y)))
   def fixed():
    for (r,f),w in zip(x[1:],ws[1:]):
     if not permits(w):continue
     h={};
     for j in range(1,f+2):
      if not (f+1)%j:h[j]=(r**j-1)//math.prod(n for k,n in h.items() if not j%k)
     assert math.prod(n for k,n in h.items() if k>1)==w
     if any(permits(z) for k,z in h.items() if k>1):return True
    return False
   if fixed():un.append(s);continue
   if any(b+lq>LIMIT for d,L,pr,b in bbs):continue
   if s==0:un.append(s);continue
   def emitter(j):
    cost=lq+ll*5**j;bs=[(b-L*j+cost,d,pr) for d,L,pr,b in bbs]
    if not any(b-d.de>LIMIT for b,d,pr in bs):return False
    if j:
     if u>1 and not any(b-hi(u)>LIMIT for b,d,pr in bs):return False
     return all(any(b-pr[z]-hi(z**v)>LIMIT for b,d,pr in bs) for z,v in m.items())
    if split:
     if any(z>1 and not any(b+max(-hi(z),gap-cost if i==0 else -hi(z))>LIMIT for b,d,pr in bs) for i,z in enumerate(O)):return False
    elif u>1 and not any(b-hi(u)>LIMIT for b,d,pr in bs):return False
    for z,v in m.items():
     cr=0;t=self.A
     while t%z==0:t//=z;cr+=1
     assert cr<=v
     g=v+(v%2);h=iroot(B//(X*(D//z**v)),z)
     while g<=h and not (good(z,g) and permits(sig(z,g))):g+=2
     if g>h:continue
     fee=lq+(g-v)*lo(z)
     if cr:fee=max(fee,gap-hi(z**(v-cr)))
     if not any(b+fee-pr[z]>LIMIT for d,L,pr,b in bbs):return False
    return True
   # If Q is small do not assume the emitter has positive supply only in order>1 case.
   if (32*5**self.e*Q**6<243*B and (Q<=M+1 or not all(emitter(j) for j in range(1,min(J,V-s)+1)))) or not emitter(0):un.append(s)
  if not un:self.stats['condition-closed']+=1;return True
  if not m:return False
  p=max(m);c=m[p];fs=[f for f in range(c,iroot(B//(X*(D//p**c)),p)+1) if good(p,f) and (f%2==0 or (f==1 and p%4==1 and self.A%p and vp(p+1) in un))];self.stats['splits']+=1;self.eg.setdefault('splits',[]).append(dict(path=[(str(p),f) for p,f in x],s=[min(un),max(un),len(un)],exponents=fs));
  # Odd exponent here would require a separate assigned-Euler proof; never skip it.
  return all(f%2==0 and self.cond(x+[(p,f)],un,self.state(x+[(p,f)])) for f in fs)
if __name__=='__main__':
 cert=json.loads((R/'IndicatorCapacity/Certificates/DualP5.json').read_text());ps=primes(cert['R_act']);pack=json.loads((NF/'Batch8.json').read_text());ds=[Bank(v,cert['R_act'],ps) for v in cert['duals']+pack['duals']];
 for e in list(map(int,sys.argv[1:])) or [460,568,592]:
  tr=Condition(e,pack,ds);q=tr.run();print(json.dumps(dict(e=e,passed=q,stats=tr.stats,examples=tr.eg)),flush=True);assert q

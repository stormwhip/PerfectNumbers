"""Exact conditions on the two live fibers of (7,438), no third-party dependency."""
from math import gcd,prod,isqrt
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H));from Prices import loss
p=7;e=438;t=572749682520506652634407616247;B=10**2400
def sigma(r,h):return (r**(h+1)-1)//(r-1)
def v(x,p):
 assert x>0;h=0
 while x%p==0:x//=p;h+=1
 return h
def strip(n,ps):
 for r in ps:n//=r**v(n,r)
 return n
def outside(Z,m):
 Q=2*m-1
 if Q>Z:return True
 k=Z*pow(Q,-1,4*m)%(4*m)
 return Z//Q<4*m and not (0<k<=Z//Q and Z%k==0)
def prove_prime(t):
 # Recursive Lucas certificate using complete factorizations, privately generated.
 table=json.loads((H/'Lucas.json').read_bytes())
 def check(n):
  if n<100000:return n>=2 and all(n%i for i in range(2,isqrt(n)+1))
  g,ps=table[str(n)];return prod(int(z)**h for z,h in ps.items())==n-1 and pow(g,n-1,n)==1 and all(check(int(z)) and gcd(pow(g,(n-1)//int(z),n)-1,n)==1 for z in ps)
 assert check(t)
def run(f,r):
 S=sigma(p,e)*sigma(t,f);X0=p**e*t**f;D0=strip(S,[p,t]); c=f-1
 assert v(S,t)==1 and v(S,p)==0 and v(D0,r)==1 and D0%19
 assert (t-1)==2*439*97613*6682864888306503255889 and (t-1)%4==2
 # Exhaust small odd orders without needing primality of the large factors.
 orders=[o for o in range(3,5101,2) if (t-1)%o==0]; assert orders==[439]
 assert 3**5100>B and t>5101
 for z in range(3,100000,2):
  if X0*z**438>B:break
  if all(z%i for i in range(2,isqrt(z)+1)) and pow(z,439,t)==1 and z%t!=1:
   assert X0*(D0//z**v(D0,z))*z**438>B or z in [7,t,19]
 else:assert False
 for z in range(5,100000,4):
  if X0*z**877>B:break
  assert not all(z%i for i in range(2,isqrt(z)+1)) or pow(z,878,t)!=1 or pow(z,2,t)==1 or z in [p,t,19]
 else:assert False
 m0=t**c;q0=2*m0-1; A=sigma(p,e)//t; C=sigma(t,f)
 assert gcd(A,C)==gcd(A*C,X0)==1 and outside(A,m0) and X0*D0*q0**5>B
 # q cannot divide C: t has odd order at q while (t/q)=-1.
 # q^1 exact, all nonfixed suppliers now ordinary. s=v_7(q+1).
 U=loss(p,e,19,10);n,d=U.as_integer_ratio(); live=[]; killed=[]; naive=[]
 h=0
 while X0*D0//r*r**(h+2)<=B:
  h+=2; Z=sigma(r,h);X=X0*r**h; D=strip(S*Z,[p,t,r]);
  if S*Z%19==0 or v(S*Z,p)>e or v(S*Z,t)>f or X*D>B:continue
  naive.append(h);assert v(Z,t)==0
  cp=e-v(Z,p);Zout=strip(Z,[p,t,r]); blocks=[A,C//r,Zout];assert prod(blocks)==D
  # Split D into pairwise coprime blocks; conservative shortcut merges intersecting blocks.
  blocks=[b for b in blocks if b!=1]
  while any(gcd(b,g)>1 for i,b in enumerate(blocks) for g in blocks[i+1:]):
   i,j=next((i,j) for i,b in enumerate(blocks) for j,g in enumerate(blocks) if j>i and gcd(b,g)>1); blocks[i]*=blocks.pop(j)
  survives=False
  for s in range(cp+1):
   m=m0*p**s;Q=2*m-1; wp=p**(19*(cp-s));
   if (X*Q)**10*wp*d>B**10*n:continue
   # q is distinct from r (3 mod 4), external to A,C; q may divide Zout.
   external=outside(Zout,m)
   if X0*D0*Q>B or (external and X*D*Q>B):continue
   if external:
    ov=max(blocks+[1]); lo,hi=0,cp-s+1
    while lo<hi:
     mid=(lo+hi)//2
     if 2*X*D*Q*Q*p**mid>3*B*ov:hi=mid
     else:lo=mid+1
    u=lo-1
    if u<0 or (2*X*Q*Q*p**u)**10*p**(19*(cp-s-u))*d>(3*B)**10*n:continue
   survives=True;break
  (live if survives else killed).append(h)
 print('438',f,'secondary',r,'directly live',len(naive),'after',len(live),'surviving',live,flush=True)
 return naive,live,killed
if __name__=='__main__':
 assert __debug__;prove_prime(t)
 for f,r,lo,hi,cap in [(10,67,228,292,300),(12,27431,74,110,110)]:
  prove_prime(r); assert r%4==3
  direct,live,killed=run(f,r);assert direct==list(range(2,cap+1,2)) and killed==list(range(lo,hi+1,2))

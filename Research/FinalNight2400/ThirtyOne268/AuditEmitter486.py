"""Independent cell-by-cell reclassification of (7,486). Reuses certified independent U/domain, does not import PairSeven. Uses float only as search hint; threshold bracket always verified exactly."""
import sys,runpy,time,hashlib
from pathlib import Path
from math import gcd,prod,log2
H=Path(__file__).resolve().parent;src=H.parent/'AuditNext/Check486.py';raw=runpy.run_path(str(src));U=raw['U'];start=time.monotonic();p=7;s=349667;t=1229048719;e=486;B=10**2400;A=(7**487-1)//6
pp=[7**u for u in range(487)];q1=lambda a,k:(2*k*pp[a]-1)

def ext(z,m):
 Q=2*m-1
 if Q>z:return True
 cap=z//Q
 if cap>=4*m:return False
 n=z*pow(Q,-1,4*m)%(4*m);return not(1<=n<=cap and z%n==0)

def audit(i,j):
 X=pp[-1]*s**i*t**j;Z=[A,(s**(i+1)-1)//(s-1),(t**(j+1)-1)//(t-1)];S=prod(Z);D=S//gcd(S,X);cp=e-raw['val'](S,7);ct=j-raw['val'](S,t);cs=i-raw['val'](S,s);assert cs==i-1;T=s**cs;M=pp[cp]*t**ct;z=[v//gcd(X,v)for v in Z];assert prod(z)==D
 H=max(v*prod(gcd(v,u)for k,u in enumerate(z)if k!=n)for n,v in enumerate(z));L=X**10*M**19;right=B**10*U;sz=X*D
 for b in range(ct+1):
  tv=t**b;k=T*tv;R=right*tv**19
  # q=2k*7^a-1; the basic RHS crossing occurs near the indicated base-7 exponent. No floating threshold is trusted.
  approx=(log2(L)+10*(1+log2(k))-log2(R))/(9*log2(7));a=min(cp+1,max(0,int(approx)))
  def basic(n):return L*q1(n,k)**10>R*pp[n]**19
  while a<=cp and basic(a):a+=1
  while a>0 and not basic(a-1):a-=1
  assert a==0 or basic(a-1)
  if a>cp:continue
  while a<=cp:
   m=pp[a]*tv;q=2*T*m-1
   # First sufficient permanent size or permanent emitter exclusion; if no permanence, explicitly advance (including b==0).
   root_ext=a>0 or ext(z[0],T*m);third_ext=b>0 or ext(z[2],T*m)
   if not(root_ext and third_ext):return False
   perman=(a>0 or q>z[0]) and (b>0 or q>z[2]);
   if sz*q>B:
    if perman:break
   else:
    maxY=min(M//m,3*B*H//(2*sz*q*q));# y=1 allowed, 0 proves impossibility.
    if (2*X*q*q)**10*M**19<=(3*B)**10*U*m**19*maxY**9:return False
    if a>0 and b>0:break
   a+=1
 return True
extra=[];left=[]
for ij in raw['rem']:
 (extra if audit(*ij) else left).append(ij)
allcut=sorted(raw['done']+extra);assert len(extra)==150 and len(left)==612 and len(allcut)==905;print('PASS independent extension',len(raw['done']),len(extra),len(left),'upper survivor coordinates',max(i for i,j in left),max(j for i,j in left),'extra seconds',round(time.monotonic()-start,3),'cells digest',hashlib.sha256(repr(allcut).encode()).hexdigest(),flush=True)

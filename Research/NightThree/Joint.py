"""Root-3 joint supplier/source replay; Python stdlib, no data downloaded. Run with -B."""
from pathlib import Path
import sys,json,math,argparse,gzip
from functools import cache
from itertools import accumulate
from hashlib import sha256
H=Path(__file__).resolve().parent; R=H.parent;sys.path.insert(0,str(R/'EveningRoot3'));import IndependentEvening as I
B=10**2400;T=I.T;BAN=I.BAN
@cache
def powerlog(n,b):
 if n<1:return -1
 j=max(0,int(math.log(n)/math.log(b)));z=b**j
 while z>n:j-=1;z//=b
 while z*b<=n:j+=1;z*=b
 return j
@cache
def rates(z,f,cap):
 j=powerlog(f+1,3);out=[]
 while True:
  g=3**(j+1)-1
  if not I.legal(z,g):break
  cost=z**(g-f)
  if cost>cap:break
  out.append(cost);f=g;j+=1
 return tuple(out)
@cache
def res(h,u):
 if u==1:return 0,0,T+1
 stride=math.lcm(3,2*h); start=1+((T-1)//stride+1)*stride; last=start+stride*1000; floor=last
 for x in range(start,last,stride):
  if u%x==0:floor=x;break
 return powerlog(u,floor*floor),powerlog(u,floor),floor
@cache
def pricebase():return sorted(v for z in I.SUP for v in rates(z,0,(T+1)**2))
def audit(e,fs,details=False,finance=False,phisource=False):
 A=(3**(e+1)-1)//2;pe=3**e;P=3*pe; d,u=I.factor_small(A)
 for z in sorted(set(fs)):
  if z<=T:continue
  if A%z:raise ValueError('invalid forced divisor')
  while u%z==0:d[z]=d.get(z,0)+1;u//=z
 f={z:I.minimum(z,c) for z,c in d.items()};extr={z:z**(f[z]-c) for z,c in d.items()};M=pe*A*math.prod(extr.values());disc=max([1]+[v for z,v in extr.items() if z%4==1 and all((z+1)%b for b in BAN)]);G=sum(powerlog(m+1,3) for z,m in f.items() if z%3==1)
 # Maximal count of suppliers in each block; an unknown supplier may have one positive marginal of size only z (all subsequent increments >= z^2).
 chunks=[(h,math.gcd(u,U)) for h,U in I.blocks(e).items()];assert math.prod(v for _,v in chunks)==u
 tariffs=pricebase().copy();cap=(T+1)**2
 for z,m in f.items():
  if z%3==1:
   # Keep old rates as additional phantom opportunities; never remove too much.
   tariffs.extend(rates(z,m,cap))
 for h,v in chunks:
  g,count,l=res(h,v);G+=g;tariffs.extend([l]*count)
 C=[1,*accumulate(sorted(tariffs+[cap]*e)[:e],lambda x,y:x*y)]; missed=[]; highs=[]
 for s in range(e,-1,-1):
  y=3**s;Q=max(5,2*y-1);k=e-s;c=C[max(0,k-G)]; m=M*c
  if m>B*disc:continue
  high=max(3125,3**max(0,5*s-5));ordinary=pe*I.ordinary()[k]
  if ordinary*high<=B and (y<=1+powerlog(B,5) or m*high<=B):highs.append(s)
  if s and m*Q>B:continue
  if not s or 8*pe*Q**4<27*B:missed.append(s);continue
  if 2*ordinary*Q*Q>=3*B:continue
  # Exterior source distinct from A. Internal unknown: balance lemma. Known sources permit a finite CRT check.
  rhs=B*max(P,Q)*(P//y+4);L=m*Q*Q*y
  if 2*m*Q*Q<3*B:missed.append(s);continue
  if u>1 and L<rhs:
   if not phisource:missed.append(s);continue
   from SourcePhi import source
   if any(source(e,h,v,s,M,c) for h,v in chunks if v>1):missed.append(s);continue
  for z,c0 in d.items():
   if L>=rhs*extr[z]:continue
   limit=B//(m*Q);stop=f[z]+powerlog(limit,z); g=f[z]
   while g<=stop:
    if (g+1)%3 and I.legal(z,g):
     sig=(z**(g+1)-1)//(z-1);w=(-sig)%y or y
     if sig>=Q*w:break
    g+=2
   if g<=stop:missed.append(s);break
 if finance and missed and min(missed)>0:
  import Finance as F
  budget=F.bounds(e,pe,A,u,{z:(d[z],f[z]) for z in d},M,e,missed,T+1,{3},source_h=5); rem=[]
  for s in missed:
   y=3**s;Q=2*y-1;k=e-s;n,b=budget[s]
   # Treat all internal emitters via the uniform D,E bound, deducting the largest known parity premium if the emitter is already priced through its even floor. Exterior emitter abundance was debited in the dual.
   if 8*pe*Q**4<27*B or 2*M*n*Q**2<3*B*b or (u>1 and M*n*Q**2*y<B*b*max(P,Q)*(P//y+4)):rem.append(s);continue
   for z in d:
    if M*n*Q**2*y>=B*b*max(P,Q)*(P//y+4)*extr[z]:continue
    stop=f[z]+powerlog(B*b//(M*Q*n),z)
    for g in range(f[z],stop+1,2):
     if (g+1)%3 and I.legal(z,g):
      sg=(z**(g+1)-1)//(z-1);w=(-sg)%y or y
      if sg>=Q*w:break
    else:continue
    rem.append(s);break
  missed=rem
 return missed,highs

def base():
 a=json.loads((R/'EveningMerge/Audit.json').read_text());assert len(a['remaining_shards'])==880
 return [t for t in a['remaining_shards'] if t['root']==3]

def delta(es):return [s['id'] for s in base() if s['remaining_actuals'] and set(s['remaining_actuals'])<=set(es)]

def discover():
 from sympy import isprime
 D=Path('E:/PerfectNumbers/upstream/Research/EveningRoot3');raw=json.loads((D/'Candidates.json').read_text());es={e for t in base() for e in t['remaining_actuals']};rows=[];ranks=[]
 for e in sorted(es,reverse=True):
  fs=[int(v) for v,k in raw[str(e)] if int(v)>T and isprime(int(v))];one,hi=audit(e,fs);ranks.append([e,len(one),len(hi),one[:3],hi[:3]])
  if not(one or hi):rows.append({'e':e,'fs':list(map(str,fs))});(H/'Screen.json').write_text(json.dumps(rows)+'\n')
  print(e,len(one),len(hi),flush=True)
 (H/'Ranks.json').write_text(json.dumps(ranks)+'\n')
if __name__=='__main__':discover()

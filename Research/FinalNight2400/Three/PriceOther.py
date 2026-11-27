"""Generalization of the hard66 product to siblings with one or more blocks."""
from pathlib import Path
from math import gcd,prod
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Night2400/B'));from EulerRoute import F,Q,P,R,cap_two,sigma,B

def score(prefix):
 if any(h%2 for _,h in prefix):return None
 z,h=prefix[-1];X,S,c,V,_=cap_two(prefix,(Q,z));D=S//gcd(S,X);assert gcd(D,X)==1
 if V<=B:return ('under',V.numerator.bit_length()-V.denominator.bit_length())
 bs0=[sigma(r,e)//gcd(sigma(r,e),X) for r,e in prefix];bs=[b for b in bs0 if b>1];assert prod(bs)==D
 # For this bound cluster blocks until coprime, keeping any one emitter inside at most one cluster.
 clusters=[]
 for b in bs:
  same=[w for w in clusters if gcd(w,b)>1];clusters=[w for w in clusters if w not in same];clusters.append(b*prod(same))
 bmax=max(clusters);good=0;left=0;internal=0;weak=None
 for i in range(c[0]+1):
  for j in range(c[1]+1):
   m=Q**i*z**j;a=2*m-1
   if V*a>B*m*m:continue
   poss=False
   for b in bs:
    u=b*pow(a,-1,4*m)%(4*m) or 4*m;hi=b//a
    if u<=hi and ((hi-u)//(4*m)>16 or any(not b%v for v in range(u,hi+1,4*m))):poss=True;break
   if poss:internal+=1;continue
   if X*D*a>B:continue
   floor=4*V*X*D*a**4/(9*m*m*bmax);weak=floor if weak is None else min(weak,floor)
   if floor>B**2:good+=1
   else:left+=1
 return ('result',good,left,internal, (weak.numerator.bit_length()-weak.denominator.bit_length()) if weak else None)

def main():
 tree=json.loads(gzip.decompress((H/'HardTree.json.gz').read_bytes()))['tree'];t=0
 for j,v in tree['cases'].items():
  t0=[*F[:3],(R,int(j))]
  if v and v['type']=='forest':continue
  if not v or j in ('2','4','8','12','28'):print('price',j,None,score(t0),flush=True)
  if not v:continue
  for k,c in v['cases'].items():
   if not c and int(k)%2==0:print('price',j,k,score([*t0,(v['q'],int(k))]),flush=True)
if __name__=='__main__':main()

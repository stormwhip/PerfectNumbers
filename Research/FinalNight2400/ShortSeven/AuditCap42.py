"""Zero-author-import verification of the mixed-source cap Q^5 with positive 173 supply."""
from math import gcd,isqrt,lcm
from pathlib import Path
import json,gzip,hashlib,collections
p,R=7,173;Q=(7**13-1)//6;B=10**2400;X=p**12*Q**42*R**2;M=Q**5
assert __debug__ and Q>5100 and all(Q%k for k in range(2,isqrt(Q)+1)) and all(R%k for k in range(2,isqrt(R)+1)) and 3**5100>B and R-1==4*43 and (Q-1)%R
counts=collections.Counter()
for o in range(3,5101,2):
 if (Q-1)%o:continue
 div=[k for k in range(2,o+1) if o%k==0 and all(k%g for g in range(2,isqrt(k)+1))];a=next(pow(g,(Q-1)//o,Q) for g in range(2,300) if all(pow(pow(g,(Q-1)//o,Q),o//k,Q)!=1 for k in div));assert pow(a,o,Q)==1
 for k in (43,173):
  h=lcm(o,k)-1
  if h>=5100 or X*3**h>B:continue
  counts['feasible order cases']+=1;assert X*M**h>B
  if X*5000**h>B:
   rr=[r for r in range(3,5000,2) if pow(r,o,M)==1];counts['small search']+=1
  else:
   # Fixed Teichmuller/primitive powers, instead of Newton expansion of the generator.
   y=a;m=Q
   for _ in range(4):m*=Q;y=pow(y,Q,m)
   rr=[pow(y,j,M) for j in range(1,o+1) if gcd(o,j)==1];assert len(rr)==len(set(rr));counts['lift search']+=1
  for r in rr:
   if r<3 or not r%2 or r in (7,19,Q,R) or X*r**h>B or r%Q==1:continue
   if (k==173 and r%R!=1) or (k==43 and (r%R==1 or pow(r,43,R)!=1)):continue
   assert pow(2,r-1,r)!=1,(o,k,r)
F=Path(__file__).resolve().parents[1]/'SevenNext/CapEvidence.json.gz';d=json.loads(gzip.decompress(F.read_bytes()));cases=sorted(map(int,d['nodes']));assert cases==[172,180,192,196,198,200,202,204,206,208,210]
for h in cases:
 rows=[(7,12),(Q,42),(R,h)];X=1;S=1
 for z,f in rows:X*=z**f;S*=(z**(f+1)-1)//(z-1)
 D=S
 while (g:=gcd(D,X))>1:D//=g
 assert X*D<=B and all(D%z==0 and z not in dict(rows) for z in d['nodes'][str(h)])
print('PASS Q=',Q,'bound u<=4 on joint ordinary source only',dict(counts),'cases',cases,'large labels',len(d['ecpp']),'SHA',hashlib.sha256(F.read_bytes()).hexdigest())

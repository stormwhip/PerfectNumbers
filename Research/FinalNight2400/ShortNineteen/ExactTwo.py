"""Two exact secondary exclusions below exact first exponents 2. No whole-fiber claim."""
import sys,json
from pathlib import Path
from math import gcd,prod
H=Path(__file__).resolve().parent;Root=H.parents[1];sys.path.insert(0,str(Root/'Session20261126'));from PivotCheck import C,B
Q={330:1214428680506010004551311201724184433986966434253654794712076383,420:28174642921954703272833689609691232580811241064837460583}
R={330:2649006202622389754026474949684537136117722932291062868195158132223440533168779423867212541,420:18716166489844799458885230781362655242022878296316554735036307387001821111739679109236269675618028263}
L=541060314202200985634836209806257

def verify(e):
 q,r=Q[e],R[e];Hist=Root/'Night2400'/('C2' if e==330 else 'C')
 certs={q:'PivotECPP.json',r:'Split8ECPP.json' if e==330 else 'Forced8ECPP.json'}
 def prime(n):
  if n in certs:
   for row in json.loads((Hist/certs[n]).read_bytes()):assert row[0]==n;n=C.pc.level(*row)
  if n==L:
   fs=[2,2,2,2,3,7,7,7,619,2347,157823,143329732348247561];assert prod(fs)==n-1 and all(C.pc.prime64(z) for z in fs)
   return any(pow(b,n-1,n)==1 and all(gcd(pow(b,(n-1)//z,n)-1,n)==1 for z in fs) for b in range(2,100))
  return C.pc.prime64(n)
 assert prime(q) and prime(r) and C.sigma(19,e)%q==0 and C.sigma(q,2)%r==0
 prefix=[(19,e),(q,2)];s=C.State(prefix);assert not s.conflict
 c=C.valuation(s.D,r);h=c;live=[]
 while s.base//r**c*r**h<=B:
  if s.possible(r,h,c):
   z=C.State(prefix+[(r,h)])
   if not z.conflict and z.base<=B and prod(C.sigma(b,f) for b,f in z.rows.items())<=2*z.X:live.append(h)
  h+=1
 assert live==([1,2,4,5,6,8] if e==330 else [2,4,6]);g=live[-1];s=C.State(prefix+[(r,g)])
 roots=[3,7,L] if e==330 else [3,701,11243,57331,3228751,14137697557]
 assert all(prime(b) for b in roots);C.validate_forest(s,roots,[],128,prime);lo,_=C.Forest(s,roots,[],128).lower();assert lo>B
 print('PASS f2 secondary',e,g,'direct domain',live,'tail',h,'all-Euler floor',len(str(lo))-1)
if __name__=='__main__':
 for e in [330,420]:verify(e)

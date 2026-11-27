from pathlib import Path
import json,math,sys
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[1];D=R.parent/'Build';sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B,floor10
Q=3602407438103418087310110702859943140744217508967;P=7;root=[(P,430)];val=C.valuation;sig=C.sigma
from fractions import Fraction
@cache
def loss7():
 p=7;n=430;roots=[2,4];out={};m=p
 for j in range(1,n+1):
  for r in roots:
   # Ordinary prime r, or the square of admissible Euler prime; even representatives cannot lose because next representative exceeds m.
   if r<=2 or not r%2 or r>=m:continue
   z=math.isqrt(r);ok=lambda z:z>=3 and z%2 and z not in (7,19,Q) and pow(2,z-1,z)==1
   if ok(r) or z*z==r and ok(z):out[r]=max(out.get(r,1),Fraction(m*m,r*r))
  m*=7;roots=[pow(r,7,m) for r in roots]
 return math.prod(out.values(),start=Fraction(1)),len(out)
if __name__=='__main__':
 L,n=loss7();print('loss7 labels',n,'bits',L.numerator.bit_length()-L.denominator.bit_length());
 for f in (2,4,12):
  t=json.loads((D/f'Even430F{f}.json').read_bytes());z=max(t['roots']);
  for pp in sorted(D.glob(f'Even430F{f}J*.json')):
   j=int(pp.stem.split('J')[1]);r=root+[(Q,f),(z,j)];s=C.State(r);a=json.loads(pp.read_bytes());k=a['roots'];o=a['owners'];s.fixed_euler=True;F=C.Forest(s,k,o,a['head']);v=F.lower()[0];verts=set(k)|{x for x,u in o};c=430-sum(val(sig(x,h),7) for x,h in r);bound=0;missing=[]
   for x in verts:
    if not C.euler(x,s.bad):continue
    v7=val(x+1,7);price=s.X*x*7**(2*(c-v7))*L.denominator//L.numerator
    if price<=B:missing.append((x,v7));
   print(f,j,'ord',floor10(v),'X',floor10(s.X),'missing',len(missing),'of',len(verts),'q candidates',sorted(missing,key=lambda t:-t[1])[:4],flush=True)

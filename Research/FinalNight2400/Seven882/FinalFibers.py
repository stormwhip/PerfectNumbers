from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Special import *
from collections import Counter

def rawdomain(row,z):
 s=C.State(row);v=C.valuation(s.D,z);assert z not in s.rows and z not in s.bad and v>0;out={};h=v
 while s.base//z**v*z**h<=B:
  if s.possible(z,h,v):
   r=row+[(z,h)];s2=C.State(r)
   if not s2.conflict and s2.base<=B and prod(C.sigma(p,a) for p,a in r)<=2*s2.X:out[str(h)]=r
  h+=1
 return out

def verify(f):
 assert __debug__ and f in (1,2,4,8);d=json.loads(gzip.decompress((H/f'Done{f}.json.gz').read_bytes()));book=d['ecpp'];used=set();stats=Counter()
 @cache
 def prime(z):
  assert type(z)==int and z>2;y=z
  if z>=2**64:
   used.add(str(z));
   for r in book[str(z)]:assert y==r[0];y=C.pc.level(*r)
  assert C.pc.prime64(y);return True
 assert prime(7) and prime(Q) and C.valuation(C.sigma(*ROOT),Q)==1 and d['first']==f
 def walk(row,m,t):
  kind=t['type'];stats[kind]+=1;s=state(row,m)
  if kind=='conflict':assert s.conflict;return
  if kind=='ban':assert s.conflict or gcd(s.D,prod(s.bad))!=1 or bool(s.present & (set(s.bad)-s.rows.keys()));return
  assert not s.conflict
  if kind=='masks':
   assert m==0 and f in (2,8) and set(map(int,t['cases']))=={50,58,178}
   for mask,u in t['cases'].items():walk(row,int(mask),u)
  elif kind=='split':
   z=t['q'];assert prime(z);cs=rawdomain(row,z);assert set(cs)==set(t['cases']),(row,z,set(cs)^set(t['cases']))
   for e,r in cs.items():walk(r,m,t['cases'][e])
  elif kind=='forest':
   k=t['roots'];o=t['owners'];h=t['head'];C.validate_forest(s,k,o,h,prime);assert C.Forest(s,k,o,h).lower()[0]>B
  elif kind=='abun':
   from fractions import Fraction
   k=t['roots'];assert len(k)==len(set(k)) and all(prime(z) and z not in s.rows and z not in s.bad and (s.D%z==0 or z in s.present) for z in k);b=Fraction(prod(C.sigma(z,h) for z,h in row),s.X);rates=[Fraction(1)]
   for z in k:
    v=max(1,C.valuation(s.D,z));h=v+v%2
    while not C.permitted(z,h,s.bad):h+=2
    even=Fraction(C.sigma(z,h),z**h);b*=even
    if not s.fixed_euler and C.euler(z,s.bad):
     h=v+(1-v)%4
     while not C.permitted(z,h,s.bad):h+=4
     rates.append(Fraction(C.sigma(z,h),z**h)/even)
   assert b*min(rates)>2
  elif kind=='price':assert s.fixed_euler and priced(row)>B
  elif kind=='square':assert square(row)
  else:
   assert kind=='win';k=t['roots'];assert all(prime(z) and z not in s.rows and s.D%z==0 for z in k) and len(k)==len(set(k));assert not sevenwin(row,k)
 walk([ROOT,(Q,f)],0,d['tree']);assert used==set(book);print('PASS',f,'canonical' if f in (1,4) else 'on historically remaining masks 50,58,178',dict(stats),'certs',len(book),flush=True)
if __name__=='__main__':
 for f in map(int,sys.argv[1:]):verify(f)

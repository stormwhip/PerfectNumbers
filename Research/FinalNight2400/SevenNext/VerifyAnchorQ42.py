"""Six further complete even 173 fibers, with a certified largest anchor and full integer-domain replay."""
import sys,gzip,json
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from EvenAnchor import go,Q,R,C,val;from SimulCap import check
B=10**2400;dom={130:[1,2],136:[2],138:[1],156:[1,2],176:[1,2,4],182:[2,4,6]}
if __name__=='__main__':
 assert __debug__ and check(5)==[] and C.pc.prime64(Q) and C.pc.prime64(R) and C.sigma(7,12)==Q and (Q-1)%R!=0 and R-1==4*43
 z=json.load(gzip.open(H/'AnchorQ42.json.gz'));assert set(map(int,z['nodes']))==set(dom);used=set();small=[r for r in range(3,10000,2) if C.pc.prime64(r)]
 @cache
 def pp(n):
  y=n
  if n>=2**64:
   used.add(str(n))
   for row in z['ecpp'][str(n)]:assert row[0]==y;y=C.pc.level(*row)
  return C.pc.prime64(y)
 for k,fs in z['nodes'].items():
  h=int(k);rows=[(7,12),(Q,42),(R,h)];s=C.State(rows);a=max(fs);assert len(set(fs))==len(fs) and all(pp(r) and s.D%r==0 and r not in s.rows for r in fs);v=val(s.D,a);i=v;live=[]
  while s.base//a**v*a**i<=B:
   if s.possible(a,i,v):
    t=C.State(rows+[(a,i)])
    if not t.conflict and t.base<=B:
     live.append(i);known=sorted(set(fs)|{p for p in small if p not in t.rows and C.sig_odd(a,i)%p==0});ok,fail=go(h,known,a,i);assert ok,(h,i,fail)
   i+=1
  assert live==dom[h];print('PASS',h,'anchor bits',a.bit_length(),'complete live',live,'size tail',i,flush=True)
 assert used==set(z['ecpp'])

"""Complete mixed 19/10 source prices at actual 7^438,t^10,67^h. Safe only under the preceding proved Euler q^1 and t^9 constraint."""
from pathlib import Path
from functools import cache
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Price67Cut import go,C,B,p,r,t,T,V
HS=[192,194,196,198,202,204,206,208,210,224]
def main():
 assert __debug__ and C.pc.prime64(p) and C.pc.prime64(r) and r-1==2*3*11 and (p-1)==6 and 3**5100>B;V.prove_prime(t)
 for l in (p,r):assert (2*l+1)**(10*(l-1))>l**19 and 3**(10*3*(l-1))>l**19
 z=json.load(gzip.open(H/'Mixed67Primes.json.gz'));assert set(z['nodes'])=={'67'} and sorted(map(int,z['nodes']['67']))==HS;used=set()
 @cache
 def prime(q):
  y=q
  if q>=2**64:
   used.add(str(q))
   for row in z['ecpp'][str(q)]:assert row[0]==y;y=C.pc.level(*row)
  return C.pc.prime64(y)
 for k,fs in z['nodes']['67'].items():
  h=int(k);sig=C.sigma(r,h);assert len(fs)==len(set(fs)) and all(prime(y) and y not in (7,r,t,19) and sig%y==0 for y in fs);ok,fail=go(h,fs);assert ok,(k,fail);print('mixed 7/67',h,flush=True)
 assert used==set(z['ecpp']);print('PASS exact R67 conditional powers',HS,flush=True)
if __name__=='__main__':main()

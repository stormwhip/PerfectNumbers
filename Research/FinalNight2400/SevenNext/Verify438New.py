"""37 further secondary valuations for 7^438. The fixed q forcing is the previously audited Seven/Proof.md statement."""
from pathlib import Path
from functools import cache
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Seven438One as O, Seven438Joint as J
from Odd42 import C,B
D={67:[148,172,190,200,212,214,216,218,220,222,226,294,296,298,300],27431:list(range(30,73,2))}
def main():
 assert __debug__;data=json.load(gzip.open(H/'New438Credits.json.gz'));assert set(map(int,data['nodes']))==set(D);J.V.prove_prime(J.t);used=set()
 @cache
 def prime(n):
  y=n
  if n>=2**64:
   used.add(str(n))
   for row in data['ecpp'][str(n)]:assert row[0]==y;y=C.pc.level(*row)
  return C.pc.prime64(y)
 assert all(prime(n) for n in (67,27431,7)) and (27431-1)==2*5*13*211 and all(prime(n) for n in (5,13,211)) and 3**5100>B
 for rr,hmap in data['nodes'].items():
  r=int(rr);f=10 if r==67 else 12;assert sorted(map(int,hmap))==D[r]
  for val,fs in hmap.items():
   h=int(val);sig=C.sigma(r,h);assert len(fs)==len(set(fs)) and all(prime(y) and sig%y==0 and y not in [7,r,J.t,19] for y in fs)
   ok,fail=(O.go if f==10 else J.go)(h,fs);assert ok,(r,h,fail)
  print('PASS 7^438 t^',f,'R',r,'exact powers',D[r],flush=True)
 assert used==set(data['ecpp'])
if __name__=='__main__':main()

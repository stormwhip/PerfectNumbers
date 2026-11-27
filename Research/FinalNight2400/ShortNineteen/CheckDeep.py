"""All-Euler forest or strict mixed-price/ordinary dichotomy. Exact scope only."""
import sys,json,gzip
from pathlib import Path
from math import prod,gcd
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from ExactTwo import Q,R,C,B,Root,verify as exact_two
from Price import price

def verify_row(e,g):
 t,r=Q[e],R[e];P=[(19,e),(t,2),(r,g)] if g else [(19,e),(t,6)]
 fs=H/(f'Strong{e}x2x{g}.json' if g else f'Rich{e}x6.json');bk=H/(f'DeepBook{e}x{g}.json.gz' if g else f'RichPrimes{e}x6.json.gz')
 o=json.loads(fs.read_bytes());book=json.loads(gzip.decompress(bk.read_bytes()));K,O=o['roots'],o['owners'];V=set(K)|{q for q,_ in O};used=set();S=C.State(P)
 for a,(p,f) in enumerate(P):assert p==19 or any(C.sigma(z,h)%p==0 for z,h in P[:a])
 hist=Root/'Night2400'/('C' if e==420 else 'C2');extra={t:'PivotECPP.json',r:'Forced8ECPP.json' if e==420 else 'Split8ECPP.json'}
 def prime(n):
  a=n
  if n>=2**64:
   if str(n) in book:used.add(str(n));chain=book[str(n)]
   else:chain=json.loads((hist/extra[n]).read_bytes())
   assert chain
   for rr in chain:assert rr[0]==a;a=C.pc.level(*rr)
  assert C.pc.prime64(a);return True
 assert all(prime(p) for p,h in P);C.validate_forest(S,K,O,128,prime);assert used==set(book) and not S.conflict
 if (e,g)==(420,4):
  v,Qc,_,_=price(P,[2,2,2]);assert v>B;M=prod(p**c for p,c,w in Qc)
  for q in V:
   if q%4==1:assert v*q>B*gcd(M,q+1)**2
  S.fixed_euler=True
 lo,_=C.Forest(S,K,O,128).lower();assert lo>B
 print('PASS',P[0][1],P[1][1],'secondary',g or 'unrestricted','floor',len(str(lo))-1,'vertices',len(V),'ECPP',len(book),flush=True)
if __name__=='__main__':
 for e in (330,420):exact_two(e)
 for e,g in [(330,1),(330,5),(420,2),(420,4),(330,0)]:verify_row(e,g)

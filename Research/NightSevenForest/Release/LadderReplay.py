"""First rule out 3|N by finite strict abundancy, then exhaust the forest with 3 forbidden. No external artifacts."""
import gzip,json,sys,math
from pathlib import Path
from fractions import Fraction
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import SplitReplay as F

def abundant(root,proof):
 p,e=root['p'],root['e'];F.check(p==11 and (p,e,3)==(proof['p'],proof['e'],proof['q']),'root/split mismatch');bad=(19,7);K=proof['cut'];F.check(type(K)==int and 1<=K<=50,'cut');A=F.sigma(p,e);legal=lambda r,k:all(F.sigma(r,k)%b for b in bad);ratio=lambda z,f:Fraction(F.sigma(z,f),z**f);tail=K+1+(K+1)%2
 while not legal(3,tail):tail+=2
 fs=[f for f in range(2,K+1,2) if legal(3,f)]+[tail];F.check([s[0] for s in proof['slabs']]==fs,'uncovered exponent');
 for f,qs in proof['slabs']:
  S=A*(F.sigma(3,f) if f!=tail else 1);F.check(len(set(qs))==len(qs),'duplicate support');W=ratio(3,f)*ratio(p,e);dis=[Fraction(1)]
  for q in qs:
   F.check(F.pc.prime64(q) and q not in (2,3,7,11,19) and S%q==0,'invalid forced prime');h=F.valuation(S,q);k=h+h%2
   while not legal(q,k):k+=2
   o=ratio(q,k);W*=o
   if q%4==1 and legal(q,1):
    j=h+(1-h)%4
    while not legal(q,j):j+=4
    dis.append(ratio(q,j)/o)
  F.check(W*min(dis)>2,'abundancy insufficient')

def replay(d):
 for cell in d['rows']:
  row=cell['forest'];abundant(row,cell['ladder']);m=min(F.proof(row,d['ecpp'],3,False).values());F.check(m>F.B,'absent forest insufficient');print(row['p'],row['e'],len(str(m))-1,flush=True)
if __name__=='__main__':
 for n in sys.argv[1:]:replay(json.loads(gzip.decompress((D/n).read_bytes())))

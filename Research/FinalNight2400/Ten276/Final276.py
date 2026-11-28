"""Replay a frozen (19,276) first-pivot packet; report explicit remaining values."""
from pathlib import Path
import sys,gzip,json
from fractions import Fraction
from math import prod
from collections import Counter
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H.parent/'TenNext'),str(H.parents[1]/'Session20261126')]
sys.path.insert(0,str(H));import AbCheck as A
from PivotCheck import C,exact_leaf,B
assert __debug__
p=19;e=276;t=1176672733;s=1109

def prime(q):A.prime(q);return True

def split(P,r):
 st=C.State(P);assert not st.conflict and prime(r) and r not in st.rows and st.D%r==0
 c=C.valuation(st.D,r);scale=st.base//r**c;f=c;res={}
 while scale*r**f<=B:
  pp=P+[(r,f)];st1=C.State(pp)
  if st.possible(r,f,c) and not st1.conflict and st1.base<=B and prod(C.sigma(a,h) for a,h in pp)<=2*st1.X:res[f]=pp
  f+=1
 return res,f

def chk_tree(P,nodes):
 used=set();ct=Counter()
 def rec(P):
  k=','.join(str(h) for p,h in P);assert k not in used;used.add(k);row=nodes[k];ty=row['kind'];ct[ty]+=1;st=C.State(P)
  if ty=='split':
   cs,tail=split(P,row['q'])
   for pp in cs.values():rec(pp)
  elif ty=='inert':
   from Inert import excluded
   assert prime(row['r']) and excluded(P,row['r'])
  elif ty=='weight':
   from CertifiedPrice import proof
   assert st.fixed_euler and 1109 in st.rows and proof(P)
  elif ty=='multi':
   raise AssertionError('unregistered proof tag')
  elif ty=='mask':
   K,O,head=row['w'];bad=row['bad'];assert len(K)==len(set(K)) and all(prime(q) and q not in st.rows and st.D%q==0 for q in K) and len(set(bad))==len(bad) and not set(bad)&(set(K)|set(st.rows));I=Fraction(prod(C.sigma(q,h) for q,h in P),st.X)
   for q in K:
    a=C.valuation(st.D,q);f=a+(a%2 if st.fixed_euler or q%4==3 else 0);I*=Fraction(C.sigma(q,f),q**f)
   for q in bad:
    assert prime(q);g=1 if q%4==1 and not st.fixed_euler else 2;assert I*Fraction(C.sigma(q,g),q**g)>2
   sm=C.State(P,absent=bad);C.validate_forest(sm,K,O,head,prime);sys.path.insert(0,str(H.parents[1]/'Night2400/A'));from MaskedForest import exact_absence_bound
   assert min(C.Forest(sm,K,O,head).lower()[0],exact_absence_bound(P,K,O,head,sm.bad,B))>B
  elif ty=='forest':
   K,O,head=row['w'];C.validate_forest(st,K,O,head,prime);assert min(C.Forest(st,K,O,head).lower()[0],exact_leaf(P,K,O,head))>B
  else:
   F=row['F'];assert ty in ('ab','parity') and len(set(F))==len(F) and all(prime(q) and q not in st.rows and st.D%q==0 for q in F)
   h={q:C.valuation(st.D,q) for q in F};base=Fraction(st.base);fn=lambda q,f:Fraction(q**(f-h[q]));limit=B
   if ty=='ab':base=Fraction(prod(C.sigma(p,e) for p,e in P),st.X);fn=lambda q,f:Fraction(C.sigma(q,f),q**f);limit=2
   ev={q:a+a%2 for q,a in h.items()};ordmin=base*prod(fn(q,f) for q,f in ev.items());odd=[ordmin/fn(q,ev[q])*fn(q,a+(1-a)%4) for q,a in h.items() if q%4==1 and not st.fixed_euler];assert min([ordmin,*odd])>limit
 rec(P);assert used==set(nodes);return ct

def run(N):
 packet=json.loads(gzip.decompress((H/f'Cases{N}.json.gz').read_bytes()));A.book.clear();A.book.update(json.loads(gzip.decompress((H/f'Book{N}.json.gz').read_bytes())));A.prime.cache_clear();assert prime(19) and prime(t) and prime(s) and C.sigma(19,276)%(s*t)==0
 dom,tail=split([(19,276)],t);assert len(dom)==70 and tail==188
 ct=Counter();last=A.readfile
 try:
  for f,z in sorted(packet.items(),key=lambda kv:int(kv[0])):
   m=int(f);P=dom[m];assert m in dom
   if z[0]=='hybrid':ct.update(chk_tree(P,z[1]))
   else:
    assert z[0]=='abtree';A.paths=[P];A.readfile=lambda _,v=z[1]:v;prev=A.stats.copy();A.verify(0);ct.update(A.stats-prev)
   print('PASS 19^276 first',m,z[0],flush=True)
 finally:A.readfile=last
 assert len(packet)==N;remaining=sorted(set(dom)-set(map(int,packet)));print('TOTAL',N,'of',len(dom),'raw tail',tail,'stats',ct,'ECPP',len(A.used),'remaining',remaining,flush=True)
if __name__=='__main__':run(int(sys.argv[1]))
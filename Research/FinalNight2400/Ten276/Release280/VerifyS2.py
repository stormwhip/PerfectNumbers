"""Complete first s^2 under (19,280): reconstruct T², T⁶, plus VerifyT280 union."""
from pathlib import Path
import sys,gzip,json
from math import prod,gcd
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from VerifyT280 import v,old,compact,split,exact,C,B,run as partial
from Paths280 import paths,pre,t,y,k,s,Tdomain
assert __debug__
def prime(q):v.prime(q);return True

def compactP(P,name):
 K,O,h=json.loads((H/(name+'.json')).read_bytes());state=C.State(P);assert not state.conflict and all(prime(p) for p,e in P)
 for j,(p,e) in enumerate(P):
  if j:
   L,*_=split(P[:j],p);assert L[str(e)]==P[:j+1]
 C.validate_forest(state,K,O,h,prime);lb=C.Forest(state,K,O,h).lower()[0];lb2=exact(P,K,O,h);assert min(lb,lb2)>B
 return len(str(min(lb,lb2)))-1

def two():
 a=75917843017803377803429109449;K,_,_,tail=split(paths[19],a);ls=[]
 for key,P in K.items():
  if key=='1':
   assert a%4==1 and prime(a);st=C.State(P);assert st.fixed_euler and all(st.D%r==0 and prime(r) for r in (3,5,7))
   # Already 3²,5²,7² and the original 19 power are abundant.
   X0=19**280*(3*5*7)**2;S0=v.sig(19,280)*prod(v.sig(r,2) for r in (3,5,7));assert S0>2*X0
  else:ls.append(compactP(P,'GrowT2a'+key))
 print('PASS entire T^2',len(K),'a vals incl a^1 abundant, tail',tail,'min forest',min(ls),flush=True)

def six():
 data,_,_,sha,top=old['reader']('Paths2.json.gz');assert sha=='2e8230b7e7c98f4ee89ab29389fcda7db8aa4ca81ceb383082ec630ffa57dd6c';v.book.update(data['ecpp']);v.prime.cache_clear();hist={tuple(map(tuple,rec['parts'])):rec['tree'] for rec in data['paths'].values()};ids={tuple(paths[i]):i for i in [4,5,6,7,8,9,10,11]};counts={}
 def close(P):
  for r,h in P:prime(r)
  i=ids.get(tuple(P));ty=''
  if i is not None:v.verify(i);ty='new_exact_tree'
  elif tuple(P) in hist:old['forest'](P,hist[tuple(P)],prime);ty='old_forest'
  else:
   if P[-1][0]==y:name='GrowSub6x'+str(P[-1][1])
   else:assert P[-1][0]==k;name='GrowK'+str(P[-1][1])
   compactP(P,name);ty='new_compact'
  counts[ty]=counts.get(ty,0)+1
 K,_,_,ytail=split(pre+[(t,6)],y)
 for e,P in K.items():
  if e=='12':
   Kk,_,_,ktail=split(P,k)
   for Q in Kk.values():close(Q)
  else:close(P)
 print('PASS entire T^6',len(K),'y vals, tails',ytail,ktail,'leaves',counts,flush=True)
if __name__=='__main__':
 if sys.argv[1:]==['--last-two']:two();six()
 else:
  assert not sys.argv[1:];partial();two();six()
  print('PASS COMPLETE (19,280) first s^2. Other first s^16,18 not proved by this entry.')

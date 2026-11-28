"""Combine only identical-prefix price certificates; terminal nulls remain explicitly open."""
import sys,gzip,json
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Full as W;C=W.C

def make():
 read=lambda name:json.loads((H/name).read_bytes());o=json.loads(gzip.decompress((H/'DeepPrimary2.json.gz').read_bytes()));t=o['branch'];book=o['ecpp'];opts={};used=set()
 for fn,typ in [('FilteredDeepPrimary2.json','fastpair'),('SqrFirst2.json','sqratom')]:
  if (H/fn).exists():
   for row in read(fn):
    P=tuple(map(tuple,row[0]));params=row[1:-1]
    if row[-1] and (P not in opts or typ=='fastpair'):opts[P]=dict(type=typ,args=params)
 def go(n,P):
  if P in opts:return opts[P]
  if not n:return None
  if n['type']=='split':
   q=n['q'];used.add(q);return dict(type='split',q=q,cases={k:go(v,P+((q,int(k)),)) for k,v in n['cases'].items()})
  used.update(n['roots']);used.update(z for z,q in n['owners']);return n
 t=go(t,((3,6),(1093,2)));book={str(z):book[str(z)] for z in sorted(used) if z>=2**64};(H/'PartialTwo.json.gz').write_bytes(gzip.compress(json.dumps(dict(tree=t,ecpp=book),separators=(',',':')).encode(),mtime=0))

def run():
 file=sys.argv[1] if len(sys.argv)>1 else 'PartialTwo.json.gz';assert file in ('PartialTwo.json.gz','SecondaryTwo.json.gz','DeltaTwo.json.gz','LateTwo.json.gz');d=json.loads(gzip.decompress((H/file).read_bytes()));book=d['ecpp'];seen=set();stats=Counter();gaps=[];outer=[];floors=[];assert __debug__ and C.sigma(3,6)==1093 and C.pc.prime64(1093)
 def prime(z):
  assert type(z)is int and z>=3;t=z
  if t>=2**64:
   seen.add(str(z))
   for a in book[str(z)]:assert a[0]==t;t=C.pc.level(*a)
  assert C.pc.prime64(t);return True
 def go(P,n):
  s=C.State(P);assert W.viable(s)
  if n is None:gaps.append(P);return False
  typ=n['type'];stats[typ]+=1
  if typ=='triple2':
   from FastPair import J
   assert len(P)==5 and P[:2]==[(3,6),(1093,2)] and J.excludes(P,(19,7,11,31,13),[2,3,4])==(n['count'],n['bins']);return True
  if typ=='fastpair':
   from FastPair import prove
   q,r,a,b=n['args'];assert q!=r and q in s.rows and r in s.rows and prove(P,q,r,a,b);return True
  if typ=='sqratom':
   from SquareMixedRows import trial
   q,r,w,v=n['args'];assert q!=r and q in s.rows and r in s.rows and not s.fixed_euler and trial(P,q,r,w,v);return True
  if typ=='forest':
   k,o,h=n['roots'],n['owners'],n['head'];C.validate_forest(s,k,o,h,prime);a=min(W.PC.exact_leaf(P,k,o,h),C.Forest(s,k,o,h).lower()[0]);assert a>W.B;floors.append(W.PC.floor10(a));return True
  assert typ=='split';q=n['q'];assert prime(q) and q not in s.rows and q not in s.bad and s.D%q==0;v=C.valuation(s.D,q);h=v;live=set();ok=True
  while s.base//q**v*q**h<=W.B:
   if s.possible(q,h,v):
    T=P+[(q,h)]
    if W.viable(C.State(T)):
     live.add(str(h));z=go(T,n['cases'][str(h)]);ok=ok and z
     if len(P)==2 and z:outer.append(h)
   h+=1
  assert live==set(n['cases']);return ok
 go([(3,6),(1093,2)],d['tree']);assert seen==set(book);print('PASS exact first2',len(outer),'of',len(d['tree']['cases']),'full secondary gaps',sorted({P[2][1] for P in gaps}),'null terminals',len(gaps),'stats',dict(stats),'ECPP',len(seen),'minfloor',min(floors),flush=True)
if __name__=='__main__':
 if sys.argv[1:]==['--make']:make()
 else:run()

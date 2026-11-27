"""Seal all presently closed f1 secondary values as a single exhaustive class, no duplicated intervals."""
from pathlib import Path
from functools import cache
from math import prod
from collections import Counter
import json,gzip,sys,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Full as W;from ScarceOpt import exceptions;from RootNets import more;from FastPair import prove as pair
C=W.C

def load(n):return json.loads(gzip.decompress((H/n).read_bytes()))
def dump(n,d):(H/n).write_bytes(gzip.compress(json.dumps(d,separators=(',',':')).encode(),mtime=0))
def domain_for_aug(k,q):
 P=[(3,6),(1093,1),(547,k)];s=C.State(P);v=C.valuation(s.D,q);h=v
 while s.base//q**v*q**h<=W.B:
  if s.possible(q,h,v) and W.viable(C.State(P+[(q,h)])):yield h
  h+=1

def make(out):
 low=load('LowOne.json.gz');one=load('D11.json.gz');oldnet=load('RootNet1.json.gz');D={};book={};used=set();selected={}
 def put(k,n,lam,bookup):
  k=str(k)
  if k in D or n is None:return
  def fix(node,P):
   if node is None:
    for p in [H/f'POne{k}.json',H/f'PAugDeep{k}.json']:
     if p.exists():
      for pp,q,r,a,b,ok in json.loads(p.read_bytes()):
       if ok and list(map(tuple,pp))==P:return {'pair':[q,r,a,b]}
    if k=='4':
     weighted=json.loads((H/'WeightLow4.json').read_bytes())
     for pp,q,r,a,b,w,v,ok in weighted:
      if ok and list(map(tuple,pp))==P:return {'weighted':[q,r,a,b,w,v]}
     if P[-1]==(32896733372595790517,4) and len(P)==10:return {'triple':[3,5,7]}
    return None
   if 'net' in node:return {'net':node['net'],'lam':node.get('lam',lam)}
   if node.get('type')=='split':
    q=node['q'];cs={h:fix(v,P+[(q,int(h))]) for h,v in node['cases'].items()};return None if any(v is None for v in cs.values()) else dict(type='split',q=q,cases=cs)
   return node
  u=fix(n,[(3,6),(1093,1),(547,int(k))]);
  if u is not None:D[k]=u;book.update(bookup)
 for k,n in oldnet['cases'].items():put(k,dict(net=n),1,oldnet['ecpp'])
 for k,n in low['cases'].items():put(k,n,1,low['ecpp'])
 for k,n in one['tree']['cases'].items():
  if int(k)<294:put(k,n,1,one['ecpp'])
 for path in sorted(H.glob('AugOne*.json.gz')):
  k=int(path.stem.split('.')[0][6:]); n=load(path.name);v=n['tree'];
  if v and (v.get('type')!='split' or len(v['cases'])==len(list(domain_for_aug(k,v['q'])))):put(k,v,1,n['ecpp'])
 for path in sorted(H.glob('AugDeep*.json.gz')):
  k=int(path.stem.split('.')[0][7:]); n=load(path.name);put(k,n['branch'],1,n['ecpp'])
 for lam in (1000,10000):
  grown=load(f'GrownNets{lam}.json.gz')
  for k,n in grown['cases'].items():put(k,n,lam,grown['ecpp'])
 for pt in sorted(H.glob('Deep*.json.gz')):
  label=pt.name.split('.')[0]
  if label.startswith('DeepOrd'):k=int(label[7:]);lam=1000 if k in (2,4,8,24,26,80) else 10000
  elif label.startswith('DeepNet'):k=int(label[7:]);lam=1000 if k in (166,150,138) else 10000
  else:continue
  d=load(pt.name);put(k,d['tree'],lam,d['ecpp'])
 m=H/'MergedLow2.json.gz'
 if m.exists():
  x=load(m.name);put(2,x['branch'],1,x['ecpp'])
 def walk(n):
  if 'net' in n:used.update(n['net']);return
  if 'pair' in n or 'triple' in n or 'weighted' in n:return
  if n['type']=='forest':used.update(n['roots']);used.update(z for z,p in n['owners']);return
  used.add(n['q']);[walk(v) for v in n['cases'].values()]
 [walk(n) for n in D.values()];dump(out,dict(cases=D,ecpp={str(p):book[str(p)] for p in sorted(used) if p>=2**64}));print('sealed',sorted(map(int,D)),flush=True)

def run(file):
 assert __debug__ and C.sigma(3,6)==1093 and C.sigma(1093,1)==1094;ps=(3,1093,547);bookdata=load(file);book=bookdata['ecpp'];seen=set();stats=Counter();floors=[];complete=set();unresolved=[]
 @cache
 def prime(p):
  assert type(p)is int and p>=3;t=p
  if t>=2**64:
   seen.add(str(p))
   for row in book[str(p)]:assert row[0]==t;t=C.pc.level(*row)
  assert C.pc.prime64(t);return True
 for p in ps:prime(p)
 @cache
 def EE(lam):assert lam in (1,1000,10000);return exceptions(292,lam)
 def walk(P,n):
  s=C.State(P);assert W.viable(s)
  if 'net' in n:
   rr=n['net'];lm=n['lam'];assert len(rr)==len(set(rr)) and all(prime(z) and z not in s.rows and s.D%z==0 for z in rr);V=more(P,rr,lm,EE(lm));assert V>W.B;stats['net']+=1;floors.append(W.PC.floor10(V.numerator//V.denominator));return
  if 'triple' in n:
   from FastPair import J; ii=n['triple'];assert len(ii)==3 and J.excludes(P,(19,7,11,31,13),ii)==(21,[0,0,0]);stats['triple']+=1;return
  if 'weighted' in n:
   from FixedWeighted import prove as WP
   q,r,a,b,w,v=n['weighted'];assert q!=r and q in s.rows and r in s.rows and 2<=w<=8 and 2<=v<=8 and WP(P,q,r,a,b,w,v);stats['weighted']+=1;return
  if 'pair' in n:
   q,r,a,b=n['pair'];assert q!=r and q in s.rows and r in s.rows and pair(P,q,r,a,b);stats['pair']+=1;return
  if n['type']=='forest':
   k,o,h=n['roots'],n['owners'],n['head'];C.validate_forest(s,k,o,h,prime);v=min(W.PC.exact_leaf(P,k,o,h),C.Forest(s,k,o,h).lower()[0]);assert v>W.B;stats['forest']+=1;floors.append(W.PC.floor10(v));return
  assert n['type']=='split';q=n['q'];ks=set();assert prime(q) and q not in s.rows and q not in s.bad and s.D%q==0;v=C.valuation(s.D,q);h=v;stats['split']+=1
  while s.base//q**v*q**h<=W.B:
   if s.possible(q,h,v):
    T=P+[(q,h)];u=C.State(T)
    if W.viable(u):ks.add(str(h));walk(T,n['cases'][str(h)])
   h+=1
  assert ks==set(n['cases'])
 X0=3**6*1093;s=C.State([(3,6),(1093,1)]);h=2
 from Six import exc
 U=prod(exc().values(),start=1)
 while X0*547**h<=W.B:
  P=[(3,6),(1093,1),(547,h)];u=C.State(P)
  if s.possible(547,h,1) and W.viable(u):
   if X0*547**h*547**(2*(h-1))>W.B*U:stats['uniform']+=1
   elif str(h) in bookdata['cases']:walk(P,bookdata['cases'][str(h)]);complete.add(str(h))
   else:unresolved.append(h)
  h+=2
 assert complete==set(bookdata['cases']) and stats['uniform']==52 and len(complete)+52+len(unresolved)==160 and seen==set(book)
 if file=='OneComplete.json.gz':assert not unresolved and len(complete)==108 and hashlib.sha256((H/file).read_bytes()).hexdigest()=='29c7fdf6f1e22320e22c0df4e55fd19c0dc9095e12316996a16ca8ed2b28db1d'
 print('PASS f1 union',len(complete)+52,'of 160 | gaps',unresolved,'|',dict(stats),'ECPP',len(seen),'minfloor',min(floors),flush=True)
if __name__=='__main__':
 if sys.argv[1:2]==['--make']:make(sys.argv[2]);
 else:run(sys.argv[1])

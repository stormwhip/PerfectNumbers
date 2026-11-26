"""Conditional forest: every odd sigma residual outside the reserved prime set is exact and charged once; at most one Euler coupon. See Report.md. Verification: standalone integer arithmetic; nomination needs historical local discovery forests only."""
from pathlib import Path
import sys,math,gzip,json,hashlib,os,time,itertools
from functools import cache,lru_cache
H=Path(__file__).resolve().parent;repo=Path(os.environ.get('OPN_REPO',H.parents[2])).resolve();R=repo/'Research';sys.path.insert(0,str(R/'RootFiveNext'));import PrimeCheck as pc
O=(19,7,11,31,13,3,5,17);B=10**2400;front=json.load(open(R/'Session20261126/OpenSupport.json'));assert front['order']==list(O)
@lru_cache(40000)
def sigma(p,f):return (p**(f+1)-1)//(p-1)
def val(t,q):
 a=0
 while t%q==0:t//=q;a+=1
 return a
@cache
def cert(q):
 if q<2**64:return [] if pc.prime64(q) else None
 f=lib/'certs'/(hashlib.sha256(str(q).encode()).hexdigest()[:24]+'.json');
 if not f.is_file():return None
 try:
  rr=json.loads(f.read_bytes());n=q
  for r in rr:
   if r[0]!=n:return None
   n=pc.level(*r)
  if pc.prime64(n):return rr
 except (ValueError,TypeError,AssertionError,IndexError):pass
 return None

def tree(t,ban,need):
 p=t['p'];e=t['e'];a=sigma(p,e);rs=(set(t['roots'])|set(need))-{p};assert all(a%q==0 or q in need for q in rs);ow=dict(t['owners']);V=rs|ow.keys();kids={q:[] for q in V};seen=set();todo=list(rs)
 for q,z in ow.items():
  if z in V and q not in rs and q not in ban and q!=p and a%q:kids[z].append(q)
 while todo:
  q=todo.pop();assert q not in seen;seen.add(q);todo.extend(kids[q]);
 assert not(rs&set(ban)) and all(a%q for q in ban)
 return rs,{q:z for q,z in ow.items() if q in seen-rs}

def factory(t,need,mode='int'):
 p,e=t['p'],t['e'];assert p in O and e>=2 and e%2==0;a=sigma(p,e);rs,ow=tree(t,[],need);nodes=rs|set(ow);kids={q:[] for q in nodes};
 for q,z in ow.items():kids[z].append(q)
 U=p*a*math.prod(ow)*math.prod(need);cap=t['head'];assert type(cap)==int and 1<=cap<=1024
 heights={q:max(1,val(a,q)) for q in rs};base=p**e*(a//math.prod(q**val(a,q) for q in rs));
 # Reuse sigma residuals between masks sharing this required support.
 @cache
 def offers(q,f):
  v=sigma(q,f)//(1+f%2);u=v
  while (g:=math.gcd(u,U))!=1:u//=g
  return u,[(z,val(v,z)) for z in kids[q] if v%z==0]
 @cache
 def block(q,h,ban):
  bad=set(ban);children=kids[q];spok=q%4==1 and all((q+1)%b for b in bad);least=flex=B+1
  if q in bad:return B+1,B+1
  for sp in (0,1) if spok else (0,):
   f=h+((1-h)%4 if sp else h%2);step=4 if sp else 2;tested=0
   while tested<cap and q**f<(flex if sp else least):
    if all((f+1)%b if q%b==1 else pow(q,f+1,b)!=1 for b in bad):
     tested+=1;u,sub=offers(q,f);cost=q**f*u;alts=[]
     for z,k in sub:
      n,c=block(z,k,ban);cost*=n;alts.append((n,c))
     if not sp:least=min(least,cost);cost=min([cost]+[cost//n*c for n,c in alts]);
     flex=min(flex,cost)
    f+=step
   if not sp:least=min(least,q**f)
   flex=min(flex,q**f)
  return least,flex
 def eval(ban):
  if any(a%b==0 for b in ban) or any(q in ban for q in rs):return B+1
  sub=[block(q,k,tuple(sorted(ban))) for q,k in heights.items()];v=base*math.prod(n for n,c in sub);out=min([v]+[v//n*c for n,c in sub]);block.cache_clear();return out
 return eval

def clean(t):
 p,e=t['p'],t['e'];rs=[q for q in t['roots'] if cert(q) is not None];ow={q:z for q,z in t['owners'] if cert(q) is not None};nodes=set(rs)|ow.keys();ow={q:z for q,z in ow.items() if z in nodes};rr=dict(p=p,e=e,roots=rs,owners=sorted(ow.items()),head=t['head']);_,aa=tree(rr,[],[]);rr['owners']=sorted(aa.items());return rr

def discover():
 dest=H/'Forest';dest.mkdir(exist_ok=True);dirs='pruned restart augment smooth refined deep rows'.split();items=[]
 for k,mi in front['rows'].items():
  p,e=map(int,k.split(':'));candidates=[]
  for d in dirs:
   f=lib/d/f'{p}x{e}.json'
   if f.exists():
    t=json.load(open(f));candidates.append((t.get('score',0),str(f),t))
  if candidates:items.append((max(candidates,key=lambda a:a[0]),p,e,mi))
 for (score,fn,t),p,e,ms in sorted(items,key=lambda a:-a[0][0]):
  destf=dest/f'{p}x{e}.json.gz'
  if destf.exists():continue
  start=time.time();t=clean(t);t['head']=min(t['head'],64);known={};cols={};reg=set(O[:O.index(p)]);eset={};
  for mask in sorted(ms,key=int.bit_count):
   have={q for j,q in enumerate(O) if mask>>j&1};ban=set(O)-have
   # Presence of 23 and 29 already certified for 3,5,19 absent. Optional conservative generic mode uses deductions only for those exact masks.
   forced=(have|{23,29}) if not (have&{3,5,19}) else have
   nf=tuple(sorted(forced-{p}));ev=cols.get(nf)
   if ev is None:ev=cols[nf]=factory(t,nf)
   x=ev(ban)
   if x>B:known[mask]=x.bit_length()
  if known:
   keys=set(t['roots'])|set(dict(t['owners']));out=dict(row=t,closed=known,ecpp={str(q):cert(q) for q in keys if q>=2**64});destf.write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),compresslevel=5));print('FOUND',p,e,len(known),known,flush=True)
  print('SCAN',p,e,round(score),len(known),round(time.time()-start,1),flush=True);sigma.cache_clear()

def verify(f):
 t=json.load(gzip.open(f));r=t['row'];p,e=r['p'],r['e'];valid=front['rows'][f'{p}:{e}'];seen=set()
 for q in set(r['roots'])|set(dict(r['owners'])):
  assert q>2 and type(q)==int;n=q
  if q>=2**64:
   for step in t['ecpp'][str(q)]:assert n==step[0];n=pc.level(*step)
  assert pc.prime64(n)
 for sm,bits in t['closed'].items():
  m=int(sm);assert m in valid;have={q for j,q in enumerate(O) if m>>j&1};assert p in have and not set(O[:O.index(p)])&have;ban=set(O)-have;need=(have|{23,29}) if not(have&{3,5,19}) else have;x=factory(r,tuple(sorted(need-{p})))(ban);assert x>B and x.bit_length()==bits;seen.add((p,e,m))
 print('VERIFIED',f.name,len(seen),flush=True);sigma.cache_clear();return seen
if __name__=='__main__':
 assert __debug__
 if sys.argv[1]=='discover':
  if len(sys.argv)!=3:raise SystemExit('usage: ForestMasks.py discover DISCOVERY_INPUT_DIR')
  lib=Path(sys.argv[2]).resolve(strict=True);discover()
 else:
  hits=set();fs=map(Path,sys.argv[2:]) if len(sys.argv)>2 else sorted((H/'Forest').glob('*.gz'))
  for f in fs:hits.update(verify(f))
  print('VERIFIED triples',len(hits));(H/'ForestKeys.json').write_text(json.dumps(sorted(hits)))

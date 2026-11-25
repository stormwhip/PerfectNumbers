"""Offline strict replayer on baseline 3b50576. Only certificate rows, not discovery/caches, are read. Exit nonzero on unproved rows."""
import argparse,json,gzip,hashlib,sys,time,math
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;R=H.parent
sys.path.insert(0,str(R/'EveningTree'));import IndependentTree as I
# Do not import the discovery tree, oracle, or its arithmetic helpers.
@cache
def prime(n):
 if n<2**64:return I.ec.prime64(n)
 q=n;fn=H/'ECPP'/(hashlib.sha256(str(n).encode()).hexdigest()[:24]+'.json.gz');c=json.loads(gzip.decompress(fn.read_bytes()))
 for row in c:
  if q!=row[0]:raise ValueError('bad ECPP subject')
  q=I.ec.level(*row)
 if not I.ec.prime64(q):return False
 return True
class Check(I.Proof):
 def __init__(self,row):
  super().__init__(row['p'],row['e'],row['fs'],False,True);self.depth=row['depth'];self.pending=set(row['fs']);self.origins={}
 def visit(self,parts,X,S,ban):
  # fs is a trial bank, not a root-factor claim. Record the first actual sigma power furnishing a compulsory divisor of D at a visited node.
  D=math.lcm(X,S//math.gcd(S,2))//X
  for z in tuple(self.pending):
   if D%z:continue
   a,f=next((a,f) for a,f in parts if I.sigma(a,f)%z==0);self.origins[str(z)]=[a,f];self.pending.remove(z)
  if len(parts)>7:
   # Extend the independent replay only by rebuilding a fresh mandatory-power range.
   return last(self,parts,X,S,ban)
  if len(parts)==7 and self.depth>=7:return last(self,parts,X,S,ban)
  return super().visit(parts,X,S,ban)
def last(t,parts,X,S,ban):
 t.stats['nodes']+=1
 if t.stats['nodes']>25000:return False
 U=math.lcm(X,S//math.gcd(S,2))//X
 if math.gcd(U,X*math.prod(ban)*2)>1 or X*U>I.B or S>2*X:return True
 used=any(f%2 for _,f in parts);blocks={}
 for z in t.pr:
  c=I.vp(U,z)
  if not c:continue
  U//=z**c;ds=I.forbidden_indices(z,ban);m=I.least(z,c,ds,False);a=None if used else I.least(z,c,ds,True);blocks[z]=c,m,a,ds
 base=X*U*math.prod(z**m for z,(_,m,_,_) in blocks.items());saves={z:z**max(0,m-a) for z,(_,m,a,_) in blocks.items() if a is not None}
 if base>I.B*max([1,*saves.values()]) or t.valuation_close(X,S,U,base,blocks,used):return True
 if len(parts)>t.depth or not blocks:return False
 z=max(blocks);c,m,a,ds=blocks[z];D=base//z**m;other=max([1,*[x for k,x in saves.items() if k!=z]])
 for f in range(c,10000):
  w=z**f
  if w*D>I.B*other:return True
  if f%2 and (used or z%4!=1 or f%4!=1 or w*D>I.B):continue
  if I.permissible(f,ds) and not t.visit(parts+((z,f),),X*w,S*I.sigma(z,f),ban):return False
 return False

def verify(row,sources=None):
 if not __debug__:raise RuntimeError('optimized Python not supported')
 if type(row['p'])!=int or type(row['e'])!=int or row['e']<2 or row['e']%2:raise ValueError('invalid exponent')
 if row['p'] not in (7,11,13,19,31) or (row['p'],row['e'])==(11,306):raise ValueError('wrong scope')
 if not all(type(z)==int and z>2 and prime(z) for z in row['fs']):raise ValueError('unproved factor')
 t=Check(row)
 if not t.prove():raise ValueError(('unclosed tree',row['p'],row['e'],t.stats))
 if sources is not None:sources.append(dict(p=row['p'],e=row['e'],origins=t.origins,unused=sorted(t.pending)))
 return dict(t.stats)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',default='Accepted.json');ap.add_argument('--sources');args=ap.parse_args();sources=[];rows=json.loads((H/args.input).read_text());openpairs={(s['root'],e) for s in json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards'] for e in s['remaining_actuals']};seen=set();start=time.monotonic()
 for row in rows:
  k=(row['p'],row['e']);assert k in openpairs and k not in seen;seen.add(k);t=time.monotonic();stats=verify(row,sources);print(*k,stats,round(time.monotonic()-t,3),flush=True)
 if args.sources:(H/args.sources).write_text(json.dumps(sources,separators=(',',':'))+'\n')
 print('verified',len(seen),'wall_seconds',round(time.monotonic()-start,3))
if __name__=='__main__':main()

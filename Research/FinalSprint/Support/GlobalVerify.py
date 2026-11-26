"""Standalone global hitting-set replay. Python -I -S -B GlobalVerify.py --repo REPO. No installation, solver, frontier, historical nominator or model cache. All case assumptions are regenerated from the claimed hitting set."""
from pathlib import Path
import sys,gzip,json,argparse,gc
from math import inf
assert __debug__;H=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=H.parents[2]);ap.add_argument('--only',nargs='+',default=[]);a=ap.parse_args();R=a.repo.resolve()/'Research';sys.path.insert(0,str(R/'MiddayTerminal'));import Audit,Common
assert Path(Audit.__file__).resolve()==R/'MiddayTerminal/Audit.py';base=json.load(gzip.open(R/'MiddayTerminal/PackNewTriple3513.json.gz'));Common.dataset=lambda:{'ecpp':base['ecpp'],'rows':{}}

def premises(bad,need):
 # Imported six previously proved hitting sets explicitly asserted; completely separate from any finite frontier.
 hits=[{3,5,q} for q in [7,11,13]]+[{3,5,19,q} for q in [17,23,29]];P=sorted(set.union(set(bad),set(need),*hits))
 for m in range(1<<len(P)):
  s={q for i,q in enumerate(P) if m>>i&1}
  if not s.intersection(bad) and all(s&h for h in hits):assert set(need)<=s

def make(bad,need,L,cut,ext,w):return dict(root=0,e=0,extra=sorted(bad),x=[],lower=[[p,1] for p in sorted(need)],L=L,T=3*L,cut=cut,cap=cut,wide=True,extend=sorted(ext.items()),parity=True,weights=w)
def direct(f,bad,need,fl):
 d=json.loads(f.read_bytes());cfg=d['cfg'];assert cfg[0]==bad and cfg[1]==need and d['floor']==fl;premises(bad,need);_,_,L,E,r,depth,cut,_=cfg;ext={q:c for q,c in base['args']['extend'] if q not in bad};ext[r]=max(E,ext.get(r,0));
 for q in set(need)|{7,11,13,17,19,23,29,31}:
  if q not in bad:ext[q]=max(ext.get(q,0),depth)
 u=Audit.replay(**make(bad,need,L,cut,ext,d['w']))[0];den=Audit.W*Audit.logs(10)[1];assert u>2400*den and u//den==fl;print('GLOBAL PASS',bad,'floor',fl,flush=True)

def filter47():
 row=json.loads((H/'Side1931.json').read_bytes());bad,need,L,cut,add,w,old=row;assert bad==[3,5,19,31] and need==[7,11,13,17];required=sorted([*need,23,29]);forbid=sorted([*bad,47]);premises(forbid,required);ext={q:c for q,c in base['args']['extend'] if q not in bad};ext.update({q:max(c,ext.get(q,0)) for q,c in add});_,V,pr=Common.init(0,0,bad,True);ps=sorted((set(Audit.primes(L))|V|set(pr)|set(ext)|set(need))-set(bad));stop=2+len(ps)+len(need);w=[(i,a) for i,a in w if i<2 or i>=stop];u,r,G,_=Audit.replay(**make(bad,need,L,cut,ext,w));assert list(G)==ps;den=Audit.W*Audit.logs(10)[1];disc=0
 # Refund original groupwise minima (including absence). Re-minimize with presence constraints, q!=47, legal parity, extra sigma obstruction only for exact columns; tail Euler columns may only be discarded if 47 | q+1.
 for q,g in G.items():
  oldmin=min([0]+[r[i] for i,e,x in g]);evens=[] if q in required else [0];odd=[]
  for i,e,x in g:
   if q==47:continue
   if x and Audit.geom(q,e)%47==0:continue
   if not x and e%2 and (q+1)%47==0:continue
   (odd if e%2 else evens).append(r[i])
  assert evens;v=min(evens);u+=v-oldmin
  if odd:disc=min(disc,min(odd)-v)
 u+=disc
 assert u>2400*den and u//den==2432;print('GLOBAL PASS',forbid,'floor',u//den,flush=True)

cases=[('3x5x19x31x37',[3,5,19,31,37],[7,11,13,17,23,29],2453),('3x5x17x23x29',[3,5,17,23,29],[7,11,13,19],2574)]
extra=H/'AdditionalGlobal.json'
if extra.is_file():cases+=json.load(open(extra))
for tag,bad,need,fl in cases:
 if not a.only or tag in a.only:direct(H/('Hit'+tag+'.json'),bad,need,fl);Audit.split.cache_clear();Audit.geom.cache_clear();Audit.primeproduct.cache_clear();Audit.chunks.cache_clear();Audit.logs.cache_clear();gc.collect()
if not a.only or '47' in a.only:filter47()

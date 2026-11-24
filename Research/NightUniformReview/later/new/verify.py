"""Standard-library proof checker, complete exact p,e domain with intersection-cover verification."""
import sys,json,gzip,time
from pathlib import Path
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D.parents[1]));import Verify31 as V
R=V.R
if __name__=='__main__':
 if not __debug__:raise RuntimeError('disabled assertions')
 if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
 sys.setrecursionlimit(30000);p,e=map(int,sys.argv[1:3]);proofs=json.loads(gzip.decompress((D/f'cert-{p}-{e}.gz').read_bytes()));used=set();num=0;origin=R.rect;t=time.time()
 def check(C,c,z,T,lo,hi,cap):
  global num
  if not origin(C,c,z,T,lo,hi,0):return False
  k=V.key(C,c,z,T);cur=lo
  for i,(l,h,w) in enumerate(proofs.get(k,())):
   if h<cur:continue
   if l>cur:break
   if (k,i) not in used:
    assert 1<l<=h
    if w==['direct']:
     first=l+(z-l)%T;assert (h-first)//T<=12 and all(C%r**c for r in range(first,h+1,T))
    elif w==['rectangle']:assert not origin(C,c,z,T,l,h,0)
    else:assert R.LatticeLeaf.verify(C,c,z,T,l,h,w)
    used.add((k,i))
   cur=h+1
   if cur>hi:num+=1;return False
  return True
 R.rect=check;x=next(z for z in json.loads((R.D/'input.json').read_bytes()) if (z['p'],z['e'])==(p,e));r=R.run(x,0);assert not r['inside'] and not r['outside'] and sum(r['counts'].values())==e+1 and len(used)==sum(map(len,proofs.values()));print('VERIFIED',p,e,'s',e+1,'post',len(r['post_sponsor']),'boxes',num,'leaves',len(used),'seconds',round(time.time()-t,1),flush=True)

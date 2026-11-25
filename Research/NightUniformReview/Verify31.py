"""Additional full-domain exponent review; compact packets prove a union of boxes per congruence. Never trusts discovery flags or partial windows."""
import sys, json, gzip, collections, argparse,hashlib,time
from pathlib import Path
import Replay as R
D=Path(__file__).resolve().parent

def key(C,c,z,T):return hashlib.sha256(('|'.join(map(str,(C,c,z,T)))).encode()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('assertions disabled')
 ap=argparse.ArgumentParser();ap.add_argument('p',type=int);ap.add_argument('e',type=int);group=ap.add_mutually_exclusive_group(required=True);group.add_argument('--raw',type=Path);group.add_argument('--compact',type=Path);group.add_argument('--collect',type=Path);a=ap.parse_args();sys.setrecursionlimit(30000)
 if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
 x=next(z for z in json.loads((D/'Input.json').read_bytes()) if (z['p'],z['e'])==(a.p,a.e));t=time.time();boxes=collections.defaultdict(set);rec={};used=set();origin=R.rect
 if a.raw:R.pack=json.loads(gzip.decompress(a.raw.read_bytes()));assert R.pack
 else:
  if a.compact:
   rec=json.loads(gzip.decompress(a.compact.read_bytes()));assert rec
  def check(C,c,z,T,L,H,cap):
   if not origin(C,c,z,T,L,H,0):return False
   if a.collect:boxes[(C,c,z,T)].add((L,H));return False
   # Use any supplied divisor modulus of the actual progression; the proof box must cover the actual range.
   for j in range(1,1000):
    TT=T//(a.p**(j-1));zz=z%TT;g=key(C,c,zz,TT)
    if g in rec:
     for i,(lo,hi,w) in enumerate(rec[g]):
      if lo<=L and H<=hi:
       if (g,i) not in used:assert R.LatticeLeaf.verify(C,c,zz,TT,lo,hi,w);used.add((g,i))
       return False
    if TT%a.p:break
   return True
  R.rect=check
 r=R.run(x,0);assert not r['outside'] and not r['inside'] and sum(r['counts'].values())==a.e+1
 if a.collect:
  a.collect.write_bytes(gzip.compress(json.dumps([[*k,sorted(v)] for k,v in boxes.items()],separators=(',',':')).encode()));print('NOT CERTIFIED: generated candidate boxes',len(boxes),sum(map(len,boxes.values())))
 else:
  assert (R.checked==set(R.pack)) if a.raw else (len(used)==sum(map(len,rec.values())));print('VERIFIED',a.p,a.e,'levels',a.e+1,'post',len(r['post_sponsor']),'leaves',len(used) or len(R.checked),'seconds',round(time.time()-t,2),flush=True)
if __name__=='__main__':main()

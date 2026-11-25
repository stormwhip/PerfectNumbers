"""Additional five-prime sets with 13 allowed; prior dependency ReleaseFour.
No asserted primality or original canonical root assumptions. No ledger credit.
"""
from pathlib import Path
import sys,subprocess,gzip,json,hashlib,itertools
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Audit import replay,W,logs,split,chunks,primeproduct
import Common

def main():
 if not __debug__:raise SystemExit('Do not run with -O')
 args=sys.argv[1:];assert args in ([],['--baseline'],['--only-new'])
 if args!=['--only-new']:subprocess.run([sys.executable,'-I','-S','-B',str(H/'ReleaseFour.py'),*args],check=True)
 def forbidden():raise ValueError('research inputs forbidden')
 Common.dataset=forbidden;sets=[]
 for fn,no,k in [('NewNo13.json.gz',[17,19],2407),('NewNo13b.json.gz',[17,23],2466),('NewNo13c.json.gz',[19,23],2426)]:
  raw=(H/fn).read_bytes();d=json.loads(gzip.decompress(raw));assert (d['root'],d['e'],d['extra'],d['x'],d['lower'])==(0,0,[3,5,11]+no,[],[[7,1],[13,1]]);u,*_=replay(**d);unit=W*logs(10)[1];assert u>2400*unit and u//unit==k;print(fn,hashlib.sha256(raw).hexdigest(),k,flush=True);sets.append(set(no));split.cache_clear();primeproduct.cache_clear();chunks.cache_clear()
 for b in itertools.product([0,1],repeat=3):
  active={p for p,yes in zip([17,19,23],b) if yes}
  if all(c&active for c in sets):assert len(active)>=2
 print('Absent 3,5,11 implies 7 and 13 by {3,5,7}, {3,5,11,13}; hence all three packets apply. At least two of 17,19,23 must occur. Complete exponents/shards: 0/0.',flush=True)
if __name__=='__main__':main()

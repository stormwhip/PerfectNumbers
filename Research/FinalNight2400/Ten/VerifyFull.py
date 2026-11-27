"""Full (19,58) union; default replays all dependencies. --incremental uses historical receipts."""
import sys,subprocess,json,gzip,hashlib
from pathlib import Path
assert __debug__
H=Path(__file__).resolve().parent;ROOT=H.parents[2];N=ROOT/'Research/Night2400';G=ROOT/'Research/GeminiFrontier'
assert sys.argv[1:] in ([],['--incremental'])
def run(*args):subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',*map(str,args)],cwd=ROOT,check=True)
def pin(p,h):
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h;return json.loads(gzip.decompress(b))
a=N/'Fibers19x58.json.gz';b=N/'C10/EulerF1.json.gz'
A=pin(a,'adff8cd3fa4651ab8816924b6ca5d2d747edcfcdb76382f7e1b45b4bc9f4dce8');C=pin(b,'f52b0f8b3fd0f8e869e0e38f7d6ac34cf0254a1082dce5c2ad8df3f2ca7f5c90')
assert [A['p'],A['e'],A['pivot']]==[C['p'],C['e'],C['pivot']] and [C['p'],C['e']]==[19,58]
assert sorted(map(int,A['cases']))==[2,4,5,6,8,9,10,12,13,14]
def opens(t,P):
 if t is None:yield tuple(P)
 elif t['type']=='split':
  for f,v in t['cases'].items():yield from opens(v,P+[(t['q'],int(f))])
 else:assert t['type'] in ('price','forest')
P=[(19,58),(C['pivot'],1)];T=C['tree']['q'];old=set(opens(C['tree'],P));assert len(old)==11
new6=set()
for idx in (3,4,5,6,7,8,9,10):
 name=('Weight' if idx in (3,9,10) else 'Tree')+str(idx)+'.json';path=tuple(map(tuple,json.loads((H/name).read_bytes())['path']));assert path[:3]==tuple(P+[(T,6)]) and path not in new6;new6.add(path)
new2={p for p in old if p[2]==(T,2)};assert len(new2)==2 and old==new6|new2|{tuple(P+[(T,10)])}
shard='P19_I00015';ledger=json.loads((G/'ShardToKeys.json').read_bytes());assert {k:vs for k,vs in ledger.items() if [19,58] in vs}=={shard:[[19,58]]}
if not sys.argv[1:]:
 run(N/'FrontierTree.py',a);run(N/'Receipts/FiberPartition.py',a);run(N/'C10/Verify.py')
else:print('INCREMENTAL: relying on historical (19,58) first-sibling and C10 receipts; those trees NOT replayed.',flush=True)
run(G/'VerifyT10.py','--arithmetic-only');run(H/'VerifyTwo.py');run(H/'VerifySix.py');run(H/'VerifyWeighted.py')
print('PASS full exact key (19,58); singleton P19_I00015; mode:', 'incremental' if sys.argv[1:] else 'full dependency replay',flush=True)

"""Full exact-key binder: canonical root (19,280), no historic scout claims assumed."""
import sys,subprocess,json,gzip,hashlib,runpy
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];R=ROOT/'Research';N=R/'Night2400';assert __debug__
assert sys.argv[1:] in ([],['--history-only'])
def execute(*args):subprocess.run([sys.executable,'-I','-B','-S','-X','int_max_str_digits=0',*map(str,args)],cwd=ROOT,check=True)
def raw(f):return json.loads(gzip.decompress(f.read_bytes()))
fin=N/'Fibers19x280.json.gz';raw0=raw(fin);assert (raw0['p'],raw0['e'],raw0['pivot'])==(19,280,353998162545967)
# Every node of the 25 first-fiber packet is checked by immutable stock kernel.
sys.path[:0]=[str(N),str(N/'C7')];from FrontierTree import replay
r=replay(fin);assert r['key']==[19,280] and r['pivot']==str(raw0['pivot']) and r['domain']==list(range(2,59,2)) and r['open']==[2,16,18,22] and not r['open_paths'];assert r['covered']==sorted(set(r['domain'])-{2,16,18,22})
execute(N/'Receipts/FiberPartition.py',fin);execute(N/'C13/Verify.py')
assert set(raw(N/'C13/Fiber22.json.gz')['cases'])=={'22'}
ledger=R/'GeminiFrontier';sh=json.loads((ledger/'ShardToKeys.json').read_bytes());ks=json.loads((ledger/'KeyToShards.json').read_bytes());assert {k:v for k,v in sh.items() if [19,280] in v}=={'P19_I00058':[[19,280]]} and ks['19,280']==['P19_I00058']
if not sys.argv[1:]:
 execute(H/'VerifyS2.py');execute(H/'High280.py');print('FULL exact (19,280); 25+1+3=29 first fibers; singleton P19_I00058; all dependencies replayed.',flush=True)
else:print('PASS historical union 25 firsts plus 22; NEW THREE FIBERS NOT RUN in --history-only mode.',flush=True)

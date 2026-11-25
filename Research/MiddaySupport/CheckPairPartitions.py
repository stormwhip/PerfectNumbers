"""Aggregate three old two-forbidden witness inputs and preimage digests of exact replay outputs."""
from pathlib import Path
from hashlib import sha256
import json,subprocess,sys,tempfile
H=Path(__file__).resolve().parent
M={7:('TwoAvoidSevenB.json',291,253,826),3:('TwoTail3.json',1202,1188,2394),5:('TwoTail5.json',719,701,1422)}
def read(p):return json.loads(p.read_bytes())
for q,(name,baseline,count,top) in M.items():
 fn=H.parent/'NightUniform'/name if q==7 else H/name;dest=H/('PairResults.json' if q==7 else f'PairResults{q}.json');saved=dest.read_bytes()
 with tempfile.TemporaryDirectory() as td:
  out=Path(td)/'partition.json';subprocess.run([sys.executable,'-I','-S','-B',str(H/'PairDual.py'),str(fn),'--output',str(out)],check=True);assert read(dest)==read(out),'ledger mismatch'
 a=read(fn)['cases'][0];b=read(dest)['cases'][0];assert a['p']==q and set(b['forbidden'])=={3,5,7}-{q};old=set(a['survivors']);new=set(map(int,b['new']));left=set(b['survivors']);assert len(old)==baseline and not left&new and left|new==old and len(left)==count and max(left)==top;print('exact',q,baseline,len(new),len(left),top,sha256(saved).hexdigest(),flush=True)

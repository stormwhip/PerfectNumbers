"""Audit strict threshold and Delta membership; transfer only through odd-divisor indices."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Verify import verify

def audit():
 base=H.parent/'Nov25/Delta.json';d=json.loads(base.read_bytes());shards=d['remaining_shards'];due={(s['root'],e) for s in shards for e in s['remaining_actuals']};rows=[];got=set()
 for f in sorted(H.glob('Forest*.json.gz')):
    p,e,fl,h=verify(f);assert (p,e) in due and (p,e) not in {(a['p'],a['e']) for a in rows};effects={(p,n) for pp,n in due if p==pp and (n+1)%(e+1)==0};got|=effects;rows.append(dict(p=p,e=e,packet=f.name,sha256=h,floor_log10=fl,coverage=sorted(effects)))
 closed=[s['id'] for s in shards if all((s['root'],n) in got for n in s['remaining_actuals'])];return dict(baseline_sha256=sha256(base.read_bytes()).hexdigest(),actuals=sorted(got),closed_shards=closed,packets=rows)
if __name__=='__main__':print(json.dumps(audit(),indent=2))

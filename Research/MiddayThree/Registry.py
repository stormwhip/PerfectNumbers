"""Fixed explicit root-three packet registry, no glob-as-authority. Edits are
only deduped when all shard obligations have been covered. Optional --replay
reruns *both* implementations; --check always checks byte hashes and exact
froniter membership. Uses no discovery cache or nonstandard modules."""
from pathlib import Path
from hashlib import sha256
import json,sys,gzip
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H));import Forest as F;from IndependentForest import checkfile

def entries(names):
 out=[]
 for name in names:
  p=H/name;pk=json.loads(gzip.decompress(p.read_bytes()));r=pk['row'];lo,_,_=F.measure(r,pk['ecpp']);F.check(lo>F.B,'open');test=checkfile(p);F.check(test==lo,'different integer floors');out.append(dict(e=r['e'],packet=name,sha256=sha256(p.read_bytes()).hexdigest(),floor=len(str(lo))-1,roots=len(r['roots']),edges=len(r['edges']),ecpp=len(pk['ecpp'])))
 return sorted(out,key=lambda x:x['e'])
def run(rows):
 delta=json.loads((H.parent/'Nov25/Delta.json').read_bytes());tasks=[s for s in delta['remaining_shards'] if s['root']==3];es={r['e'] for r in rows};F.check(len(es)==len(rows) and es<={j for s in tasks for j in s['remaining_actuals']},'invalid frontier');closed=[s['id'] for s in tasks if set(s['remaining_actuals'])<=es]
 for x in rows:
  p=H/x['packet'];F.check(p.parent==H and sha256(p.read_bytes()).hexdigest()==x['sha256'],'hash');d=json.loads(gzip.decompress(p.read_bytes()));F.check(d['row']['e']==x['e'],'binding')
 return dict(exact=sorted(es),closed=closed,rows=rows)
if __name__=='__main__':
 path=H/'Registry.json'
 if sys.argv[1:2]==['--make']:
  x=run(entries(sys.argv[2:]));path.write_text(json.dumps(x,indent=2)+'\n',encoding='utf8')
 else:
  x=json.loads(path.read_bytes());fresh=entries([t['packet'] for t in x['rows']]) if '--replay' in sys.argv else x['rows'];F.check(run(fresh)==x,'manifest mismatch')
 print('PASS root three',x['exact'],'closed',x['closed'])

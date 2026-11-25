"""Root-three release inventory. Separate proven coverage from conditional
cells, inactive scouts and duplicated shared graphs. Explicit declarations.
Use --replay for both-implementation proofs versus --check for SHA only.
"""
from pathlib import Path
import gzip,json,sys,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Registry import run,entries
from Portfolio import verify
from IndependentPivot import replay as independent
from NestedReplay import replay as nested

def make(pivots,trees,confirm=False):
 base=json.loads((H/'Registry.json').read_bytes());rr=base['rows'];assert run(rr)==base
 if confirm:assert entries([r['packet'] for r in rr])==rr
 rows=[dict(exponent=r['e'],proof='forest',file=r['packet'],sha256=r['sha256']) for r in rr]
 for e in [*pivots,*trees]:
  n=e in trees;name=('Nested' if n else 'Pivot')+str(e)+'.json.gz';p=H/name;d=json.loads(gzip.decompress(p.read_bytes()));assert d['e']==e
  if confirm:
   if n:nested(p)
   else:verify(p);independent(p)
  rows.append(dict(exponent=e,proof='nested' if n else 'pivot',file=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 es={r['exponent'] for r in rows};delta=json.loads((H.parent/'Nov25/Delta.json').read_bytes());shards=[s for s in delta['remaining_shards'] if s['root']==3];legit=set().union(*(s['remaining_actuals'] for s in shards));assert len(es)==len(rows) and es<=legit;closed=[s['id'] for s in shards if set(s['remaining_actuals'])<=es];return dict(root=3,fixed_baseline_sha256=hashlib.sha256((H.parent/'Nov25/Delta.json').read_bytes()).hexdigest(),covered_actuals=sorted(es),closed_shards=closed,remaining_actuals=sorted(legit-es),rows=sorted(rows,key=lambda r:r['exponent']))
if __name__=='__main__':
 p=H/'Release.json';args=sys.argv[1:];write='--make' in args
 if write:
  pivots=[int(x[1:]) for x in args if x.startswith('p')];trees=[int(x[1:]) for x in args if x.startswith('n')]
 else:
  expected=json.loads(p.read_bytes());pivots=[r['exponent'] for r in expected['rows'] if r['proof']=='pivot'];trees=[r['exponent'] for r in expected['rows'] if r['proof']=='nested']
 out=make(pivots,trees,'--replay' in args);assert write or out==expected
 if write:p.write_text(json.dumps(out,indent=2)+'\n')
 print('root3 exact',len(out['covered_actuals']),'closed shards',len(out['closed_shards']),'remain',len(out['remaining_actuals']))

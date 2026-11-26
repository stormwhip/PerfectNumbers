"""Replay conditional terminal certificates. Input records have p-independent absence/presence sets."""
from pathlib import Path
import sys,json,gzip,argparse
assert __debug__;H=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=H.parents[2]);ap.add_argument('--integer-logs',action='store_true');opt=ap.parse_args();R=opt.repo.resolve()/'Research';sys.path.insert(0,str(R/'MiddayTerminal'));import Audit,Common
assert Path(Audit.__file__).resolve()==(R/'MiddayTerminal/Audit.py').resolve()
if opt.integer_logs:
 import runpy
 Audit.logs=runpy.run_path(str(H/'AltLogs.py'))['logs']
base=json.load(gzip.open(R/'MiddayTerminal/PackNewTriple3513.json.gz'));Common.dataset=lambda:{'ecpp':base['ecpp'],'rows':{}};rows=json.loads((H/'GlobalDuals.json').read_bytes());passed=[]
for row in rows:
 bad,need,L,cut,added,w,fl=row;assert not set(bad)&set(need) and {3,5}<=set(bad) and {7,11,13}<=set(need);ext=dict((q,c) for q,c in base['args']['extend'] if q not in bad)
 for q,c in added:ext[q]=max(c,ext.get(q,0))
 kw=dict(root=0,e=0,extra=sorted(bad),x=[],lower=[[q,1] for q in sorted(need)],L=L,T=3*L,cut=cut,cap=cut,wide=True,extend=sorted(ext.items()),parity=True,weights=w);u=Audit.replay(**kw)[0];den=Audit.W*Audit.logs(10)[1];assert u//den==fl and u>2400*den;passed.append((frozenset(bad),frozenset(need)));print('PASS',bad,need,fl,flush=True);Audit.split.cache_clear();Audit.chunks.cache_clear();Audit.primeproduct.cache_clear()
assert all((frozenset([3,5,17,19,q]),frozenset([7,11,13])) in passed for q in (23,31));assert (frozenset([3,5,17,19]),frozenset([7,11,13])) in passed;print('With the three established {3,5,r} theorems (r=7,11,13), {3,5,17,19} hits every hypothetical odd perfect N <= 10^2400.');assert all((frozenset([3,5,19,q]),frozenset([7,11,13,17])) in passed for q in [23,29]);print('If 3,5,19 are absent, then 17,23,29 all occur. New four-prime hitting sets: {3,5,17,19}, {3,5,19,23}, {3,5,19,29}.')

"""Portable conditional-support verifier. Standard library only. Never writes the source tree."""
import sys,gzip,json,hashlib,subprocess,argparse
from pathlib import Path
from collections import Counter
assert __debug__;H=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=H.parents[2]);args=ap.parse_args();root=args.repo.resolve();R=root/'Research';sys.path.insert(0,str(R/'MiddayTerminal'));import Audit,Common
sys.path.insert(0,str(R/'SupportSplit'));import Verify as V
# This file is __main__, while imported Verify resolves on the prepended frozen path.
assert Path(V.__file__).resolve()==(R/'SupportSplit/Verify.py').resolve()
raw=(R/'Midday/Delta.json').read_bytes();assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='3a7b6812aafed3dddd228c34ed9575324d242887';d=json.loads(raw);pairs={(x['root'],e) for x in d['remaining_shards'] for e in x['remaining_actuals']};assert len(pairs)==244 and d['open']==204
old={(p,e,tuple(sorted(s))) for p,e,s,q in V.WITNESSES}|{(31,8,(3,5,13,31))};rem={(p,e,tuple(sorted(s))) for p,e in pairs for s in V.masks(p) if not V.leaf(p,e,s)}-old;assert len(rem)==6556
meta=json.load(gzip.open(R/'MiddayTerminal/PackNewTriple3513.json.gz'));Common.dataset=lambda:{'ecpp':meta['ecpp'],'rows':{}};new=set();K=set(V.ROOTS)
for row in json.loads((H/'Duals.json').read_bytes()):
 p=row['p'];bad=set(row['bad']);need=set(row['need']);L=row['L'];cut=row['cut'];assert (bad|need)<=K and not bad&need and p in need and set(V.ROOTS[:V.ROOTS.index(p)])<=bad
 E=max(e for q,e in pairs if p==q);ext=[(q,c) for q,c in meta['args']['extend'] if q not in bad and q!=p][:row['limit']]+[(p,E)]
 kw=dict(root=0,e=0,extra=sorted(bad),x=[],lower=[[q,1] for q in sorted(need)],L=L,T=3*L,cut=cut,cap=cut,wide=True,extend=ext,parity=True,weights=row['w']);u,rc,G,_=Audit.replay(**kw);gr=G[p];base=u-min([0]+[rc[j] for j,f,ex in gr]);den=Audit.W*Audit.logs(10)[1];res={e:(base+rc[j])//den for j,e,ex in gr if ex and (p,e) in pairs and base+rc[j]>2400*den};assert res=={int(e):v for e,v in row['expected'].items()};add={(p,e,s) for pp,e,s in rem if pp==p and e in res and not set(s)&bad and need<=set(s)};print(row['tag'],len(res),len(add),len(add-new),flush=True);new|=add
 Audit.split.cache_clear();Audit.chunks.cache_clear();Audit.primeproduct.cache_clear();Audit.logs.cache_clear();Audit.geom.cache_clear()
for script,nm in [('TreeReplay.py','EulerTrees.jsonl'),('RoleReplay.py','EulerPositions.jsonl')]:subprocess.run([sys.executable,'-I','-S','-B',str(H/script),'verify',str(root),str(H/nm)],check=True)
new.update((p,e,tuple(s)) for p,e,s,t in map(json.loads,(H/'EulerTrees.jsonl').read_text().splitlines()));assert new<=rem and sorted(new)==[(p,e,tuple(s)) for p,e,s in json.loads((H/'Ledger.json').read_bytes())];surv=rem-new;live={k[:2] for k in surv};roles={(p,e,tuple(s),q) for p,e,s,q,t in map(json.loads,(H/'EulerPositions.jsonl').read_text().splitlines())};print(json.dumps(dict(baseline_pairs=len(pairs),baseline_shards=204,baseline_support=len(rem),excluded=len(new),remaining=len(surv),pairs_touched=len({k[:2] for k in new}),new_full_pairs=sorted(pairs-live),new_full_shards=[x['id'] for x in d['remaining_shards'] if all((x['root'],e) not in live for e in x['remaining_actuals'])],by_root=Counter(k[0] for k in new),euler_positions=len(roles),position_states_still_open=sum(k[:-1] not in new for k in roles))))

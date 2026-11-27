"""Independent cell/receipt/link audit for final frozen 24-key checkpoint. NO git and no arithmetic batch replay."""
from pathlib import Path
from hashlib import sha256,sha1
from collections import Counter,defaultdict
from urllib.parse import unquote,urlsplit
import ast,sys,json,re
R=Path(sys.argv[1]).resolve();H=R/'Research/FinalNight2400';G=R/'Research/GeminiFrontier'
load=lambda p:json.loads(p.read_bytes());rows=load(H/'Results.json');cur=load(H/'OpenFrontier.json');baseline='1447d41b806f43ec5775e0cef7eaa7739ab67388'
stable={(19,58),(31,310),(13,262),(13,310),(31,352),(31,16),(11,358),(11,462),(13,388),(19,312),(7,430),(19,372),(19,420),(19,618),(11,396),(7,882),(19,330),(11,456),(19,280),(19,82),(19,282),(19,292),(31,240),(7,36)}
for fn,blob in [('ShardToKeys.json','de821605b9bb0c124ff8ca4a576f85ced96afaa2'),('KeyToShards.json','efad9522397f1b9a79aaf27c4ab90e65d58d1683')]:
 b=(G/fn).read_bytes();assert sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==blob
sh=load(G/'ShardToKeys.json');inverse=load(G/'KeyToShards.json');prev=Counter((s,*k) for s,ks in sh.items() for k in ks);inv=Counter((s,*map(int,k.split(','))) for k,ss in inverse.items() for s in ss);assert prev==inv and all(v==1 for v in prev.values())
assert all(r['BaselineCommit']==baseline for r in rows);full=[r for r in rows if r['Status']=='VERIFIED_FULL'];assert Counter(tuple(r['Key']) for r in full)==Counter(stable);now=cur['ShardRemainders'];after=Counter((s,*k) for s,ks in now.items() for k in ks); assert (not(after-prev)) and all(now[s]==sh[s] for s in now)
removed=prev-after;assert len(removed)==len(stable) and {(p,e) for s,p,e in removed}==stable and set(sh)-set(now)=={s for s,p,e in removed}
for s,p,e in removed:assert sh[s]==[[p,e]] and inverse[f'{p},{e}']==[s]
surviving={(p,e) for s,p,e in after};byroot=defaultdict(list)
for p,e in sorted(surviving):byroot[str(p)].append(e)
assert set(cur['RemainingByRoot'])==set(map(str,[19,7,11,31,13,3,5,17])) and all(cur['RemainingByRoot'][p]==byroot[p] for p in cur['RemainingByRoot'])
assert (len(sh),len(inverse),sum(len(x)==1 for x in sh.values()))==(68,78,60);count=(3072-len(now),len(now),len(surviving),sum(len(v)==1 for v in now.values()));assert count==(3028,44,54,36)==tuple(cur[k] for k in ('ClosedShards','OpenShards','DistinctKeys','SingletonShards'));assert (cur['GlobalStatus'],cur['TotalShards'],cur['ExcludedCanonicalRoots'])==('INCOMPLETE_FRONTIER',3072,[5,17])
# Parse literal actual subprocess-dispatch list without importing the integration checker.
ast0=ast.parse((H/'Verify.py').read_text(encoding='utf-8'));v=next(o.value for o in ast0.body if isinstance(o,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='CHECKS' for k in o.targets));assert isinstance(v,ast.Call) and v.func.attr=='splitlines';cmds=[l.split()[0] for l in v.func.value.value.splitlines() if l.strip()];assert all((H/f).is_file() for f in cmds)
ref_pat=re.compile(r'[a-zA-Z0-9_/.-]+[.]md');docs=set()
for r in full:
 cert=r['CertificateReference'];assert cmds.count(cert)==1 and (H/cert).is_file();
 for key in ['VerificationStatus','ProofReference']:
  last=H;refs=ref_pat.findall(r[key]);assert refs,r[key]
  for name in refs:
   p=(H/name) if '/' in name else last/name
   assert p.is_file(),(r['Key'],name,p);docs.add(p);last=p.parent
# Test all markdown links throughout overlay (including reference links), resolving relative to actual source paths.
links=0;broken=[]
for p in H.rglob('*.md'):
 t=p.read_text(encoding='utf-8');dest=re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',t)+re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)',t,re.M)
 for l in dest:
  l=l.strip().split(maxsplit=1)[0].strip('<>');u=urlsplit(l)
  if u.scheme or u.netloc or not u.path:continue
  a=(p.parent/unquote(u.path)).resolve();links+=1
  if not a.exists() or not a.is_relative_to(R):broken.append((p.relative_to(R).as_posix(),l))
print('status',Counter(r['Status'] for r in rows),'24 exact singleton removals',sorted(removed),'projection',count,'root-key counts',dict(sorted((k,len(v)) for k,v in byroot.items())),'refs docs',len(docs),'cmds',len(cmds),'local links checked',links,'broken',broken)
for n in ['Results.json','OpenFrontier.json','Verify.py','Project.py']:print(n,sha256((H/n).read_bytes()).hexdigest())
assert not broken,broken

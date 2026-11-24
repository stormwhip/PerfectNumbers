"""Optional frontier check, separate from the standalone mathematical proof."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'EveningMerge/Audit.json'
raw=p.read_bytes().replace(b'\r\n',b'\n');blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
if blob!='fc1467ec0b649137ac8922867704f43a467ca2bc':raise ValueError('not 3b50576 frontier blob')
es={808,810,820,828,838,852};a=json.loads(raw);sh=a['remaining_shards']
if len(sh)!=880:raise ValueError('inconsistent frontier size')
hits=[(s['id'],s['remaining_actuals']) for s in sh if s['root']==13 and set(s['remaining_actuals'])&es]
if len(hits)!=6 or {tuple(r) for _,r in hits}!={(e,) for e in es}:raise ValueError('incorrect shard projection')
print('3b50576',hits);over=set()
for p in sorted((R/'NightOrder').glob('Batch*Manifest.json')):
    b=json.loads(p.read_text());r={e for root,e in b['actuals'] if root==13}&es
    if r:print(p.name,sorted(r));over.update(r)
print('net after NightOrder manifests',sorted(es-over))

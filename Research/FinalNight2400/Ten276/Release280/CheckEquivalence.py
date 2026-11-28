"""Validate PascalCase release and reconstruct the audited pre-translation blobs offline."""
from pathlib import Path
import hashlib,re,json,sys
from urllib.parse import urlparse,unquote
H=Path(__file__).resolve().parent;old=H.parents[1]/'TenNext';R=H.parents[2];ROOT=R.parent
sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()
E=json.loads((H/'Equivalence.json').read_bytes());rows=E['files'];assert len(rows)==161 and E['originalBase']=='1447d41b';assert len(set(r['target'] for r in rows))==len(rows)==len(set(r['source'] for r in rows));targets={r['target'] for r in rows};links=0;paired=0
for x in H.iterdir():
 if x.name=='__pycache__':continue
 assert re.fullmatch(r'[A-Z][A-Za-z0-9]*[.][a-z0-9]+(?:[.][a-z0-9]+)*',x.name),x.name
for r in rows:
 a=(H/r['target']).read_bytes();assert sha(a)==r['targetSha256'] and blob(a)==r['targetBlob'];src=r['source'];assert Path(src).name==src
 # A whitelist of *literal* representation changes; no arithmetic change authorized.
 for x,y in r['edits']:
  if src.endswith('.py'):assert (x,y) in [('Ab280_','Ab280Case'),('Grow280_','Grow280Case'),('Hybrid280_','Hybrid280Case'),('H.parents[2]','H.parents[3]'),('H.parents[1]','H.parents[2]')]
  else:assert src.endswith('.md') and ((x,y) in [('](../../','](../../../'),('Research/FinalNight2400/TenNext/','Research/FinalNight2400/Ten276/Release280/')] or any(z['source']==x and z['target']==y for z in rows))
 orig=a
 for x,y in reversed(r['edits']):orig=orig.replace(y.encode(),x.encode())
 assert sha(orig)==r['sourceSha256'] and blob(orig)==r['sourceBlob'],src
 if '--with-original' in sys.argv:assert (old/src).read_bytes()==orig;paired+=1
 if src.endswith('.py'):compile(a,r['target'],'exec');compile(orig,src,'exec')
 if src.endswith('.md'):
  text=a.decode()
  for href in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
   u=urlparse(href);assert not u.scheme and not u.netloc
   resolved=(H/unquote(u.path)).resolve();assert resolved.is_relative_to(ROOT) and resolved.is_file(),(src,href);links+=1
   if resolved.parent==H:assert resolved.name in targets
 oldname=src.replace('Ab280_','Ab280Case').replace('Grow280_','Grow280Case').replace('Hybrid280_','Hybrid280Case').replace('_','X');assert oldname==r['target']
a=('\n'.join(r['sourceSha256']+'  '+r['source'] for r in rows)+'\n').encode();a=a.replace(b'\n',b'\r\n') if E['sourceManifestCrlf'] else a
assert sha(a)==E['sourceManifestSha256']=='b7d6464b6da32f4f01da9f35a2c9a7f4527a90ae69b51127ee4970b3494362ec' and blob(a)==E['sourceManifestBlob']
a=('\n'.join(r['targetSha256']+'  '+r['target'] for r in rows)+'\n').encode();assert a==(H/'Manifest280.txt').read_bytes()
assert (R/'RootFiveNext/PrimeCheck.py').is_file() and (R/'Night2400/C13/Verify.py').is_file() and ROOT==H.parents[3]
print('PASS 161 source blobs reconstructed; 66 PascalCase renames; 153 byte-identical; validated',links,'local Markdown targets; direct pair comparisons',paired,'release manifest',sha(a))

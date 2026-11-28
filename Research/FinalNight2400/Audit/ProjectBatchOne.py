"""Independent projection for immutable five-key batch; no changes or full arithmetic replay."""
import hashlib,json,sys
from collections import Counter
from pathlib import Path
assert __debug__;root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[3];H=root/'Research/FinalNight2400';G=root/'Research/GeminiFrontier'
def load(p):return json.loads(p.read_bytes())
pairs={(19,58):'P19_I00015',(31,310):'P31_I00062',(13,262):'P13_I00055',(13,310):'P13_I00063',(31,352):'P31_I00069'}
accepted={(19,58):'Ten/VerifyFull.py',(31,310):'Others/Full31.py',(13,262):'Others/Full13.py',(13,310):'Others/FullNext.py',(31,352):'Others/FullMore.py'}
old=load(G/'ShardToKeys.json'); rev=load(G/'KeyToShards.json');results=load(H/'Results.json');now=load(H/'OpenFrontier.json')
def cells(d):return {(s,*k) for s,ks in d.items() for k in ks}
oldcells=cells(old);oldinv={(s,*map(int,k.split(','))) for k,ss in rev.items() for s in ss}; assert oldcells==oldinv
assert len(old)==68 and len(rev)==78 and sum(len(ks)==1 for ks in old.values())==60
full=[r for r in results if r['Status']=='VERIFIED_FULL']; assert Counter(tuple(r['Key']) for r in full)==Counter(pairs.keys())
check=(H/'Verify.py').read_text(encoding='utf-8').splitlines()
for r in results:
 assert r['BaselineCommit']=='1447d41b806f43ec5775e0cef7eaa7739ab67388' and r['Status'] in ('VERIFIED_FULL','VERIFIED_CONDITIONAL','CANDIDATE')
 if r['Status']=='VERIFIED_FULL':
  k=tuple(r['Key']);s=pairs[k];cert=r['CertificateReference'];assert cert==accepted[k] and cert in check and (H/cert).is_file() and (H/r['ProofReference']).is_file()
  assert old[s]==[list(k)] and rev[','.join(map(str,k))]==[s]
after=cells(now['ShardRemainders']);difference=oldcells-after
assert after<=oldcells and difference=={(v,*k) for k,v in pairs.items()}
assert set(old)-set(now['ShardRemainders'])==set(pairs.values()) and all(now['ShardRemainders'][s]==old[s] for s in now['ShardRemainders'])
keys={(p,e) for s,p,e in after};assert {(int(p),e) for p,vs in now['RemainingByRoot'].items() for e in vs}==keys
assert all(now['RemainingByRoot'][str(p)]==sorted(e for pp,e in keys if pp==p) for p in (19,7,11,31,13,3,5,17));counts=(3072-len(now['ShardRemainders']),len(now['ShardRemainders']),len(keys),sum(len(z)==1 for z in now['ShardRemainders'].values()))
assert counts==(3009,63,73,55)==tuple(now[n] for n in ('ClosedShards','OpenShards','DistinctKeys','SingletonShards'));assert now['TotalShards']==3072 and now['GlobalStatus']=='INCOMPLETE_FRONTIER';print('PASS complete Five, no conditional credits, precise removed triples:',sorted(difference),'counters',counts,'record-status counts',Counter(r['Status'] for r in results));
for p in (H/'Results.json',H/'OpenFrontier.json',H/'Verify.py'):print(p.name,hashlib.sha256(p.read_bytes().replace(bytes((13,10)),bytes((10,)))).hexdigest())

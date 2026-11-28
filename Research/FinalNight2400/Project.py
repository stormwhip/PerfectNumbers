"""Project accepted full keys only. No discovery, and no full-key attestation by JSON alone."""
import argparse,hashlib,json
from pathlib import Path
from collections import defaultdict
here=Path(__file__).resolve().parent
base=here.parent/'GeminiFrontier'
sha='1447d41b806f43ec5775e0cef7eaa7739ab67388'
def load(name,blob):
    data=(base/name).read_bytes().replace(b'\r\n',b'\n')
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
    return json.loads(data)
shards=load('ShardToKeys.json','de821605b9bb0c124ff8ca4a576f85ced96afaa2');inv=defaultdict(list)
for s,K in shards.items():
    assert len(set(map(tuple,K)))==len(K) and K
    for p,e in K: inv[f'{p},{e}'].append(s)
assert dict(inv)==load('KeyToShards.json','efad9522397f1b9a79aaf27c4ab90e65d58d1683')
results=json.loads((here/'Results.json').read_text(encoding='utf-8'));full=set()
for row in results:
    assert row['BaselineCommit']==sha and row['Status'] in ('CANDIDATE','VERIFIED_CONDITIONAL','VERIFIED_FULL')
    if row['Status']=='VERIFIED_FULL': full.add(tuple(row['Key']))
assert all(f'{p},{e}' in inv for p,e in full)
now={s:[k for k in K if tuple(k) not in full] for s,K in shards.items()};now={s:k for s,k in now.items() if k}
pool=sorted({tuple(k) for K in now.values() for k in K});roots=(19,7,11,31,13,3,5,17)
output=dict(BaselineCommit=sha,GlobalStatus='INCOMPLETE_FRONTIER',TotalShards=3072,ClosedShards=3072-len(now),OpenShards=len(now),DistinctKeys=len(pool),SingletonShards=sum(len(K)==1 for K in now.values()),ExcludedCanonicalRoots=[5,17],CoprimeCase='excluded in baseline; no new full-history cold replay',RemainingByRoot={p:[e for pp,e in pool if pp==p] for p in roots},InheritedConditionalIndexes=['Research/Night2400/README.md','Research/GeminiFrontier/Review.md','Research/FinalSprint/Support/README.md'],ShardRemainders=now)
text=json.dumps(output,indent=2)+'\n';dest=here/'OpenFrontier.json'
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.write:dest.write_text(text,encoding='utf-8',newline='\n')
    else:assert dest.read_text(encoding='utf-8')==text
    print({k:output[k] for k in ('ClosedShards','OpenShards','DistinctKeys','SingletonShards')})

"""Synchronize both human-facing reports to the exact incidence relation. No arithmetic closure by metadata."""
from pathlib import Path
import hashlib,json
from collections import Counter
H=Path(__file__).resolve().parent

def j(p):return json.loads(p.read_bytes())
if __name__=='__main__':
 assert __debug__
 old=j(H.parent/'GeminiFrontier/ShardToKeys.json');records=j(H/'Results.json');delta=j(H/'OpenFrontier.json');now=delta['ShardRemainders'];complete=[tuple(r['Key']) for r in records if r['Status']=='VERIFIED_FULL'];E=set(complete);assert len(E)==len(complete)
 assert delta['GlobalStatus']=='INCOMPLETE_FRONTIER' and set(now)<=set(old)
 removed={}
 for name,ks in old.items():
    expected=[pair for pair in ks if tuple(pair) not in E];assert now.get(name,[])==expected
    if not expected:
        assert len(ks)==1 and tuple(ks[0]) not in removed;removed[tuple(ks[0])]=name
 assert set(removed)==E
 table={}
 for line in (H/'Proof.md').read_text('utf8').splitlines():
    if not line.startswith('|('):continue
    _,pair,shard,link,_=line.split('|');pair=tuple(map(int,pair.strip('()').split(',')));assert pair not in table and (H/link.split('](')[1][:-1]).is_file();table[pair]=shard
 assert table==removed
 rows={}
 for line in (H/'Report.md').read_text('utf8').splitlines():
    if line.startswith('|') and line.split('|')[1].isdigit():
        _,p,done,n,remain,_=line.split('|');p=int(p);rr=tuple(map(int,remain.split(',')));closed=[] if done=='无' else list(map(int,done.split(',')))
        assert sorted(closed)==sorted(e for q,e in E if q==p) and list(rr)==delta['RemainingByRoot'][str(p)] and int(n)==sum(s.startswith('P'+str(p)+'_') for s in now);rows[p]=rr
 assert set(rows)=={p for p,e in (tuple(k) for K in now.values() for k in K)}
 candidates={tuple(k) for K in now.values() for k in K};stats=(3072-len(now),len(now),len(candidates),sum(len(K)==1 for K in now.values()));assert stats==tuple(delta[k] for k in ('ClosedShards','OpenShards','DistinctKeys','SingletonShards'))
 print('PASS independent exact set difference, per-key singleton and proof links, Chinese per-root table:',len(E),'new full keys; counts',stats)

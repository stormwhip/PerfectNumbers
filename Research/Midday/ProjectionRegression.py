"""Fast adversarial projection tests on the final release, without running discoveries.
A duplicate proof reference, representative-only deletion, digest mismatch, and
unregistered exponent must all be rejected. These are bookkeeping tests, not proof replay.
"""
from pathlib import Path
import copy,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from LedgerTests import check

def main():
    if not __debug__:raise SystemExit('assertions must be enabled')
    d=json.loads((H/'Delta.json').read_bytes());r=json.loads((H/'Registry.json').read_bytes());b=json.loads((H.parent/'Nov25/Delta.json').read_bytes());check(b,d,r)
    def rejects(tag,x,reg):
        try:check(b,x,reg)
        except (AssertionError,ValueError,KeyError):print('REJECT',tag);return
        raise ValueError('accepted '+tag)
    x=copy.deepcopy(d);x['proofs'].append(copy.deepcopy(x['proofs'][0]));rejects('duplicate proof reference',x,r)
    x=copy.deepcopy(d);key=next(i for i,s in enumerate(x['remaining_shards']) if len(s['remaining_actuals'])>=2);x['remaining_shards'][key]['remaining_actuals']=x['remaining_shards'][key]['remaining_actuals'][:1];rejects('lost secondary obligation',x,r)
    x=copy.deepcopy(d);u=next(s for s in x['remaining_shards'] if len(s['remaining_actuals'])>=2);x['new_shards'].append(u['id']);rejects('premature shard closure',x,r)
    x=copy.deepcopy(d);u=x['remaining_shards'][0];x['new_actuals'].append([u['root'],u['remaining_actuals'][0]]);rejects('unregistered actual',x,r)
    rr=copy.deepcopy(r);rel=next(iter(rr['forests']));rr['forests'][rel]='0'*64;rejects('bad packet digest',d,rr)
    print('PASS five negative ledger tests')
if __name__=='__main__':main()

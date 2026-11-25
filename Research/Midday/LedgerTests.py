"""Independent projection and cold-ledger integrity tests. No proof search or discovery input."""
import json,hashlib,gzip,argparse
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;ROOT=R.parent

def check(b,d,reg):
    s0=b['remaining_shards'];users={};old={}
    for s in s0:
        k=s['id'];assert k not in old;old[k]=s.copy();es=s['remaining_actuals'];assert es==sorted(set(es)) and es
        for e in es:
            assert (e==s['exponent'] if s['exact'] else (e+1)%(s['exponent']+1)==0);users.setdefault((s['root'],e),set()).add(k)
    assert (len(s0),len(users),sum(map(len,users.values())))==(406,511,582)
    got=set(); alive={k:set(s['remaining_actuals']) for k,s in old.items()};proofnames=set();allfiles=set(reg['forests'])|set(reg.get('prefix_trees',{}))|set(reg.get('special',{}))
    assert d['status']=='INCOMPLETE_FRONTIER'
    assert reg['baseline']==d['baseline']
    required=Counter();reported=Counter()
    for rel in allfiles:
        raw=(ROOT/rel).read_bytes();packet=json.loads(gzip.decompress(raw) if rel.endswith('.gz') else raw)
        if rel in ('Research/Midday/ReleaseSupply7x1018.json','Research/Midday/ReleaseSupply11x718.json'):
            p,e=packet['root'],packet['exponent'];assert rel==f'Research/Midday/ReleaseSupply{p}x{e}.json' and packet['domain']==[0,e];keys=[(p,e)]
        elif rel in reg['forests']:
            if 'row' in packet:keys=[(3,packet['row']['e'])]
            else:r,=packet['rows'];keys=[(r['p'],r['e'])]
        elif rel in reg.get('prefix_trees',{}):keys=[(packet['p'],packet['e'])]
        elif rel=='Research/MiddayFive/Accepted.json.gz':keys=[(5,r['e']) for r in packet];assert set(keys)=={k for k in users if k[0]==5}
        elif rel.startswith('Research/MiddayThree/'):keys=[(3,packet['e'])]
        elif rel.startswith('Research/Midday/Euler'):keys=[(packet['general']['p'],packet['general']['e'])]
        else:raise ValueError('unsupported packet '+rel)
        required.update((rel,p,e) for p,e in keys)
    for row in d['proofs']:
        reported[(row['packet'],*row['seed'])]+=1
        rel=row['packet'];p,e=row['seed'];assert rel in allfiles and (p,e) in users;proofnames.add(rel)
        wanted={f for pp,f in users if pp==p and (f+1)%(e+1)==0 and f>=e} if rel in reg['forests'] else {e};assert sorted(wanted)==row['actuals']
        for f in wanted:
            if (p,f) in got:continue
            got.add((p,f))
            for k in users[p,f]:alive[k].remove(f)
    assert required==reported and all(n==1 for n in required.values())
    assert proofnames==allfiles and sorted(map(list,got))==d['new_actuals']
    left=[dict(s,remaining_actuals=sorted(alive[k])) for k,s in old.items() if alive[k]];closed=[k for k in old if not alive[k]];assert left==d['remaining_shards'] and closed==d['new_shards'];assert d['closed']==2666+len(closed) and d['open']==len(left) and d['closed']+d['open']==3072 and d['open_actuals']==511-len(got) and d['singletons']==sum(len(x['remaining_actuals'])==1 for x in left)
    for group in ('forests','prefix_trees','special'):
        for p,v in reg.get(group,{}).items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v
    print('PASS independent overlap reconciliation:',len(got),'distinct keys;',len(closed),'new canonical shards;',len(left),'open')
if __name__=='__main__':
    if not __debug__:raise SystemExit('no -O')
    ap=argparse.ArgumentParser();ap.add_argument('--delta',type=Path,default=H/'Delta.json');ap.add_argument('--registry',type=Path,default=H/'Registry.json');a=ap.parse_args();check(json.loads((R/'Nov25/Delta.json').read_bytes()),json.loads(a.delta.read_bytes()),json.loads(a.registry.read_bytes()))

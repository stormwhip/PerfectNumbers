"""Recheck ordinary forest packets using two existing integer implementations.
The fresh delta is a projection of the pinned 204-shard ledger, not a count of files.
Run: python -I -S -B Research/Session20261126/Replay.py [--write]
"""
from pathlib import Path
from hashlib import sha256
import sys,json,gzip
H=Path(__file__).resolve().parent
R=H.parent
sys.path[:0]=[str(R/'MiddayForest'),str(R/'Midday')]
from Verify import verify
from ModeCheck import replay

def projection():
    raw=(R/'Midday/Delta.json').read_bytes().replace(b'\r\n',b'\n')
    import hashlib
    if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!='3a7b6812aafed3dddd228c34ed9575324d242887':
        raise ValueError('unexpected baseline ledger')
    sh=json.loads(raw)['remaining_shards']; original={(s['root'],e) for s in sh for e in s['remaining_actuals']}
    assert len(sh)==204 and len(original)==244
    proofs=[];excluded=set()
    for path in sorted(H.glob('Forest*.json.gz')):
        p,e,floor,digest=verify(path);data=json.loads(gzip.decompress(path.read_bytes()));row,=data['rows']
        assert path.name==f'Forest{p}x{e}.json.gz' and (p,e) in original
        assert set(row)=={'p','e','head','owners','roots'}
        pp,ee,values=replay({'general':row,'special':{},'ecpp':data['ecpp']})
        assert (pp,ee)==(p,e) and values==[floor]
        hits=sorted(f for q,f in original if q==p and (f+1)%(e+1)==0)
        excluded.update((p,f) for f in hits)
        proofs.append(dict(packet=path.name,sha256=digest,seed=[p,e],floor=floor,actuals=hits))
        print('PASS',p,e,floor,hits,flush=True)
    sys.path.insert(0,str(R/'NightLowRoute/Release'))
    import ForestReplay
    for path in sorted(H.glob('Price*.json.gz')):
        p,e,floor,digest=verify(path);data=json.loads(gzip.decompress(path.read_bytes()));r,=data['rows']
        assert p in (13,19,31) and path.name==f'Price{p}x{e}.json.gz' and (p,e) in original
        assert min(ForestReplay.proof(r,data['ecpp']).values())>10**(2400*r['den'])
        excluded.add((p,e));proofs.append(dict(packet=path.name,sha256=digest,seed=[p,e],floor=floor,actuals=[e]));print('PASS exact priced forest',p,e,flush=True)
    sys.path.insert(0,str(H))
    import PivotCheck
    for path in sorted(H.glob('Pivot*.json.gz')):
        p,e,floor,n=PivotCheck.verify(path)
        assert path.name==f'Pivot{p}x{e}.json.gz' and (p,e) in original
        excluded.add((p,e));proofs.append(dict(packet=path.name,sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],forest_leaf_min_floor=floor,forest_leaves=n,actuals=[e]))
        print('PASS exact pivot',p,e,floor,n,flush=True)
    import TreeCheck
    for path in sorted(H.glob('Tree*.json.gz')):
        p,e,stats=TreeCheck.verify(path);assert path.name==f'Tree{p}x{e}.json.gz' and (p,e) in original
        excluded.add((p,e));proofs.append(dict(packet=path.name,sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],forest_leaves=stats[0],split_nodes=stats[1],direct_cases=stats[2],actuals=[e]));print('PASS exact tree',p,e,stats,flush=True)
    from subprocess import check_output
    for path in sorted(H.glob('MaskTree*.json.gz')):
        import ast
        p,e,stats=ast.literal_eval(check_output([sys.executable,'-I','-S','-B',str(H/'CheckMaskTree.py'),'--repo',str(R.parent),str(path)],text=True).splitlines()[-1]);second=check_output([sys.executable,'-I','-S','-B',str(H/'IndependentMask.py'),'--repo',str(R.parent),str(path)],text=True).splitlines()[-1]
        assert second==f'verified {p} {e} {stats}' and path.name==f'MaskTree{p}x{e}.json.gz' and (p,e) in original
        excluded.add((p,e));proofs.append(dict(packet=path.name,sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],forest_leaves=stats[0],split_nodes=stats[1],direct_cases=stats[2],actuals=[e]));print('PASS full S8 support tree',p,e,flush=True)
    for path in sorted(H.glob('Hybrid*.json.gz')):
        import ast
        p,e,stats=ast.literal_eval(check_output([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(H/'HybridCheck.py'),'--repo',str(R.parent),str(path)],text=True).splitlines()[-1]);assert path.name==f'Hybrid{p}x{e}.json.gz' and (p,e) in original
        excluded.add((p,e));proofs.append(dict(packet=path.name,sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],forest_leaves=stats[0],split_nodes=stats[1],direct_cases=stats[2],dual_leaves=stats[3],actuals=[e]));print('PASS hybrid forest/dual tree',p,e,flush=True)
    cut_dir=H/'SupplyForest';packets=sorted(cut_dir.glob('Cut*.json.gz'))
    if packets:
        raw=check_output([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(cut_dir/'VerifyCut.py'),str(R),*map(str,packets)],text=True)
        answers=[json.loads(line) for line in raw.splitlines()];assert len(answers)==len(packets)
        for path,answer in zip(packets,answers):
            p,e=answer['actual'];assert path.name==f'Cut{p}x{e}.json.gz' and (p,e) in original
            excluded.add((p,e));proofs.append(dict(packet='SupplyForest/'+path.name,sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],actuals=[e],receipt=answer));print('PASS exact supply cut',p,e,flush=True)
    branch_dir=cut_dir/'Breakpoint'
    for path in sorted(branch_dir.glob('Branch*.json.gz')):
        v=json.loads(check_output([sys.executable,'-I','-S','-B',str(branch_dir/'VerifyBranch.py'),str(R),str(path)],text=True));p,e=v['p'],v['e'];assert (p,e) in original and path.name==f'Branch{p}x{e}.json.gz'
        excluded.add((p,e));proofs.append(dict(packet=path.relative_to(H).as_posix(),sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],actuals=[e],receipt=v))
    recursive=cut_dir/'Recursive'
    for path in sorted(recursive.glob('Recursive*.json.gz')):
        v=json.loads(check_output([sys.executable,'-I','-S','-B',str(recursive/'Domain.py'),str(R),str(path)],text=True));p,e=v['p'],v['e'];assert (p,e) in original and path.name==f'Recursive{p}x{e}.json.gz'
        excluded.add((p,e));proofs.append(dict(packet=path.relative_to(H).as_posix(),sha256=sha256(path.read_bytes()).hexdigest(),seed=[p,e],actuals=[e],receipt=v))
    import JointReplay
    joint=JointReplay.verify();assert joint['seed']==[3,1162] and (3,1162) in original
    excluded.add((3,1162));proofs.append(joint);print('PASS complete E0/E1/E2/E3 and range sieve: 3 1162',flush=True)
    remaining=[];closed=[]
    for s in sh:
        left=[e for e in s['remaining_actuals'] if (s['root'],e) not in excluded]
        if left:remaining.append(dict(s,remaining_actuals=left))
        else:closed.append(s['id'])
    assert {(s['root'],e) for s in remaining for e in s['remaining_actuals']}==original-excluded
    return dict(baseline='2889e47f6db49c8a9bc8dda2c9153829c18a70ca',status='INCOMPLETE_FRONTIER',proofs=proofs,new_actuals=sorted(map(list,excluded)),new_shards=closed,closed=2868+len(closed),open=len(remaining),open_actuals=len(original-excluded),remaining_shards=remaining)

if __name__=='__main__':
    if not __debug__ or sys.argv[1:] not in ([],['--write']):raise SystemExit('assertions required; optional argument --write')
    result=projection();dest=H/'Delta.json'
    if sys.argv[1:]:dest.write_text(json.dumps(result,indent=1)+'\n',encoding='utf8',newline='\n')
    elif result!=json.loads(dest.read_bytes()):raise ValueError('ledger mismatch')
    print('closed / open / open actuals:',result['closed'],result['open'],result['open_actuals'])

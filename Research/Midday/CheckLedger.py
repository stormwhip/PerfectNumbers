"""Cold verification: replay each registered forest, then recompute the entire canonical delta.
Registration is explicit. No discovery output, working clone cache, network or numeric library is required.
"""
from pathlib import Path
import argparse,hashlib,json,gzip,sys,importlib.util
from concurrent.futures import ProcessPoolExecutor
from math import prod,gcd
H=Path(__file__).resolve().parent;R=H.parent;ROOT=R.parent
BASE='6732a1a894817457a1bc1b88b7d214ac4d6c9872'

def need(c,msg):
    if not c:raise ValueError(msg)

def one(item):
    rel,sha=item;f=ROOT/rel;d=f.read_bytes();need(hashlib.sha256(d).hexdigest()==sha,'packet digest');packet=json.loads(gzip.decompress(d));r,=packet['rows'];p,e=r['p'],r['e'];den=r.get('den',1);need(p in (3,5,7,11,13,19,31),'unsupported forest adapter')
    if p in (3,5):
        sys.path.insert(0,str(H));from ModeCheck import replay
        replay({'general':r,'special':{},'ecpp':packet['ecpp']});return p,e,10**2400+1,1
    folder=R/('NightSevenForest/Release' if p in (7,11) else 'NightLowRoute/Release');script=folder/('Replay.py' if p in (7,11) else 'ForestReplay.py');spec=importlib.util.spec_from_file_location('PinnedForest',script);vm=importlib.util.module_from_spec(spec);spec.loader.exec_module(vm);vs=vm.proof(r,packet['ecpp']);bound=min(vs.values());need(bound>10**(2400*den),'pinned integer bound failed');return p,e,bound,den

def ledger(reg,workers):
    basefile=R/'Nov25/Delta.json';base=json.loads(basefile.read_bytes());need(reg['baseline']==BASE and reg['baseline_delta_sha256_lf']==hashlib.sha256(basefile.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),'wrong baseline');sh=base['remaining_shards'];ob={(s['root'],e) for s in sh for e in s['remaining_actuals']};need(len(ob)==511 and len(sh)==406,'wrong baseline totals')
    files=list(reg['forests'].items());proofs=[]
    with ProcessPoolExecutor(workers) as pool:
        for i,((rel,_),(p,e,amount,den)) in enumerate(zip(files,pool.map(one,files))):
            need((p,e) in ob,'seed not open');hits=sorted(f for pp,f in ob if pp==p and (f+1)%(e+1)==0 and f>=e);proofs.append({'packet':rel,'seed':[p,e],'actuals':hits});print('PASS',p,e,'Euler-complete; targets',hits,flush=True)
    new={(x['seed'][0],f) for x in proofs for f in x['actuals']};closed=[];left=[]
    for s in sh:
        es=[e for e in s['remaining_actuals'] if (s['root'],e) not in new]
        if es:left.append(dict(s,remaining_actuals=es))
        else:closed.append(s['id'])
    return {'baseline':BASE,'status':'INCOMPLETE_FRONTIER','proofs':proofs,'new_actuals':sorted(map(list,new)),'new_shards':closed,'closed':2666+len(closed),'open':len(left),'open_actuals':len(ob-new),'singletons':sum(len(s['remaining_actuals'])==1 for s in left),'remaining_shards':left}

def main():
    a=argparse.ArgumentParser();a.add_argument('--registry',type=Path,default=H/'Registry.json');a.add_argument('--write',type=Path);a.add_argument('--check',type=Path);a.add_argument('--workers',type=int,default=3);args=a.parse_args();out=ledger(json.loads(args.registry.read_bytes()),args.workers)
    if args.write:args.write.write_text(json.dumps(out,indent=1)+'\n',encoding='utf8',newline='\n')
    if args.check:need(out==json.loads(args.check.read_bytes()),'delta mismatch')
    print('PASS',len(out['new_actuals']),'actuals;',len(out['new_shards']),'new shards;',out['open'],'remain')
if __name__=='__main__':
    need(__debug__,'no -O');main()

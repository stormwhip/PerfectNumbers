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
    rel,sha=item;f=ROOT/rel;d=f.read_bytes();need(hashlib.sha256(d).hexdigest()==sha,'packet digest');packet=json.loads(gzip.decompress(d));
    if set(packet)=={'row','ecpp'} and rel.startswith('Research/MiddayThree/'):
        t=packet['row'];r={'p':3,'e':t['e'],'roots':t['roots'],'owners':t['edges'],'head':t['head']}
    else:r,=packet['rows']
    p,e=r['p'],r['e'];den=r.get('den',1);need(p in (3,5,7,11,13,19,31),'unsupported forest adapter')
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
    # Exact-prefix trees have no automatic index lift.
    for rel,sha in reg.get('prefix_trees',{}).items():
        f=ROOT/rel;need(hashlib.sha256(f.read_bytes()).hexdigest()==sha,'tree digest');sys.path.insert(0,str(R/'MiddayGraph'))
        if rel=='Research/MiddayGraph/Batch4_13x136d5.json.gz':
            from Release import verify
            pair=(13,136)
        elif rel=='Research/MiddayGraph/EcmC13x80d3.json.gz':
            from Release80 import verify
            pair=(13,80)
        elif rel=='Research/MiddayGraph/Batch4_31x136d4.json.gz':
            from Release31136 import verify
            pair=(31,136)
        else:raise ValueError('unsupported prefix proof')
        keys=verify(f);need(keys=={pair} and keys<=ob,'wrong exact tree');proofs.append({'packet':rel,'seed':list(pair),'actuals':[pair[1]]})
    for rel,sha in reg.get('special',{}).items():
        import subprocess
        path=ROOT/rel;raw=path.read_bytes();need(hashlib.sha256(raw.replace(b'\r\n',b'\n') if rel.endswith('.json') else raw).hexdigest()==sha,'special packet digest')
        if rel=='Research/MiddayFive/Accepted.json.gz':
            es=sorted(e for p,e in ob if p==5);need(len(es)==14,'five domain');cmd=[str(R/'MiddayFive/Replay.py'),'--audit',*map(str,es)];p=5
        elif path.parent==R/'MiddayThree' and path.name.startswith('Pivot') and path.name.endswith('.json.gz'):
            e=json.loads(gzip.decompress(path.read_bytes()))['e'];need(type(e)==int and (3,e) in ob and path.name==f'Pivot{e}.json.gz','wrong pivot');p=3;es=[e];cmd=[str(R/'MiddayThree/IndependentPivot.py'),str(path)]
        elif path.parent==R/'MiddayThree' and path.name.startswith('Nested') and path.name.endswith('.json.gz'):
            pkt=json.loads(gzip.decompress(path.read_bytes()));e=pkt['e'];need(type(e)==int and (3,e) in ob and path.name==f'Nested{e}.json.gz','wrong nested packet');p=3;es=[e];cmd=[str(R/'MiddayThree/NestedReplay.py'),str(path)]
        elif rel in ('Research/Midday/ReleaseSupply7x1018.json','Research/Midday/ReleaseSupply11x718.json'):
            d=json.loads(path.read_bytes());p,e=(7,1018) if rel.endswith('7x1018.json') else (11,718);es=[e];need(d=={'root':p,'exponent':e,'domain':[0,e],'forbidden':[19] if p==7 else [19,7]} and (p,e) in ob,'source scope')
            cmd=[sys.executable,'-I','-S','-B',str(R/'MiddaySupply/Release.py'),str(p),'0',str(e),'--kind','independent','--require-complete'];run=subprocess.run(cmd,check=True,capture_output=True,text=True);answer=json.loads(run.stdout.splitlines()[-1]);need(answer=={'p':p,'e':e,'domain':[0,e],'kind':'independent','open':[],'count':e+1},'source domain incomplete');print('PASS source',p,e,e+1,'windows',flush=True);proofs.append({'packet':rel,'seed':[p,e],'actuals':[e]});continue
        elif path.parent==H and path.name.startswith('Euler') and path.name.endswith('.json.gz'):
            pkt=json.loads(gzip.decompress(path.read_bytes()));p,e=pkt['general']['p'],pkt['general']['e'];need(type(p)==type(e)==int and (p,e) in ob and path.name==f'Euler{p}x{e}.json.gz','Euler-cover scope');es=[e]
            subprocess.run([sys.executable,'-I','-S','-B',str(H/'ModeCheck.py'),str(path)],check=True);cmd=[str(H/'IndependentModes.py'),str(path)]
        else:raise ValueError('unsupported special packet')
        subprocess.run([sys.executable,'-I','-S','-B',*cmd],check=True)
        for e in es:proofs.append({'packet':rel,'seed':[p,e],'actuals':[e]})
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

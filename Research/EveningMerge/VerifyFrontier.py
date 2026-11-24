"""Merge certificates relative to 4aad42d. Default: first replay ALL evening packets in isolated processes."""
import argparse,csv,json,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1];H=R/'EveningMerge';BASE={1296,1300,1302,1308,1312,1330}

def read(path):return json.loads((R/path).read_text(encoding='utf-8'))

def replay(workers):
    with tempfile.TemporaryDirectory() as tmp:
        five=Path(tmp)/'five.json'
        jobs=[['GapSupply2400/CheckShards.py'],['OrderSupplyNext/VerifyOrderSupply.py','--workers',str(workers),'--output',str(five)],['RootFiveNext/CheckCertificate.py'],['EveningRoot3/IndependentEvening.py','--verify-accepted'],['ThreeChainNext/Replay.py'],['EveningTree/IndependentTree.py','--allow-overlap','--input',str(R/'EveningTree/Verified.json')],['EveningTree/IndependentTree.py','--valuation','--allow-overlap','--input',str(R/'EveningTree/OrderVerified.json')]]
        for script,*args in jobs:subprocess.run([sys.executable,'-B',str(R/script),*args],check=True)
        if json.loads(five.read_text())!=read('OrderSupplyNext/Audit.json'):raise ValueError('five-root replay does not reproduce manifest')

def merge():
    sys.path.insert(0,str(R/'OrderSupplyNext'));import VerifyOrderSupply as v
    te=read('TeichmullerValuation/Audit2400.json');ge=read('TeichmullerValuation/GeminiBatchAudit2400.json');hist={s['id'] for s in ge['additions']};prior={f'P3_I00{i}' for i in (212,213,214)}
    before=[s for s in te['open_manifest'] if s['id'] not in hist|prior];assert len(before)==1042 and len(set(x['id'] for x in before))==1042
    raw={}
    raw['gap3']={(3,x['e']) for x in read('EveningRoot3/BothAudit.json')};raw['chain3']={(3,x['e']) for x in read('ThreeChainNext/Certificates.json')};raw['root5']={(5,e) for e in read('RootFiveNext/RootFiveVerified.json')['exponents']};raw['order']={tuple(x) for x in read('OrderSupplyNext/Audit.json')['new']}
    for k,file in [('size','Verified.json'),('order_tree','OrderVerified.json')]:raw[k]={(r['p'],r['e']) for r in read('EveningTree/'+file)}
    allpairs=set.union(*raw.values());_,previous=v.audits();old=set(previous)|{tuple(x) for x in ge['verified_exponents']}
    for file in ('SupplierBatch/BatchAudit2400.json','IndicatorCapacity/Audit2400.json'):old.update((x['root'],x['exponent']) for x in read(file)['exact_exponents'])
    old.update((x['root'],x['exponent']) for x in read('EulerOneSieve/ActualExponentRecords.json'));old.update((3,e) for e in BASE)
    with (R/'FermatRootValuation/Exponents.csv').open() as f:small={(int(r['p']),int(r['actual_e'])) for r in csv.DictReader(f) if r['result']=='OPEN'}-old
    new=[];left=[];universe=set()
    for s in before:
        p=s['root'];d=s['exponent'];exact=s['exact']
        if p in (3,5):es={e for pp,e in small if pp==p and (e==d if exact else (e+1)%(d+1)==0)}
        else:es={e for e in v.tb.covered_exponents(p,d,exact) if (p,e) not in old and p**e*v.tb.odd_part(v.tb.sigma(p,e))<=v.B and not v.baseline(p,e)}
        universe.update((p,e) for e in es);rem={e for e in es if (p,e) not in allpairs}
        if es and not rem:new.append(dict(id=s['id'],p=p,representative=d,actuals=sorted(es)))
        else:left.append(dict(s,remaining_actuals=sorted(rem)))
    proved=allpairs&universe
    return dict(baseline='4aad42d',theorem_status='INCOMPLETE_FRONTIER',baseline_closed=2030,baseline_open=1042,packet_counts={k:len(x) for k,x in raw.items()},new_actuals=len(proved),by_root_actuals=dict(sorted(Counter(p for p,e in proved).items())),new_shards=len(new),by_root_shards=dict(sorted(Counter(x['p'] for x in new).items())),closed=2030+len(new),open=len(left),accepted_actuals=sorted(proved),closed_shards=new,remaining_shards=left)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-only',action='store_true',help='counts only; not certificate verification');ap.add_argument('--output',type=Path);ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    if not __debug__:raise SystemExit('Run without -O')
    if not args.manifest_only:replay(args.workers)
    a=merge();txt=json.dumps(a,indent=1)+'\n';print('merge only' if args.manifest_only else 'proof replay complete',{k:v for k,v in a.items() if k not in ('accepted_actuals','closed_shards','remaining_shards')});
    if args.output:args.output.write_text(txt,encoding='utf-8')
    elif json.loads(txt)!=read('EveningMerge/Audit.json'):raise ValueError('stored merged audit differs')
if __name__=='__main__':main()

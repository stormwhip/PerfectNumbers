"""Map complete exact exponents against the independently published prior frontier."""
import csv,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parent
def load(p):return json.loads(p.read_text())
def delta(exps):
 su=load(R/'SupplierBatch/BatchAudit2400.json');ic=load(R/'IndicatorCapacity/Audit2400.json');te=load(R/'TeichmullerValuation/Audit2400.json');ge=load(R/'TeichmullerValuation/GeminiBatchAudit2400.json');prior={(x['root'],x['exponent']) for a in (su,ic) for x in a['exact_exponents']}|set(map(tuple,ge['verified_exponents'])); prior.update((x['root'],y['exponent']) for x in te['additions'] for y in x['proof']); ids={x['id'] for x in ge['additions']};old=[x for x in te['open_manifest'] if x['id'] not in ids];assert len(old)==1045
 with (R/'FermatRootValuation/Exponents.csv').open() as f:pending={int(x['actual_e']) for x in csv.DictReader(f) if x['p']=='5' and x['result']=='OPEN' and (5,int(x['actual_e'])) not in prior}
 rows=[];coverage=set()
 for x in old:
  if x['root']!=5:continue
  d=x['exponent'];es=sorted(e for e in pending if (e==d if x['exact'] else not (e+1)%(d+1)));coverage.update(es)
  if es and set(es)<=exps:rows.append(dict(id=x['id'],d=d,exponents=es))
 return {'input_open_exponents':len(coverage),'exponents':sorted(exps&coverage),'shards':rows}
if __name__=='__main__':
 x=set();
 for fn in sys.argv[1:] or ['TreeAudit.json']:x.update(r['e'] for r in load(H/fn) if r['closed'])
 print(json.dumps(delta(x),indent=1))

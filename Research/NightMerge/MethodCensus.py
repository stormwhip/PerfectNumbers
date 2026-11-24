"""Which method families are independently sufficient for a shard? Standalone counts are not additive; report leave-one-out and exclusive-union synergy."""
from pathlib import Path
import json,gzip,collections
H=Path(__file__).resolve().parent;R=H.parent;D=R.parent;reg=json.load(open(R/'NightMerge/Batches.json'));base=json.load(open(R/'EveningMerge/Audit.json'))['remaining_shards'];groups=collections.defaultdict(set)
def read(f):return json.loads(gzip.decompress(f.read_bytes()) if f.suffix=='.gz' else f.read_bytes())
G=groups['order + finite trees'];G.add((11,306));
for n in reg['order']:G.update((x['p'],x['e']) for x in read(R/'NightOrder'/n))
for n in reg['extra']+reg['pivot']:G.update((x['p'],x['e']) for x in read(R/'NightMerge'/n))
for n in reg['source_nodes']:groups['uniform source and interval'].update((x[0],x[1]) for x in read(R/'NightUniform'/n))
for s,a,es in reg['uniform']:groups['uniform source and interval'].update(map(tuple,es))
for n in reg['three']:groups['root-3 valuation and trees'].update((3,x['e']) for x in read(R/'NightThree'/(n+'.json')))
F=groups['root-5 prices and trees'];
for n in reg['five']+['Batch2.json']+[a for a,b in reg['five_extra']]:
 x=read(R/'NightFive'/n);F.update((5,int(k)) for k in x.get('exponents',x.get('roots',x)))
for n,s in reg['five_chain']:F.add((5,read(R/'NightFive'/n)['e']))
for n in reg.get('five_hybrid',[]):F.update((5,int(k)) for k in read(R/'NightFive'/n)['trees'])
for n in reg.get('five_weighted',[]):F.update((5,x['e']) for x in read(R/'NightFive'/n)['rows'])
seeds={};allkeys={(s['root'],e) for s in base for e in s['remaining_actuals']}
for k,dr in [('five_forest','NightFive'),('seven_forest','NightSevenForest/Release'),('forest','NightLowRoute/Release')]:
 for n in reg.get(k,[]):
    for r in read(R/dr/n)['rows']:seeds.setdefault(r['p'],set()).add(r['e']+1)
FF=groups['static forest, support splits and lifts'];FF.update((p,e) for p,e in allkeys if any((e+1)%v==0 for v in seeds.get(p,())))
for name,p,e in reg['sigma_lift']:FF.add((p,e))
for n in reg['mass']:
 x=read(R/'NightLowRoute/Release'/n);FF.add((x['p'],x['e']))
for k,dr in [('support_forest','NightLowRoute/Release'),('support13_forest','NightLowRoute/Release'),('binary_forest','NightLowRoute/Release'),('seven_split','NightSevenForest/Release')]:
 for n in reg.get(k,[]):FF.update((x['p'],x['e']) for x in read(R/dr/n)['rows'])
def complete(keys):return {x['id'] for x in base if all((x['root'],e)in keys for e in x['remaining_actuals'])}
full=set.union(*groups.values())&allkeys;total=complete(full);arch=read(R/'NightMerge/Audit.json');assert full==set(map(tuple,arch['new_actuals'])) and len(total)==arch['new_shards'];report={};
for name,pairs in groups.items():
    other=set.union(*(v for k,v in groups.items() if k!=name));single=complete(pairs);without=complete(other);report[name]=dict(actuals=len(pairs&allkeys),standalone_shards=len(single),unique_actuals=len((pairs-other)&allkeys),shards_lost_if_omitted=len(total-without))
report['combined']=dict(actuals=len(full),shards=len(total),synergy_only=len(total-set.union(*(complete(x) for x in groups.values()))));print(json.dumps(report,indent=1))

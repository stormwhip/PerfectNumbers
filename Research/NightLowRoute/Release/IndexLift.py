"""Prove anchor once; σ(p^e)|σ(p^f) whenever e+1|f+1. Map all exact actuals by set union. Does NOT lift unrelated search trees or external-terminal constraints. See IndexLift.md."""
from pathlib import Path
import argparse,gzip,hashlib,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ForestReplay import proof,B,check,sigma
BASE_SHA='5c7455f8a2bbe24e5dcc2e85efbf2ac0aa4466f7507a5005285ebaf321c0c393';BASE=H.parents[1]/'EveningMerge/Audit.json'
def closure(anchors,universe):return {(p,f) for p,f in universe if any(p==q and (f+1)%(e+1)==0 for q,e in anchors)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('packets',nargs='+');ap.add_argument('--output',type=Path);args=ap.parse_args();check(hashlib.sha256(BASE.read_bytes()).hexdigest()==BASE_SHA,'unrecognized 880 ledger');L=json.loads(BASE.read_text())['remaining_shards'];U={(s['root'],f) for s in L for f in s['remaining_actuals']};seeds=set()
 for name in args.packets:
  file=Path(name);file=file if file.is_file() else H/file;d=json.loads(gzip.decompress(file.read_bytes()));check(isinstance(d['rows'],list) and d['rows'],'empty packet')
  for row in d['rows']:
   check('extra' not in row,'do not lift terminal disjunction');p=row['p'];e=row['e'];k=p,e;check(e%2==0 and e>=2,'ordinary anchor');
   if k in seeds:continue
   low=min(proof(row,d['ecpp']).values());check(low>B**row.get('den',1),'open anchor');seeds.add(k)
 out=closure(seeds,U);alt=out-seeds;shards=[s['id'] for s in L if s['remaining_actuals'] and all((s['root'],e) in out for e in s['remaining_actuals'])];d=dict(anchors=sorted(seeds),actuals=sorted(out),lift_only=sorted(alt),whole=shards);print('seed',len(seeds),'baseline-covered',len(out),'lift-only',len(alt),'whole-880',len(shards));
 if args.output:args.output.write_text(json.dumps(d,separators=(',',':'))+'\n')
 else:print(json.dumps(d,separators=(',',':')))
if __name__=='__main__':main()

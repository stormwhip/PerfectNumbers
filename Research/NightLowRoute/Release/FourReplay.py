"""First-root 13, N<=10^2400. Recheck the five-hitting theorem and four-avoider exponent whitelist; then two certified auxiliary-root forests. Not applicable inside the whitelist."""
from pathlib import Path
import subprocess,json,sys,gzip
H=Path(__file__).resolve().parent;S=H.parents[1]/'NightUniform';sys.path.insert(0,str(H));from ForestReplay import proof,B,check

def replay(name,packet):
 cp=subprocess.run([sys.executable,'-I','-S','-B',str(S/name),str(S/packet)],stdout=subprocess.PIPE,check=True,text=True);return json.loads(cp.stdout.strip().splitlines()[-1])
if __name__=='__main__':
 five=replay('RoughTerminalWitness.py','FiveAvoid.json');check(any(sorted(s['forbidden'])==[3,5,7,11,13] and s['micro_floor']>=2400000000 for s in five['certificates']),'five witness');four=replay('FourTailWitness.py','Four13Partition.json');exc=set(json.loads((S/'Four13Partition.json').read_text())['survivors']);check(four['root']==13 and sorted(four['forbidden'])==[3,5,7,11] and four['remaining']==len(exc),'four scope');print('verified both terminal prerequisites; exceptional exponents',len(exc),flush=True)
 for arg in sys.argv[1:]:
  f=Path(arg);f=f if f.is_file() else H/arg;d=json.loads(gzip.decompress(f.read_bytes()));rs=d['rows'];check(len(rs)==2 and {r['extra'] for r in rs}=={3,5} and len({r['e'] for r in rs})==1 and all(r['p']==13 and r['e'] not in exc and r.get('den',1)==1 for r in rs),'incomplete or out-of-scope cover');vals=[]
  for r in rs:
   m=min(proof(r,d['ecpp'],forced=r['extra']).values());check(m>B,'open');vals.append([r['extra'],len(str(m))-1]);
  print(13,rs[0]['e'],vals,flush=True)

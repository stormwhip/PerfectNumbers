"""Close all three branches, then attach the exact terminal six-prime certificate. Without that prerequisite these are conditional results ONLY."""
from pathlib import Path
import subprocess,json,sys,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ForestReplay import proof,B,check
if __name__=='__main__':
 S=H.parents[1]/'NightUniform';z=subprocess.run([sys.executable,'-I','-S','-B',str(S/'TerminalSixWitness.py'),str(S/'SixClasses.json')],stdout=subprocess.PIPE,text=True,check=True);v=json.loads(z.stdout.strip().splitlines()[-1]);check(any(sorted(r['forbidden'])==[3,5,7,11,13,19] and r['micro_floor']>=2400000000 for r in v),'missing terminal class');print('terminal six verified',flush=True)
 for s in sys.argv[1:]:
  f=Path(s);f=f if f.is_file() else H/s;d=json.loads(gzip.decompress(f.read_bytes()));rows=d['rows'];check(len(rows)==3 and {r['extra'] for r in rows}=={3,5,13} and len({r['e'] for r in rows})==1 and all(r['p']==31 for r in rows),'invalid cover');infos=[]
  for r in rows:
   m=min(proof(r,d['ecpp'],forced=r['extra']).values());check(m>B,'open branch');infos.append([r['extra'],len(str(m))-1]);
  print(31,rows[0]['e'],infos,flush=True)

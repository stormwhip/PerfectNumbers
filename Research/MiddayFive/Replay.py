"""Release entry. --audit reconstructs the model with a separate implementation.
No SciPy/SymPy, private archives, PARI, networking or working-directory inputs.
"""
import argparse,sys,gzip,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));P=argparse.ArgumentParser(description=__doc__);P.add_argument('--audit',action='store_true');P.add_argument('es',nargs='*',type=int)
def main():
 if not __debug__:raise SystemExit('run without -O')
 a=P.parse_args();frontier=json.loads((H.parent/'Nov25/Delta.json').read_bytes());es={e for r in frontier['remaining_shards'] if r['root']==5 for e in r['remaining_actuals']};rows=json.loads(gzip.decompress((H/'Accepted.json.gz').read_bytes()));assert len(es)==len(rows)==14 and {r['e'] for r in rows}==es;targets=set(a.es) if a.es else es;assert targets<=es;accepted=[]
 if a.audit:
  from Audit import replay,logs as lg,W
 else:
  from Spur import extend
  from Joint import model,weighted,lg,W
 for d in rows:
  e,L,cut,cap,w=[d[k] for k in ('e','L','cut','cap','w')]
  if e not in targets:continue
  assert type(L)==type(cap)==type(cut)==int and 1001<=L<=20001 and 1<=cut<=cap<=256
  if a.audit:v=replay(e,[],[],L,cut,cap,w,True)[0]
  else:extend(e);v=weighted(model(e,(),L,cut,cap,(),True),w)
  assert v>2400*W*lg(10)[1];accepted.append(e);print(('INDEPENDENT' if a.audit else 'PRIMARY'),'EXCLUDED',5,e,'floor',v//(W*lg(10)[1]),flush=True)
 assert set(accepted)==targets
 return accepted
if __name__=='__main__':main()

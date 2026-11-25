"""Validate conditional forest portfolio: finite exact forced prime powers
and final tail. Separate graphs can use different private owners per case.
Standard-library verifier; calls independent checkfile with explicit selectors.
"""
import json,gzip,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Forest import *
def verify(path):
 x=json.loads(gzip.decompress(Path(path).read_bytes()));e=x['e'];q=x['pivot'];u=x['tail'];K=x['cases'];assert type(q)==int and type(u)==int and 1<u<=100
 req={f for f in range(1,u) if legal(q,f) and (f%2==0 or (q%4==1 and f%4==1))};check(set(K)=={str(j) for j in req}|{'tail'},'case coverage');res={}
 for label,p in K.items():
  row=p['row'];check(row['e']==e and q in row['roots'],'wrong pivot');c=(q,'ge',u) if label=='tail' else (q,'eq',int(label));n=measure(row,x['ecpp'],case=c)[0];res[label]=len(str(n))-1;check(n>B,'unclosed case')
 print('PASS PORTFOLIO',e,'pivot',q,'floor',min(res.values()),'cases',res,flush=True);return e
if __name__=='__main__':
 for f in sys.argv[1:]:verify(f)

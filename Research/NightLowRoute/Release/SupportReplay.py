"""Unconditional q|N OR q∤N complement. Distinct forests but same first p, e and q. This is not the externally conditioned Four/Six proof. Standard positive masks promote q to a root; negative masks forbid every actual sigma from containing q. No precomputed coverage needed."""
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ForestReplay import proof,B,check,R
if __name__=='__main__':
 for a in sys.argv[1:]:
  f=Path(a);f=f if f.is_file() else H/a;d=json.loads(gzip.decompress(f.read_bytes()));pos,neg=d['rows'];q=d['split'];check(type(q)==int and q in (3,5,7,11,13,17,19,23,29,31) and q!=pos['p'] and q not in R[:R.index(pos['p'])],'invalid binary split');k=pos['p'],pos['e'];check((neg['p'],neg['e'])==k and all(row.get('den',1)==1 for row in (pos,neg)),'inconsistent split');
  a=min(proof(pos,d['ecpp'],support=(q,True)).values());b=min(proof(neg,d['ecpp'],support=(q,False)).values());check(min(a,b)>B,'unclosed');print(*k,'q',q,'present/absent lower logs',len(str(a))-1,len(str(b))-1,flush=True)

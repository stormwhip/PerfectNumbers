"""Independent complete finite-cover replay, alternate primality/forest routines."""
from pathlib import Path
from math import gcd
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from IndependentForest import checkdata,must,geom,BAN

def replay(path):
 x=json.loads(gzip.decompress(Path(path).read_bytes()));must(set(x)=={'e','pivot','tail','cases','ecpp'},'packet fields');e=x['e'];q=x['pivot'];tail=x['tail'];table=x['cases'];must(all(type(t)==int for t in [e,q,tail]) and 1<tail<200 and q>3 and e>0 and e%2==0,'parameters');must(geom(3,e)%q==0,'pivot is not forced');todo=['tail'];used=set();vals={}
 for f in range(1,tail):
  if f%2 and (q%4!=1 or f%4!=1):continue
  if gcd(geom(q,f),BAN)>1:continue
  todo.append(str(f))
 must(set(table)==set(todo),'lost/extra finite case')
 for tag in todo:
  r=table[tag]['row'];must(r['e']==e and q in r['roots'],'wrong conditional root');V=set(r['roots'])|set(dict(r['edges']));c={str(z):x['ecpp'][str(z)] for z in V if z>=2**64};used.update(c);sel=(q,'ge',tail) if tag=='tail' else (q,'eq',int(tag));vals[tag]=checkdata(dict(row=r,ecpp=c),select=sel)
 must(set(x['ecpp'])==used,'orphan prime witness');print('PASS complete pivot',e,'min',len(str(min(vals.values())))-1,'branches',[(k,len(str(v))-1) for k,v in vals.items()]);return min(vals.values())
if __name__=='__main__':
 for f in sys.argv[1:]:replay(f)

"""Independent replay of recursively covered private forests. Each split prime
must divide root sigma unconditionally; leaves validate exact hypotheses and
recompute both integer DPs with their separate prime/elliptic implementations.
"""
from pathlib import Path
import sys,json,gzip,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Forest import measure,sg,B,check
from IndependentForest import checkdata,geom,BAN

def replay(path):
 x=json.loads(gzip.decompress(Path(path).read_bytes()));e=x['e'];A=sg(3,e);rows=x['rows'];cs=x['ecpp'];used=set();seen=set();lows=[]
 def visit(node,sel):
  if type(node)==int:
   seen.add(node);row=rows[node];check(row['e']==e and set(sel)<=set(row['roots']),'missing forced prime');local={str(z):cs[str(z)] for z in set(row['roots'])|set(dict(row['edges'])) if z>=2**64};used.update(local);n=checkdata(dict(row=row,ecpp=local),select=sel);m=measure(row,local,case=sel)[0];check(m==n and n>B,'different costs');lows.append(n);return
  z,t,sub=node['q'],node['tail'],node['children'];check(z>3 and A%z==0 and z not in sel and 1<=t<=200,'split');fs={str(f) for f in range(1,t) if (not f%2 or (z%4==1 and f%4==1)) and math.gcd(geom(z,f),BAN)==1};check(set(sub)==fs|{'tail'},'coverage')
  for tag,child in sub.items():visit(child,{**sel,z:(('ge',t) if tag=='tail' else ('eq',int(tag)))})
 visit(x['tree'],{});check(seen==set(range(len(rows))) and used==set(cs),'orphan certificate');print('PASS nested',e,'leaves',len(lows),'graphs',len(rows),'min',len(str(min(lows)))-1);return min(lows)
if __name__=='__main__':
 for p in sys.argv[1:]:replay(p)

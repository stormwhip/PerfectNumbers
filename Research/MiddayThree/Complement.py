"""Offline exact complementary-anchor audit; leaves explicitly omitted exponents
UNPROVED. A matching external exact-component certificate is needed for each.
Uses independent ECPP/forest DP and original DP, requiring identical integers.
"""
from pathlib import Path
import sys,json,gzip,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Forest import measure,check,B,sg;from IndependentForest import checkdata,geom,BAN

def audit(path):
 x=json.loads(gzip.decompress(Path(path).read_bytes()));e=x['e'];q=x['pivot'];t=x['tail'];omit=x['omitted'];need={j for j in range(1,t) if (j%2==0 or (q%4==1 and j%4==1)) and math.gcd(geom(q,j),BAN)==1};check(omit and len(set(omit))==len(omit) and set(omit)<=need and sg(3,e)%q==0,'coverage inputs');keys={str(f) for f in need-set(omit)}|{'tail'};check(keys==set(x['cases']),'missing represented case');used=set();vals={}
 for key,i in x['cases'].items():
  r=x['rows'][i];check(r['e']==e and q in r['roots'],'forced root binding');V=set(r['roots'])|set(dict(r['edges']));cs={str(z):x['ecpp'][str(z)] for z in V if z>=2**64};used.update(cs);sel=(q,'ge',t) if key=='tail' else (q,'eq',int(key));m=measure(r,cs,case=sel)[0];n=checkdata(dict(row=r,ecpp=cs),select=sel);check(m==n and m>B,'unproved cell');vals[key]=len(str(m))-1
 check(used==set(x['ecpp']) and set(x['cases'].values())==set(range(len(x['rows']))),'unused witnesses');print('PASS complementary cases ONLY',e,'except',omit,vals,flush=True);return e,q,set(omit),min(vals.values())
if __name__=='__main__':
 for p in sys.argv[1:]:audit(p)

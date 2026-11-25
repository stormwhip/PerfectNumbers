"""Independent finite-exception certificate for the canonical 31^10, 3|N, 5 ∤ N cell."""
from pathlib import Path
import sys,gzip,json,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Independent31 import replay,sig,req,valuation,prime64
q=150332843;x=json.loads(gzip.decompress((H/'Only3.json.gz').read_bytes()));req((x['p'],x['e'],x['pivot'],x['cut'],x['present'],x['absent'],x['exceptions'])==(31,10,q,100,[3],[5],[40,52]),'scope');D=sig(31,10);req(prime64(q) and not D%q and q%4==3,'pivot');legal={str(f) for f in range(2,101,2) if f>=valuation(D,q) and math.gcd(sig(q,f),19*7*11*5)==1};req(set(x['leaves'])==(legal-{'40','52'})|{'tail'},'coverage');scores={}
for f,u in x['leaves'].items():
 A=[[31,10]]+([] if f=='tail' else [[q,int(f)]]);K=set(u['roots'])|dict(u['owners']).keys();cs={str(z):x['ecpp'][str(z)] for z in K if z>=2**64};scores[f]=replay(dict(assigned=A,present=[3],absent=[5],leaf=u,ecpp=cs),{q:101} if f=='tail' else {})
print('ONLY3 31x10',len(scores),'forests; exceptions [40,52]; minimum',min(scores.values()),'tail',scores['tail'])

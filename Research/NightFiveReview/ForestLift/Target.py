"""Standalone entry for portable partial forest rows and odd-root-quotient lifting.
Relies only on the original checked forest arithmetic and standard library.
Without arguments proves target 31/242 from an insufficient 31/80 row.
Optional --ledger prints all hits in the baseline and current open ledger.
"""
from pathlib import Path
import argparse,gzip,math,sys,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'NightLowRoute/Release'));from ForestReplay import B,proof

def certify(r,cs,targets):
 p,e0=r['p'],r['e'];D=r.get('den',1);U=math.prod(set(r['roots'])|set(dict(r['owners'])));rho=dict(r.get('rho',[]));m=min(proof(r,cs).values());out=[]
 for e in targets:
  if e<e0 or (e+1)%(e0+1):continue
  v,a=divmod(p**(e+1)-1,p**(e0+1)-1)
  if a:raise ValueError('noninteger ratio')
  v//=v&-v;price=1
  for q,k in rho.items():
   while not v%q:v//=q;price*=q**k
  while (g:=math.gcd(v,U))>1:v//=g
  size=m*p**(D*(e-e0));P=size*v**D*price
  if P>B**D:out.append((e,fl(m,D),fl(size,D),fl(P,D)))
 return out

def fl(v,D):
 a=0;b=v.bit_length()+1
 while b-a>1:
  c=(b+a)//2
  if 10**(c*D)<=v:a=c
  else:b=c
 return a
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('pack',nargs='?',default='Fraction31.json.gz');ap.add_argument('--ledger',type=Path);opts=ap.parse_args();j=json.loads(gzip.decompress((O/opts.pack).read_bytes()));ledger=json.loads(opts.ledger.read_bytes())['remaining_shards'] if opts.ledger else None
 for r in j['rows']:
  p=r['p'];es=sorted({e for s in ledger if s['root']==p for e in s['remaining_actuals']}) if ledger is not None else [242];out=certify(r,j['ecpp'],es);print(p,r['e'],out,flush=True)
  if ledger is None and (p!=31 or r['e']!=80 or 242 not in {x[0] for x in out}):raise ValueError('failed precise claim')

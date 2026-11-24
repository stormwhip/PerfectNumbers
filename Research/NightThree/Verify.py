"""Offline release verifier; no upstream checkout or PARI required. python -I -S -B Verify.py Batch1"""
import argparse,sys,json,gzip,math
from pathlib import Path
from functools import cache
from hashlib import sha256
from itertools import accumulate
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(H));sys.path.insert(0,str(R/'ThreeChainNext'));import Replay as E;import Joint as J
B=J.B;I=J.I

def require(v,w):
 if not v:raise ValueError(w)

def independent(e,fs,ee,windows,boost=False):
 pe=3**e;A=(3*pe-1)//2;ban=math.prod(I.BAN);basic={z for z in I.PS if 3<z<=1999 and z not in I.BAN};P0=[(z,2) for z in I.SUP if z*z<=4000000];prices=sorted(z**d for z,d in P0 if I.legal(z,d)); stats={'nodes':0,'depth':0,'floor':0,'source':0,'internal':0,'sigma':0,'branch':0}
 # Additional repeated marginal prices (r^6 may fall below cap). For min allowed supplier r>=37, even r^6 > 4e6; check rather than assume.
 require(min(z for z,d in P0)**6>4000000,'short price list')
 def walk(ex,active):
  stats['nodes']+=1;stats['depth']=max(stats['depth'],len(ex)-1);require(stats['nodes']<=50000 and len(ex)<=70,'safety budget');X=math.prod(z**f for z,f in ex);src=[E.sigma(z,f) for z,f in ex];S=math.prod(src);D=S//math.gcd(S,2*X)
  if math.gcd(D,X*ban)>1 or X*D>B or S>2*X:stats['sigma']+=1;return True
  pool=set(fs)|basic
  for k in ex:pool.update(ee.get(k,()))
  U=D;floor={};charges=prices.copy();free=0;M=X
  for r in pool:
   if U%r:continue
   c=0
   while U%r==0:c+=1;U//=r
   f=E.lower(r,c,False);floor[r]=(c,f);M*=r**f
   if r%3!=1:continue
   j=E.ilog(f+1,3);free+=j;g=3**(j+1)-1
   while E.legal(r,g):
    val=r**(g-f)
    if val>4000000:break
    charges.append(val);f=g;g=3*(g+1)-1
  M*=U; free+=E.ilog(U,4000000);charges.extend([2000]*E.ilog(U,2000));charges.extend([4000000]*e);cost=[1,*accumulate(sorted(charges)[:e],lambda a,b:a*b)];need=e-E.val(S,3);live=[]
  for s in active:
   if need<s:continue
   y=3**s;Q=2*y-1
   for r,(c,f) in floor.items():
    if r%4==1 and c==1 and r>=Q and (r+1)%y==0:raise ValueError('feasible forced Euler')
   # Exclude q | U using individual origin sigmas, not a factorization of U. The root cannot source q by reciprocity. Every non-root component here is exact and even.
   if U//Q>=(-U%y or y):
    for sig in src[1:]:
     v=math.gcd(sig,U)
     if v//Q>=(-v%y or y):raise ValueError('unresolved internal Euler')
   c=cost[max(0,need-s-free)];v=M*c
   if v*Q>B:stats['floor']+=1;continue
   if 8*pe*Q**4>=27*B and 2*v*Q**2>=3*B*max([U]+[r**f for r,(_,f) in floor.items()]):stats['source']+=1;continue
   if boost and 8*pe*Q**4>=27*B and 2*v*Q**2>=3*B:
    # Divide U into coprime blocks via gcd with powers of each sigma. Refining gcd(u,sigma) to its full supported part by repeated squaring works without primality assumptions.
    cells=[U] if U>1 else []
    for orig in src:
     new=[]
     for w in cells:
      part=math.gcd(w,orig)
      while part not in (1,w):
       n=math.gcd(w,part**2)
       if n==part:break
       part=n
      if part>1:new.append(part)
      if w//part>1:new.append(w//part)
     cells=new
    require(math.prod(cells)==U,'support split');rhs=B*max(3*pe,Q)*((3*pe)//y+4);lhs=v*Q*Q*y
    skip=all(2*v*Q**2>=3*B*w or (math.gcd(w,A)>1 and lhs>=rhs*(w//math.gcd(w,A))) for w in cells)
    if skip:
     for z,(c,mf) in floor.items():
      if 2*v*Q**2>=3*B*z**mf:continue
      cA=E.val(A,z)
      if cA>0 and lhs>=rhs*z**(mf-cA):continue
      mult=1;g=mf
      while v*Q*mult<=B:
       if (g+1)%3 and E.legal(z,g):
        sig=E.sigma(z,g); residue=-sig%y or y
        if (sig//Q)>=residue:break
       mult*=z*z;g+=2
      if v*Q*mult<=B:skip=False;break
    if skip:stats['internal']+=1;continue
   live.append(s)
  if not live:return True
  if not floor:return False
  r=max(floor);c,m=floor[r];upper=B//((2*3**min(live)-1)*(M//r**m));f=m
  while r**f<=upper:
   if E.legal(r,f) and not walk(ex+[(r,f)],live):return False
   f+=2
  stats['branch']+=1;return True
 require(walk([(3,e)],windows),'unclosed tree e='+str(e));return stats

def main():
 if not __debug__:raise SystemExit('requires assertions enabled')
 p=argparse.ArgumentParser();p.add_argument('batch',nargs='?',default='Batch1');a=p.parse_args();rows=json.loads((H/(a.batch+'.json')).read_text());cert=json.loads(gzip.decompress((H/(a.batch+'ECPP.json.gz')).read_bytes()));es=[];summary=[];baseline={e for s in J.base() for e in s['remaining_actuals']}
 @cache
 def prime(r):
  if r<2**64:return E.mr(r)
  n=r
  for row in cert[sha256(str(r).encode()).hexdigest()[:24]]:
   require(row[0]==n,'ECPP subject');n=E.elliptic(*row)
  return E.mr(n)
 for row in rows:
  e=row['e'];require(type(e)==int and e in baseline and e not in es,'not unique/open');fs=list(map(int,row['root']));require(len(set(fs))==len(fs) and all(r>3 and E.sigma(3,e)%r==0 and prime(r) for r in fs),'bad root');edges={}
  for x,m,y in row['edges']:
   x,y=int(x),int(y);require(x>3 and y>3 and type(m)==int and m>0 and pow(x,m+1,y*(x-1))==1 and prime(y),'invalid edge');edges.setdefault((x,m),set()).add(y)
  one,hi=J.audit(e,fs);require(not hi and all(s>0 for s in one),'high Euler or zero branch remains');st=independent(e,fs,edges,one,boost=row.get('boost',False)) if one else {};es.append(e);summary.append(dict(e=e,windows=len(one),stats=st));print('ACCEPT',summary[-1],flush=True)
 print('actuals',sorted(es),'complete shards',J.delta(es),'baseline 880 ->',880-len(J.delta(es)))
if __name__=='__main__':main()

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

@cache
def emax():return E.ilog(B,5)
@cache
def high_floor(s):
 # Require s>7 globally, hence q=-1 mod3 and j=v3(a+1)<=7. For a fixed j, any a>=5 with a=1 mod4 has a minimal such value. A lower bound on its q^a uses CRT q>=2*3^(s-j)-1.
 require(s>7,'short high cell');vals=[B+1]
 for j in range(8):
  a=5
  while E.val(a+1,3)!=j:a+=4
  if 5**a>B:continue
  q=2*3**(s-j)-1
  if (q.bit_length()-1)*a>B.bit_length():continue
  vals.append(q**a)
 return min(vals)

def independent(e,fs,ee,windows,boost=False,reduced=False,parity=False,internal=False,exception=False,high=False):
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
  def support():
   cells=[U] if U>1 else []
   for orig in src:
    temp=[]
    for v in cells:
     g=math.gcd(v,orig)
     while g not in (1,v):
      j=math.gcd(g*g,v)
      if j==g:break
      g=j
     if g>1:temp.append(g)
     if v//g>1:temp.append(v//g)
    cells=temp
   require(math.prod(cells)==U,'parity partition');return cells
  cells_for_parity=support() if parity else [];odd=sum(math.isqrt(v)**2!=v for v in cells_for_parity)
  checks=src[1:]
  if reduced:
   checks=[]
   for z,g in ex[1:]:
    n=g+1
    while n%3==0:n//=3
    # Factor sigma(z^(n-1)) exactly as product of cyclotomics.
    phi={}
    for d in range(1,n+1):
     if n%d:continue
     phi[d]=(z**d-1)//math.prod(v for h,v in phi.items() if d%h==0)
    require(math.prod(v for d,v in phi.items() if d>1)==E.sigma(z,n-1),'bad reduced indices');checks.extend(v for d,v in phi.items() if d>1)
  rough_internal=False
  def finite(n,y,lower,upper):
   if upper<lower:return False
   mod=4*y;res=2*y-1; qa=lower+(res-lower)%mod; qb=upper-(upper-res)%mod
   if qa>qb:return False
   # Since (2Y-1)^2=1 mod 4Y, same residue is its own inverse.
   wmin=(n+qb-1)//qb;wmax=n//qa;wr=n*res%mod;wmin+=(wr-wmin)%mod;wmax-=(wmax-wr)%mod
   if wmax<wmin:return False
   if wmax-wmin<=400*mod:return any(n%w==0 and (n//w)%mod==res for w in range(wmin,wmax+1,mod))
   if qb-qa<=400*mod:return any(n%q==0 for q in range(qa,qb+1,mod))
   return True
  for s in active:
   if need<s:continue
   if high:
    require(s>7 and 3**8>1+emax(),'unrestricted internal high Euler');q0=2*3**(s-7)-1;j=min(7,E.ilog(1+E.ilog(B//X,q0),3)) if internal else 7;y=3**(s-j);Q=2*y-1
    require(not any(r%4==1 and (r+1)%y==0 for r in floor),'known high Euler not external');inside=U//Q>=(-U%y or y) and any((w:=math.gcd(U,sg))//Q>=(-w%y or y) for sg in checks)
    if inside:
     require(internal,'rough high Euler not external')
     if M*cost[max(0,need-s-free)]*high_floor(s)>B*U:stats['floor']+=1;continue
     rough_internal=True;live.append(s);continue
    if M*cost[max(0,need-s-free)]*high_floor(s)>B:stats['floor']+=1;continue
    live.append(s);continue
   y=3**s;Q=2*y-1
   for r,(c,f) in floor.items():
    if r%4==1 and c==1 and r>=Q and (r+1)%y==0:raise ValueError('feasible forced Euler')
   # Exclude q | U using individual origin sigmas, not a factorization of U. The root cannot source q by reciprocity. Every non-root component here is exact and even.
   c=cost[max(0,need-s-free)];v=M*c
   inside=False
   if U//Q>=(-U%y or y):
    for sg in checks:
     w=math.gcd(sg,U)
     if finite(w,y,Q,w) if exception else w//Q>=(-w%y or y):inside=True;break
   if inside:
    if reduced and v>B:stats['floor']+=1;continue
    if internal:rough_internal=True;live.append(s);continue
    raise ValueError('unresolved internal Euler')
   parity_charge=2000**odd*cost[max(0,need-s-free-odd)] if odd else c
   if M*max(c,parity_charge)*Q>B:stats['floor']+=1;continue
   if odd:v=M*max(c,parity_charge//2000)
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
        if (sig//Q)>=residue and (not exception or finite(sig,y,Q,B//(v*mult))):break
       mult*=z*z;g+=2
      if v*Q*mult<=B:skip=False;break
    if skip:stats['internal']+=1;continue
   live.append(s)
  if not live:return True
  if not floor:return False
  r=max(floor);c,m=floor[r];upper=B//((1 if rough_internal else (min(high_floor(s) for s in live) if high else 2*3**min(live)-1))*(M//r**m));f=m
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
  if row.get('pivots'):
   from PivotReplay import check
   st=check(row);es.append(e);print('ACCEPT PIVOTS',e,st,flush=True);continue
  if row.get('generic'):
   # Exact baseline solver enumerates Euler and ordinary powers itself; the only substituted function is its prime oracle, backed by the packet ECPP and deterministic MR already checked above.
   old=E.proven;E.proven=prime
   try:st=E.replay(row,cap=160000)
   finally:E.proven=old
   es.append(e);print('ACCEPT GENERIC',st,flush=True);continue
  one,hi=J.audit(e,fs);require(all(s>0 for s in one),'zero branch remains');highstats=independent(e,fs,edges,hi,reduced=True,high=True,internal=row.get('internal',False)) if hi else {}
  partitions=row.get('windows',[one]);require(isinstance(partitions,list) and sorted(v for w in partitions for v in w)==sorted(one),'incomplete or duplicate Euler-one subwindow');stlist=[independent(e,fs,edges,w,boost=row.get('boost',False),reduced=row.get('reduced',False),parity=row.get('parity',False),internal=row.get('internal',False),exception=row.get('exception',False)) for w in partitions if w];st=stlist[0] if len(stlist)==1 else stlist;es.append(e);summary.append(dict(e=e,windows=len(one),stats=st,high=highstats));print('ACCEPT',summary[-1],flush=True)
 print('actuals',sorted(es),'complete shards',J.delta(es),'baseline 880 ->',880-len(J.delta(es)))
if __name__=='__main__':main()

"""Standalone exhaustive factor-chain replay; no import of CutTree or TreeProof.
The finite budget is an upper bound, not an exponent cutoff. Only complete trees pass.
Use the official exact/shard ledgers AND the former upstream root screen for novelty.
"""
import argparse
from bisect import bisect_right
from collections import Counter
import csv
from functools import cache
from hashlib import sha256
import json
from math import gcd, lcm, prod, isqrt
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
R=H.parent
B=10**2400
ORDER=(19,7,11,31,13,3,5,17)

def read(path): return json.loads(path.read_text(encoding='utf8'))
def need(ok,msg):
    if not ok: raise ValueError(msg)

sys.path.insert(0,str(R/'RootFiveNext'))
sys.path.insert(0,str(R/'TeichmullerValuation'))
import PrimeCheck as ec
ECPP_FILES=set()

@cache
def prime(n):
    if n<2**64: return ec.prime64(n)
    name='Prime'+sha256(str(n).encode('ascii')).hexdigest()[:24]+'.json'
    for directory in (H/'ECPP', R/'OrderSupplyNext/certs', R/'EveningRoot3/ECPP', R/'RootFiveNext/ECPP'):
        path=directory/name
        if path.is_file():
            t=n
            for row in read(path):
                need(t==row[0], 'ECPP subject mismatch'); t=ec.level(*row)
            if not ec.prime64(t):return False
            ECPP_FILES.add(path.relative_to(R).as_posix());return True
    return False

flags=bytearray([1])*20001
for d in range(2,isqrt(20000)+1):
    if flags[d]: flags[d*d::d]=bytes(len(flags[d*d::d]))
PS=tuple(i for i in range(3,20001,2) if flags[i]); SMALL={p for p in PS if p<5000}

def sigma(z,f): return (z**(f+1)-1)//(z-1)

# For each absent prime b derive a forbidden divisor of f+1 by order,
# without testing the geometric series by the originator's modular formula.
@cache
def forbidden_indices(z,ban):
    out=set()
    for b in ban:
        t=z%b
        if t==0: continue
        if t==1: out.add(b);continue
        d=1;w=t
        while w!=1: d+=1;w=w*t%b
        out.add(d)
    return tuple(sorted(out))

def permissible(f,ds):return all((f+1)%d for d in ds)

@cache
def least(z,c,ds,euler):
    if euler:
        if z%4!=1 or 2 in ds: return None
        f=c+(1-c)%4;step=4
    else: f=c+c%2;step=2
    while not permissible(f,ds):f+=step
    return f

@cache
def allowance(p,t,euler_used):
    # For k fresh distinct primes, one may be Euler unless already used.
    # Minimal size with one exception attained with the exception LAST.
    # Each z/(z-1) decreases. Duplication of mandatory/assigned primes here
    # is deliberate (enlarges the upper bound, shrinks the cost).
    sizes=[1]; nums=[1]; dens=[1]; pair=1
    for z in PS:
        if z<=t or z in ORDER[:ORDER.index(p)+1]: continue
        pair*=z*z; lower=pair if euler_used else pair//z
        if lower>B:break
        sizes.append(lower);nums.append(nums[-1]*z);dens.append(dens[-1]*(z-1))
    else: raise RuntimeError('expand tail sieve')
    return sizes,nums,dens

from fractions import Fraction

def vp(n,p):
    b=0
    while n%p==0: b+=1;n//=p
    return b

@cache
def sale(p,k,z,m):
    # For every even f>=m take z^f / p^(k*v_p(sigma(z^f))). Independent
    # brute exponent loop with monotone lower bounding tail. LTE at order o
    # gives v_p(sigma)<=t+v_p(f+1)<=t+log_p(f+1).
    o=1
    while pow(z,o,p)!=1:o+=1
    if o%2==0:return z**m
    t=0 if o==1 else vp(z**o-1,p)
    best=None; f=m
    while True:
        v=t+vp(f+1,p) if (f+1)%o==0 else 0
        num=z**f;w=Fraction(num,p**(k*v)); best=w if best is None else min(best,w)
        # z^f/(f+1)^k increases from f>=k, as (1+1/(k+1))^k<e<3<=z.
        if f>=k and num>=best*p**(k*t)*(f+1)**k: return max(1,best)
        f+=2

@cache
def global_discounts(p,e):
    # Use ONLY the upstream profile of exceptional Teichmueller primes and
    # the published high-Euler discount, never the candidate's node logic.
    import VerifyTeichmullerValuation2400 as tb
    import VerifyGeminiExponents2400 as g
    prof=old_profile(p)
    return tb.kappa(p),prof.U(e),max([1]+[d for t,d in g.euler_deficits(p,e) if t<=e])

@cache
def old_profile(p):
    import VerifyTeichmullerValuation2400 as tb
    return tb.Profile(p)

class Proof:
    def __init__(self,p,e,fs,cut,valuation=False):
        self.p,self.e=p,e;self.pr=sorted(set(fs)|SMALL);self.cut=cut;self.valuation=valuation;self.stats=Counter()

    def valuation_close(self,X,S,U,base,blocks,used):
        p,e=self.p,self.e; k,disc,delta=global_discounts(p,e)
        remaining=e-vp(S,p)
        if remaining<0:return True
        prices={z:sale(p,k,z,m) for z,(_,m,a,ds) in blocks.items()}
        charge=Fraction(X*p**(k*remaining)*prod(prices.values()),disc)
        # If Euler is already known, every unassigned forced prime is even.
        if used:return charge>B
        elig={z for z,(_,m,a,ds) in blocks.items() if a is not None}
        if charge<=B*delta*max([1]+[prices[z] for z in elig]): return False
        # Try each feasible forced Euler prime of exponent exactly one.
        for z in elig:
            c,m,a,ds=blocks[z];s=vp(z+1,p)
            if c==1 and s<=remaining and base//z**(m-1)<=B and charge*z<=B*prices[z]*p**(k*s):return False
        # Otherwise q is either absent from D or divides its rough part U.
        for s in range(remaining+1):
            y=p**s;lo=max(5,2*y-1);hi=(B*p**(k*s))//charge
            if lo>hi:continue
            if base*lo<=B:return False
            if base>B or U<lo:continue
            # From U=q*c, q=-1 mod y, c=-U mod y. Positive c and q
            # imply ceil(U/hi)<=c<=floor(U/lo); test this entire interval.
            cmin=(U+hi-1)//hi;cmax=U//lo
            if cmin+(-U-cmin)%y<=cmax:return False
        return True
    def prove(self):
        p,e=self.p,self.e
        return self.visit(((p,e),),p**e,sigma(p,e),frozenset(ORDER[:ORDER.index(p)]))
    def visit(self,parts,X,S,ban):
        self.stats['nodes']+=1
        if self.stats['nodes']>10000: return False
        used=any(f%2 for z,f in parts)
        # lcm is the portion of N already forced by exact assigned parts and sigma.
        L=lcm(X,S//gcd(2,S));D=L//X;zs={z for z,f in parts}
        if any(D%z==0 for z in zs) or any(D%z==0 for z in ban) or D%2==0 or L>B or S>2*X:
            self.stats['direct']+=1;return True
        U=D; blocks={}
        for z in self.pr:
            if U==1: break
            if U%z: continue
            c=0
            while U%z==0: c+=1;U//=z
            bad=forbidden_indices(z,ban);even=least(z,c,bad,False)
            odd=None if used else least(z,c,bad,True)
            blocks[z]=(c,even,odd,bad)
        # Exact minimum from one global Euler exception, or none. Ignore U's parity.
        base=X*U*prod(z**v[1] for z,v in blocks.items())
        saves={z:z**max(0,m-a) for z,(_,m,a,_) in blocks.items() if a is not None}
        lower=base//max((1,*saves.values()))
        if lower>B:
            self.stats['joint-size']+=1;return True
        if self.valuation and self.valuation_close(X,S,U,base,blocks,used):
            self.stats['valuation']+=1;return True
        limit=None;room=B//lower
        if self.cut:
            # U is fully stripped at 4999. omega(U)<=floor(log_5000 U).
            w=U;cnt=0
            while w>=5000: cnt+=1;w//=5000
            num=S*prod(blocks)*5000**cnt;den=X*prod(z-1 for z in blocks)*4999**cnt
            for t in (1,17,31,53,97,149,251,499,997,1999):
                costs,ns,ds=allowance(self.p,t,used);k=bisect_right(costs,room)-1
                if num*ns[k]<2*den*ds[k]: limit=t;break
            if limit==1:self.stats['deficient']+=1;return True
        if len(parts)>getattr(self,'depth_limit',6):return False  # failure, not closure
        if blocks and (limit is None or max(blocks)>10000):
            z=max(blocks);c,m,a,ds=blocks[z]
            # Enumerate every integer f>=c without presupposing which congruence
            # family works. If even (resp odd), other primes may (resp cannot)
            # receive the Euler exception. The very first over-budget exponent
            # for BOTH budgets dominates the entire unenumerated tail.
            square=base//z**m;even_other=square//max([1]+[s for r,s in saves.items() if r!=z]);odd_other=square
            f=c;w=z**c
            while w*even_other<=B:
                feasible=(f%2==0 or (not used and z%4==f%4==1 and w*odd_other<=B))
                if feasible and permissible(f,ds):
                    if not self.visit(parts+((z,f),),X*w,S*sigma(z,f),ban):return False
                f+=1;w*=z
            self.stats['mandatory-tail']+=1;return True
        if limit is None:return False
        excluded=set(ban)
        for z in PS:
            if z>limit:break
            if z in excluded or z in zs or z in blocks: continue
            ds=forbidden_indices(z,frozenset(excluded)); f=1;w=z
            while w<=room:
                if (not f%2 or (not used and z%4==f%4==1)) and permissible(f,ds):
                    if not self.visit(parts+((z,f),),X*w,S*sigma(z,f),frozenset(excluded)):return False
                f+=1;w*=z
            excluded.add(z)
        self.stats['least-prime-tail']+=1;return True

class Historical:
    def __init__(self):
        audits=[read(R/path) for path in ('SupplierBatch/BatchAudit2400.json','IndicatorCapacity/Audit2400.json','TeichmullerValuation/Audit2400.json','TeichmullerValuation/GeminiBatchAudit2400.json')];sup,ind,tei,gem=audits
        self.ids={s['id'] for s in tei['open_manifest']}-{s['id'] for s in gem['additions']}
        self.known=set(map(tuple,gem['verified_exponents']))
        self.known.update((s['root'],s['exponent']) for s in read(R/'EulerOneSieve/ActualExponentRecords.json'))
        for audit in (sup,ind):self.known.update((s['root'],s['exponent']) for s in audit['exact_exponents'])
        for audit in audits:
            for s in audit['additions']:
                for item in s.get('proof',[]):
                    if isinstance(item,dict) and 'exponent' in item:self.known.add((s['root'],item['exponent']))
        recent=read(R/'OrderSupplyNext/Audit.json');self.known.update((v[0],v[1]) for v in recent['proved']); self.ids.difference_update(s[0] for s in recent['closed'])
        with (R/'FermatRootValuation/Results.csv').open() as f:self.shards=list(csv.DictReader(f))
        import VerifyTeichmullerValuation2400 as tb
        self.tb=tb
    def pending(self,p,e):
        hits=[s for s in self.shards if int(s['p'])==p and (int(s['d'])==e if s['mode']=='exact' else (e+1)%(int(s['d'])+1)==0)]
        if not hits or (p,e) in self.known or any(s['shard'] not in self.ids for s in hits):return False
        a=sigma(p,e);a//=a&-a
        if p**e*a>B or any(a%b==0 for b in ORDER[:ORDER.index(p)]):return False
        tb=self.tb
        rule=tb.verify_odd_root_exponent if e%2 else tb.verify_even_exponent
        return not rule(p,e,old_profile(p))[0]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,default=H/'Verified.json')
    ap.add_argument('--allow-overlap',action='store_true',help='skip ONLY novelty check against changing frontier')
    ap.add_argument('--valuation',action='store_true',help='use multilevel valuation bounds for all input records')
    args=ap.parse_args()
    rows=read(args.input);need(rows,'empty certificate');seen=set();stats=Counter();old=None if args.allow_overlap else Historical();roots=Counter()
    for row in rows:
        p,e,fs=row['p'],row['e'],row['fs'];tech='valuation' if args.valuation else row['tech']
        need(p in (7,11,13,19,31) and e>0 and (e%2==0 or p%4==e%4==1),'invalid root/exponent')
        need((p,e) not in seen and tech in ('cut','size','valuation'),'duplicate or unknown technique');seen.add((p,e))
        if old is not None:need(old.pending(p,e),('not previously open',p,e))
        need(all(z>2 and sigma(p,e)%z==0 and prime(z) for z in fs),('uncertified divisor',p,e))
        tr=Proof(p,e,fs,tech=='cut',tech=='valuation');tr.depth_limit=max(6,min(20,int(row.get('depth',6))));need(tr.prove(),('tree incomplete',p,e,tr.stats));stats.update(tr.stats);roots[p]+=1
        print(p,e,tech,dict(tr.stats),flush=True)
    print('ECPP_FILES',json.dumps(sorted(ECPP_FILES)))
    print('ALL VERIFIED',len(seen),'roots',dict(sorted(roots.items())),'totals',dict(stats),'novelty',('not checked' if old is None else 'checked'))

if __name__=='__main__':main()

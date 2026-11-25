"""Cold stdlib-only terminal certificate for a pinned set of forbidden primes. No LP solver, factorization library, PRP assumption for anonymous blocks, square-kernel bound, or Euler-refund rule. Verifies both earlier prime-only terminal archives, deterministic 64-bit / recursive Pocklington implications, every source-attached cofactor, *per-block* roughness by an exact sieve/gcd, and all dyadic dual arithmetic. The number printed is lower-rounded by a million; admission does not depend on floating points. Use `python -I -S -B .../RoughTerminalWitness.py .../FiveAvoid.json`."""
import argparse,gzip,json,math,sys,time,hashlib
from functools import cache
from pathlib import Path
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import DYADIC,allowed,build_model,verify,sigma;from RoadblockDual import log_bounds,odd_primes
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def require(x,why):
    if not x:raise ValueError(why)
@cache
def primorial(lo):return math.prod(odd_primes(lo-1))

def main():
    if not __debug__:raise SystemExit('run normally, never -O')
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);args=ap.parse_args();D=json.loads(args.packet.read_text(encoding='utf8'));now=time.perf_counter();archives=[]
    for lab in ('Original','Replacement'):
        file=T/f'Certificates/Terminal{lab}.json.gz';require(hashlib.sha256(file.read_bytes()).hexdigest()==D['archive_sha256'][lab],'archive hash');a=json.load(gzip.open(file,'rt'));verify(a);archives.append(a)
    proof=D['proof']
    @cache
    def prime(n):
        if n<2**64:return is_prime_det64(n)
        F=1;seen=set()
        for p,k,w in proof.get(str(n),[]):
            if not(type(p)==type(k)==type(w)==int and 2<=p<n and p not in seen and 1<=k<=n.bit_length() and 1<w<n and prime(p)):return False
            F*=p**k;seen.add(p)
            if (n-1)%F or pow(w,n-1,n)!=1 or math.gcd(pow(w,(n-1)//p,n)-1,n)!=1:return False
        return F*F>n
    ans=[];seen=set();den=DYADIC*log_bounds(10)[1]
    for x in D['cases']:
        bad=x['forbidden'];cap=x['cut'];require(type(bad)==list and all(type(q)==int for q in bad) and len(set(bad))==len(bad) and set(bad)<={3,5,7,11,13,17,19,31} and tuple(sorted(bad)) not in seen,'mask');seen.add(tuple(sorted(bad)));require(type(cap)==int and 22<=cap<=100,'cutoff');bs=set(odd_primes(5000))-set(bad);em={}
        for a in archives:
            for p,e,q,k in a['edges']:
                if p in bs and q not in bad and e<=cap and allowed(p,e,bad):em[p,e,q]=max(k,em.get((p,e,q),0))
        for row in x['new']:
            require(type(row)==list and len(row)==4 and all(type(a)==int for a in row),'edge');p,e,q,k=row;require(p in bs and 1<=e<=cap and (not e%2 or p%4==e%4==1) and allowed(p,e,bad),'origin');require(q>2 and q!=p and q not in bad and 1<=k<=255 and sigma(p,e)%q**k==0 and prime(q),'unverified divisor');em[p,e,q]=max(k,em.get((p,e,q),0))
        es=sorted((*key,k) for key,k in em.items());cost,rows,tail=build_model(bad,5000,cap,es);unmodified=cost.copy();ps=sorted(bs|{q for p,e,q,k in es});pos={r:i for i,r in enumerate(ps)};covered=math.prod(set(ps)|set(bad));opts=set();ab=dict(rows[0][0]);maxL=0
        for row in x['blocks']:
            require(type(row)==list and len(row)==4 and all(type(v)==int for v in row),'block');r,f,C,L=row;require(r in bs and 1<=f<=cap and (not f%2 or r%4==f%4==1) and allowed(r,f,bad) and (r,f) not in opts,'block source');opts.add((r,f));require(5001<=L<=5000001 and L%2 and C>1 and C%2 and sigma(r,f)%C==0 and math.gcd(C,covered)==1 and math.gcd(C,primorial(L))==1,'roughness/divisibility/overlap');covered*=C;maxL=max(maxL,L);count=0;tmp=C
            while tmp>=L:count+=1;tmp//=L
            ids=[j for j,a in rows[2+pos[r]][0] if unmodified[j]==f*log_bounds(r)[0]];require(len(ids)==1,'not an exact option');j=ids[0];cost[j]+=log_bounds(C)[0];ab[j]-=sum(log_bounds(L+2*h,L+2*h-1)[1] for h in range(count))
        rows[0]=list(ab.items()),rows[0][1];red=[c*DYADIC for c in cost];z=0;last=-1
        for i,v in x['weights']:
            require(type(i)==type(v)==int and last<i<len(rows) and v>=0,'weight');last=i;m,b=rows[i];z-=v*b
            for j,a in m:red[j]+=a*v
        require(red[tail]>=0,'unbounded LP tail');z+=sum(min(0,c) for j,c in enumerate(red) if j!=tail)
        for i,r in enumerate(ps):
            values=[red[j] for j,a in rows[2+i][0]];z+=min(0,min(values))-sum(min(0,k) for k in values)
        require(type(x['lb'])==int and z==x['lb'] and z>2400*den,'exact dual does not cross 2400');ans.append(dict(forbidden=bad,micro_floor=z*10**6//den,integer_bound=z,anonymous=len(opts),largest_checked_minimum_prime=maxL,new_edges=len(x['new']),model_edges=len(es),variables=len(cost)))
    require(bool(ans),'empty');print(json.dumps(dict(certificates=ans,seconds=round(time.perf_counter()-now,3)),separators=(',',':')))
if __name__=='__main__':main()

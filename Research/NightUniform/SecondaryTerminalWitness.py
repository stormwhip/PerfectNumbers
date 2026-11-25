"""Independently rebuild and cold-replay a finite exact expansion at selected large terminal bases. Never imports a solver, discovery code or previous counts. Start from SHA-pinned authenticated factor archives and verify every extra base/factor; build exact/upper options straight from Euler parity and finite forbidden sigma tests. Removing each selected pairwise-coprime rough cofactor's prime support is valid because its primes are excluded from ALL explicit bases and edges incl. newly promoted secondary sources. Standard library only. See SecondaryTerminalProof.md for the lower-bound argument."""
from pathlib import Path
from functools import cache
import sys,math,json,hashlib,gzip,time,argparse
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import verify,DYADIC;from RoadblockDual import SCALE,log_bounds,odd_primes
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def req(x,why):
    if not x:raise ValueError(why)
@cache
def sigma(p,e):return (p**(e+1)-1)//(p-1)
@cache
def primorial(l):return math.prod(odd_primes(l-1))

def main():
    if not __debug__:raise SystemExit('never run with -O')
    a=argparse.ArgumentParser();a.add_argument('packet',type=Path);args=a.parse_args();D=json.loads(args.packet.read_text());now=time.perf_counter();ar=[]
    for tag in ('Original','Replacement'):
        f=T/f'Certificates/Terminal{tag}.json.gz';req(hashlib.sha256(f.read_bytes()).hexdigest()==D['archive_sha256'][tag],'archive checksum');x=json.load(gzip.open(f,'rt'));verify(x);ar.append(x)
    proof=D['proof'];result=[];seen=set()
    @cache
    def prime(n):
        if n<2**64:return is_prime_det64(n)
        F=1;seen0=set()
        for p,k,a in proof.get(str(n),[]):
            if not (type(p)==type(k)==type(a)==int and 1<p<n and p not in seen0 and 0<k<=n.bit_length() and 1<a<n and prime(p)):return False
            seen0.add(p);F*=p**k
            if (n-1)%F or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//p,n)-1,n)!=1:return False
        return F*F>n
    for d in D['cases']:
        bad=d['forbidden'];cap=d['cut'];extra=d['promoted'];req(type(bad)==list and all(type(r)==int for r in bad) and len(set(bad))==len(bad) and set(bad)<={3,5,7,11,13,17,19,31} and tuple(sorted(bad)) not in seen,'mask');seen.add(tuple(sorted(bad)));req(type(cap)==int and 22<=cap<=100 and type(extra)==list,'cutoff');base=set(odd_primes(5000))-set(bad);arcprime=set();edges={}
        def legal(p,e):return all((e+1)%q if p%q==1 else pow(p,e+1,q)!=1 for q in bad)
        for archive in ar:
            for p,e,q,c in archive['edges']:
                arcprime.add(q)
                if p in base and q not in bad and e<=cap and legal(p,e):edges[p,e,q]=max(c,edges.get((p,e,q),0))
        def cert(q):return q in base or q in arcprime or prime(q)
        promoted={}
        for p,f in extra:
            req(type(p)==type(f)==int and p>5000 and p not in promoted and 1<=f<=100 and cert(p),'unproved secondary base');promoted[p]=f
        thresholds={p:cap for p in base};thresholds.update(promoted)
        for p,e,q,c in d['new']:
            req(all(type(z)==int for z in (p,e,q,c)) and p in thresholds and 1<=e<=thresholds[p] and (not e%2 or p%4==e%4==1) and legal(p,e),'edge source');req(q>2 and q!=p and q not in bad and 1<=c<=255 and sigma(p,e)%q**c==0 and cert(q),'unproved edge');edges[p,e,q]=max(c,edges.get((p,e,q),0))
        es=sorted((*ks,c) for ks,c in edges.items());ps=sorted(set(thresholds)|{q for p,e,q,c in es});opts={};C=[];ab=[];eu=[];exact={}
        for p in ps:
            group=[];stop=thresholds.get(p,0);l=log_bounds(p)[0]
            for start,step,isEuler in ((2,2,False),(1,4,True)):
                # If sigma(p)=p+1 forbidden then every p^(4k+1) forbidden too.
                if isEuler and (p%4!=1 or not legal(p,1)):continue
                e=start
                while e<=stop:
                    if legal(p,e):
                        i=len(C);C.append(e*l);ab.append(log_bounds(sigma(p,e),p**e)[1]);group.append((i,e,isEuler,True));exact[p,e]=(i,isEuler)
                        if isEuler:eu.append(i)
                    e+=step
                while not legal(p,e):e+=step
                i=len(C);C.append(e*l);ab.append(log_bounds(p,p-1)[1]);group.append((i,e,isEuler,False));
                if isEuler:eu.append(i)
            opts[p]=group
        tail=len(C);l=log_bounds(5001)[0];h=log_bounds(5001,5000)[1];C.extend((2*l*SCALE//h,l));ab.extend((SCALE,h));eu.append(tail+1);covered=math.prod(set(ps)|set(bad));origin=set()
        for p,e,n,L in d['blocks']:
            req(all(type(z)==int for z in (p,e,n,L)) and (p,e) in exact and (p,e) not in origin and 5001<=L<=5000001 and L%2 and n>1 and n%2 and sigma(p,e)%n==0 and math.gcd(covered,n)==1 and math.gcd(primorial(L),n)==1,'bad anonymous cofactor');origin.add((p,e));covered*=n;j,sp=exact[p,e];C[j]+=log_bounds(n)[0];u=n;c=0
            while u>=L:u//=L;c+=1
            ab[j]+=sum(log_bounds(L+2*k,L+2*k-1)[1] for k in range(c))
        rows=[(list(enumerate(-z for z in ab)),-log_bounds(2)[0]), ([(i,SCALE) for i in eu],SCALE)];rows.extend(([(j,SCALE) for j,e,s,x in opts[p]],SCALE) for p in ps)
        for p,e,q,v in es:
            j,sp=exact[p,e];rows.append(([(j,SCALE)]+[(i,-SCALE) for i,f,s,x in opts[q] if (not sp or not s) and (not x or f>=v)],0))
        red=[c*DYADIC for c in C];z=0;last=-1
        for idx,w in d['weights']:
            req(type(idx)==type(w)==int and last<idx<len(rows) and w>=0,'bad row weight');last=idx;tt,bd=rows[idx];z-=w*bd
            for j,v in tt:red[j]+=v*w
        req(red[tail]>=0,'unbounded tail');z+=sum(min(0,k) for j,k in enumerate(red) if j!=tail)
        for p in ps:
            g=[red[j] for j,e,s,x in opts[p]];z+=min(0,min(g))-sum(min(0,t) for t in g)
        den=DYADIC*log_bounds(10)[1];req(z==d['lb'] and z>2400*den,'insufficient lower bound');result.append(dict(forbidden=bad,micro_floor=z*10**6//den,integer_numerator=z,expanded=len(promoted),anonymous=len(origin),edges=len(es),variables=len(C),rows=len(rows)))
    req(bool(result),'empty packet');print(json.dumps(dict(results=result,seconds=round(time.perf_counter()-now,3)),separators=(',',':')))
if __name__=='__main__':main()

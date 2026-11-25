"""Stdlib-only verifier for anonymous size+square-kernel terminal packets. Reuses the published anonymous terminal verifier's archive/large-prime validation by importing its actual core names; builds the parity-extended LP independently of the numerical search. Claimed minimum ordinary uplift k checked via Legendre wheel (or exact short exhaustive check), not merely believed. Only one Euler refund variable may be used globally, never a refund per selected block."""
from pathlib import Path
import sys,json,gzip,math,argparse
from functools import cache
sys.path.insert(0,str(Path(__file__).resolve().parent));from TerminalAnonymousWitness import R,T,DYADIC,allowed,build_model,verify,sigma,log_bounds,odd_primes,is_prime_det64,need
SM=tuple(odd_primes(151))
@cache
def kernel(C,K):
    if K<=1:return True
    if K>5001**2 or math.isqrt(C)**2==C:return False
    # All factors of C>5000 by separate gcd check. If its squarefree kernel <K, that kernel is either 1 or a divisor prime r<K. Search every r satisfying all Legendre tests via a wheel. A composite candidate is tested too and cannot cause false exclusion.
    m=2;res=[1]
    for p in SM:
        if not C%p or not m%p:continue
        a=pow(C,(p-1)//2,p);vals=[u for u in range(1,p) if pow(u,(p-1)//2,p)==a]
        if len(res)*len(vals)>20000:break
        inv=pow(m,-1,p);res=[z+m*((u-z)*inv%p) for z in res for u in vals];m*=p
        if m>=K:break
    for z in res:
        r=5001+(z-5001)%m
        while r<K:
            if C%r==0 and math.isqrt(C*r)**2==C*r:return False
            r+=m
    return True

def main():
    if not __debug__:raise SystemExit('use without -O')
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);args=ap.parse_args();P=json.loads(args.packet.read_text());proof=P['proof'];arch=[]
    for lab in ('Original','Replacement'):
        ar=json.load(gzip.open(T/f'Certificates/Terminal{lab}.json.gz','rt'));verify(ar);arch.append(ar)
    @cache
    def prime(n):
        if n<2**64:return is_prime_det64(n)
        F=1;seen=set()
        for q,k,a in proof.get(str(n),[]):
            if not (type(q)==type(k)==type(a)==int and 2<=q<n and q not in seen and 1<=k<=n.bit_length() and 1<a<n and prime(q)):return False
            seen.add(q);F*=q**k
            if (n-1)%F or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//q,n)-1,n)!=1:return False
        return F*F>n
    ans=[];seen=set()
    for x in P['cases']:
        bad=x['forbidden'];cap=x['cut'];need(type(bad)==list and len(bad)==len(set(bad)) and all(type(r)==int for r in bad) and set(bad)<={3,5,7,11,13,17,19,31} and tuple(sorted(bad)) not in seen and type(cap)==int and 22<=cap<=100,'mask or cap');seen.add(tuple(sorted(bad)));B=set(odd_primes(5000))-set(bad);E={}
        for ar in arch:
            for r,f,q,v in ar['edges']:
                if r in B and q not in bad and f<=cap and allowed(r,f,bad):E[r,f,q]=max(v,E.get((r,f,q),0))
        for r,f,q,v in x['new']:
            need(all(type(u)==int for u in (r,f,q,v)) and r in B and 1<=f<=cap and (f%2==0 or f%4==r%4==1) and allowed(r,f,bad) and 2<q!=r and q not in bad and 1<=v<=255 and sigma(r,f)%q**v==0 and prime(q),'bad edge');E[r,f,q]=max(v,E.get((r,f,q),0))
        es=sorted((*key,v) for key,v in E.items());C,rows,tail=build_model(bad,5000,cap,es);ps=sorted(B|{q for r,f,q,v in es});base_cost=C.copy();G=math.prod(set(ps)|set(bad));ab=dict(rows[0][0]);eu=list(rows[1][0]);ex=[];used=set();blocks=x['anonymous'];Ks=x['lower'];need(len(blocks)==len(Ks),'premium count')
        for (r,f,n),K in zip(blocks,Ks):
            need(all(type(z)==int for z in (r,f,n,K)) and r in B and 1<=f<=cap and (f%2==0 or f%4==r%4==1) and allowed(r,f,bad) and (r,f) not in used and n>1 and n%2 and sigma(r,f)%n==0 and math.gcd(G,n)==1 and 1<=K<=5001**2 and kernel(n,K),'invalid block or kernel lower bound');used.add((r,f));G*=n;js=[j for j,a in rows[2+ps.index(r)][0] if base_cost[j]==f*log_bounds(r)[0]];need(len(js)==1,'source');j=js[0];u=n;cnt=0
            while u>=5001:cnt+=1;u//=5001
            ab[j]-=sum(log_bounds(5001+2*h,5000+2*h)[1] for h in range(cnt));C[j]+=log_bounds(n)[0]
            if K>1:
                i=len(C);C[j]+=log_bounds(K)[0];C.append(-log_bounds(K)[1]);eu.append((i,1<<80));ex.append(([(i,1<<80),(j,-(1<<80))],0))
        rows[0]=list(ab.items()),rows[0][1];rows[1]=eu,rows[1][1];rows+=ex;red=[u*DYADIC for u in C];z=0;last=-1
        for j,v in x['weights']:
            need(type(j)==type(v)==int and last<j<len(rows) and v>=0,'weight');last=j;tt,d=rows[j];z-=d*v
            for i,a in tt:red[i]+=a*v
        need(red[tail]>=0,'tail');z+=sum(min(0,v) for j,v in enumerate(red) if j!=tail)
        for i,p in enumerate(ps):
            rr=[red[j] for j,a in rows[2+i][0]];z+=min(0,min(rr))-sum(min(0,v) for v in rr)
        den=DYADIC*log_bounds(10)[1];need(z==x['lb'] and z>2400*den,'insufficient bound');ans.append(dict(forbidden=bad,micro_floor=z*10**6//den,blocks=len(blocks),refunds=len(ex)))
    need(bool(ans),'empty certificate');print(json.dumps(ans,separators=(',',':')))
if __name__=='__main__':main()

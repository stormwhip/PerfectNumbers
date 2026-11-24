"""Independently replay four-root complementary exponent restriction. Pure standard library, only established repo terminal and primality engines. No solver, discovery outputs, precomputed residues or package-specific helpers. Hypothesis 3,5,7,11 do not divide N, and the independently certified five-root hitting theorem (5c9dcd4) implies v13(N)>0. Result is an exhaustive necessary exponent set under N<=10^2400, never a complete four-root exclusion unless that set is empty. Input carries archived SHA, source-edge/coprime blocks, ONE sparse dual and expected survivor list; latter used solely as equality assertion after recomputation.
"""
import argparse,json,math,gzip,sys,time,hashlib
from pathlib import Path
from functools import cache
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import build_model,verify,DYADIC,allowed,sigma;from RoadblockDual import SCALE,log_bounds,odd_primes
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def req(k,w):
    if not k:raise ValueError(w)
@cache
def prod(L):return math.prod(odd_primes(L-1))
@cache
def ab(n,L):
    cnt=0
    while n>=L:n//=L;cnt+=1
    return sum(log_bounds(L+2*i,L+2*i-1)[1] for i in range(cnt))
@cache
def rough(n):
    for l in (300001,100001,30001,10001):
        if math.gcd(n,prod(l))==1:return l
    return 5001

def val(n,r):
    f=0
    while n%r==0:f+=1;n//=r
    return f

def main():
    if not __debug__:raise SystemExit('do not use -O')
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);args=ap.parse_args();D=json.loads(args.packet.read_text());P=13;bad=(3,5,7,11);cap=40;now=time.perf_counter();base=set(odd_primes(5000))-set(bad);em={};proof=D['proof'];
    for lab in ('Original','Replacement'):
        f=T/f'Certificates/Terminal{lab}.json.gz';req(hashlib.sha256(f.read_bytes()).hexdigest()==D['archive_sha256'][lab],'archive');ar=json.load(gzip.open(f,'rt'));verify(ar)
        for p,e,q,c in ar['edges']:
            if p in base and p!=P and q!=P and q not in bad and e<=cap and allowed(p,e,bad):em[p,e,q]=max(c,em.get((p,e,q),0))
    @cache
    def prime(n):
        if n<2**64:return is_prime_det64(n)
        F=1;seen=set()
        for q,k,a in proof.get(str(n),[]):
            if not(type(q)==type(k)==type(a)==int and 2<=q<n and q not in seen and 1<=k<=n.bit_length() and 1<a<n and prime(q)):return False
            seen.add(q);F*=q**k
            if (n-1)%F or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//q,n)-1,n)!=1:return False
        return F*F>n
    for p,e,q,c in D['new']:
        req(all(type(a)==int for a in (p,e,q,c)) and p in base and p!=P and 1<=e<=cap and (not e%2 or p%4==e%4==1) and allowed(p,e,bad) and q>2 and q!=P and q!=p and q not in bad and 1<=c<=255 and sigma(p,e)%q**c==0 and prime(q),'invalid edge');em[p,e,q]=max(c,em.get((p,e,q),0))
    es=sorted((*k,c) for k,c in em.items());C,rs,tail=build_model(bad,5000,cap,es);ps=sorted(base|{q for p,e,q,c in es});orig=C.copy();G={p:[j for j,_ in rs[2+i][0]] for i,p in enumerate(ps)};A=dict(rs[0][0]);used=math.prod(set(ps)|set(bad));seen=set();bl=[]
    for r,f,n,L in D['blocks']:
        req(all(type(a)==int for a in (r,f,n,L)) and r!=P and r in base and 1<=f<=cap and (not f%2 or r%4==f%4==1) and allowed(r,f,bad) and (r,f) not in seen and n>1 and n%2 and sigma(r,f)%n==0 and math.gcd(n,used)==1 and L%2 and 5001<=L<=300001 and math.gcd(n,prod(L))==1,'block or support');used*=n;seen.add((r,f));ids=[j for j in G[r] if orig[j]==f*log_bounds(r)[0]];req(len(ids)==1,'origin');j=ids[0];bl.append((r,j,n,L));C[j]+=log_bounds(n)[0];A[j]-=ab(n,L)
    rs[0]=list(A.items()),rs[0][1]+log_bounds(P,P-1)[1];index=2+ps.index(P);rs[index]=rs[index][0],0;w=[0]*len(rs);last=-1
    for i,v in D['weights']:
        req(type(i)==type(v)==int and last<i<len(w) and v>=0,'dual');w[i]=v;last=i
    red=[c*DYADIC for c in C];const=0
    for (tt,d),v in zip(rs,w):
        const-=v*d
        if v:
            for j,a in tt:red[j]+=v*a
    req(red[tail]>=0,'tail');const+=sum(min(0,v) for j,v in enumerate(red) if j!=tail)
    groupmin={}
    for r,ids in G.items():
        g=min(0,min(red[j] for j in ids));groupmin[r]=g;const+=g-sum(min(0,red[j]) for j in ids)
    req(const==D['constant'],'residual dual');limit=2400*DYADIC*log_bounds(10)[1];step=DYADIC*log_bounds(P)[0];end=max(0,1+(limit-const)//step);B=10**2400;out=[];cuts={}
    for e in range(1,end):
        if e%2 and e%4!=1:continue
        z=sigma(P,e);A=z//(z&-z);pe=P**e
        if math.gcd(A,3*5*7*11)>1:cuts['forbid']=cuts.get('forbid',0)+1;continue
        if pe*A>B:cuts['size']=cuts.get('size',0)+1;continue
        rem=A;cts={}
        for r in ps:
            if rem%r==0:f=val(rem,r);rem//=r**f;cts[r]=f
        debt=w[0]*ab(rem,rough(rem));gain=step*e+DYADIC*log_bounds(rem)[0]-debt;changes={};bases=set(cts)
        for r,j,n,L in bl:
            n0=n;g=math.gcd(n0,rem)
            while g!=1:n0//=g;g=math.gcd(n0,rem)
            if n0!=n:changes[j]=DYADIC*(log_bounds(n0)[0]-log_bounds(n)[0])+w[0]*(ab(n,L)-ab(n0,L));bases.add(r)
        for r in bases:
            c=cts.get(r,0);mn=min(red[j]+changes.get(j,0)+DYADIC*max(0,c*log_bounds(r)[0]-orig[j]) for j in G[r]);gain+=(mn if c else min(0,mn))-groupmin[r]
        if const+gain>limit:cuts['dual']=cuts.get('dual',0)+1
        else:out.append(e)
    req(type(D['survivors'])==list and all(type(e)==int for e in D['survivors']) and out==D['survivors'] and end==D['tail'],'survivor mismatch');print(json.dumps(dict(root=P,forbidden=bad,uniform_tail=end,remaining=len(out),max_remaining=max(out,default=0),cuts=cuts,seconds=round(time.perf_counter()-now,3)),separators=(',',':')))
if __name__=='__main__':main()

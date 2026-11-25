"""Replay exact anonymous cofactor dual. Reuse the already published prime-witness terminal verifier's complete original/replacement archive validation, but additionally bind all anonymous costs/gains to pairwise-coprime odd cofactors of indicated exact source sigmas. These witnesses need no primality assumptions. Rebuild modified model and compare integer dual floor, including unbounded-tail and integral per-base alternatives. Stdlib only."""
import argparse,json,gzip,math,sys
from pathlib import Path
from functools import cache
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import DYADIC,allowed,build_model,verify,sigma;from RoadblockDual import log_bounds,odd_primes
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def need(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    if not __debug__:raise SystemExit('run without -O')
    a=argparse.ArgumentParser();a.add_argument('packet',type=Path);args=a.parse_args();P=json.loads(args.packet.read_text());D=P['cases'];proof=P['proof'];need(type(D)==list and len(D)>0,'empty packet');archives=[]
    for lab in ('Original','Replacement'):
        d=json.load(gzip.open(T/f'Certificates/Terminal{lab}.json.gz','rt'));verify(d);archives.append(d)
    @cache
    def prime(n):
        if n<2**64:return is_prime_det64(n)
        F=1;seen=set()
        for q,k,a in proof.get(str(n),[]):
            if not (type(q)==type(k)==type(a)==int and 2<=q<n and q not in seen and 1<=k<=n.bit_length() and 1<a<n and prime(q)):return False
            seen.add(q);F*=q**k
            if (n-1)%F or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//q,n)-1,n)!=1:return False
        return F*F>n
    results=[];seen=set();den=DYADIC*log_bounds(10)[1]
    for x in D:
        bad=x['forbidden'];cut=x['cut'];limit=5000;need(type(bad)==list and all(type(p)==int for p in bad) and len(bad)==len(set(bad)) and set(bad)<={3,5,7,11,13,17,19,31} and tuple(sorted(bad)) not in seen,'mask');seen.add(tuple(sorted(bad)));need(type(cut)==int and 22<=cut<=100,'cut');base=set(odd_primes(limit))-set(bad);E={}
        for ar in archives:
            for p,e,q,c in ar['edges']:
                if p in base and q not in bad and e<=cut and allowed(p,e,bad):E[p,e,q]=max(c,E.get((p,e,q),0))
        for row in x['new']:
            need(type(row)==list and len(row)==4 and all(type(v)==int for v in row),'edge');p,e,q,c=row
            need(p in base and 1<=e<=cut and (not e%2 or p%4==e%4==1) and allowed(p,e,bad),'source');need(q>2 and q!=p and q not in bad and 1<=c<=255 and sigma(p,e)%q**c==0 and prime(q),'target');E[p,e,q]=max(c,E.get((p,e,q),0))
        es=sorted((*k,v) for k,v in E.items());cost,rows,tail=build_model(bad,limit,cut,es);ps=sorted(base|{q for p,e,q,c in es});index={p:i for i,p in enumerate(ps)};covered=math.prod(set(ps)|set(bad));used=set();ab=dict(rows[0][0])
        for r,f,C in x['anonymous']:
            need(type(r)==type(f)==type(C)==int and r in base and 1<=f<=cut and (not f%2 or f%4==r%4==1) and allowed(r,f,bad) and (r,f) not in used,'bad anonymous origin');used.add((r,f));need(C>1 and C%2 and sigma(r,f)%C==0 and math.gcd(C,covered)==1,'overlap, failed divisibility or even anonymous block');covered*=C
            ix=[j for j,a in rows[2+index[r]][0] if cost[j]==f*log_bounds(r)[0]];need(len(ix)==1,'unbound exact option');j=ix[0];n=C;cnt=0
            while n>=limit+1:n//=limit+1;cnt+=1
            gain=sum(log_bounds(limit+1+2*k,limit+2*k)[1] for k in range(cnt));cost[j]+=log_bounds(C)[0];ab[j]-=gain
        rows[0]=(list(ab.items()),rows[0][1]);red=[c*DYADIC for c in cost];z=0;last=-1
        for i,v in x['weights']:
            need(type(i)==type(v)==int and last<i<len(rows) and v>=0,'dual');last=i;terms,d=rows[i];z-=v*d
            for j,a in terms:red[j]+=a*v
        need(red[tail]>=0,'tail');z+=sum(min(0,k) for j,k in enumerate(red) if j!=tail)
        for i,p in enumerate(ps):
            rr=[red[j] for j,a in rows[2+i][0]];z+=min(0,min(rr))-sum(min(0,v) for v in rr)
        need(z==x['lb'] and z>2400*den,'insufficient exact lower bound');results.append(dict(forbidden=bad,micro_floor=z*10**6//den,blocks=len(used),edges=len(es)))
    print(json.dumps(results,separators=(',',':')))
if __name__=='__main__':main()

"""Exact terminal dual package with Pocklington medium-prime implications, supports arbitrary root subsets of original 8. Pinned certified archive implication reuse. No SciPy, SymPy, GPU, network, optional hooks or external discovery inputs. A single incorrect primality witness, edge, row, or dual bound fails the entire replay. Outputs a numerical floor only after the strict integer target comparison. Assumes standard odd-perfect-number and Euler form in repo's terminal model.
"""
from pathlib import Path
from functools import cache
import argparse,json,gzip,sys,math
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import DYADIC,allowed,build_model,verify,sigma;from RoadblockDual import log_bounds,odd_primes
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def need(x,why):
    if not x:raise ValueError(why)

def main():
    if not __debug__:raise SystemExit('run without -O')
    a=argparse.ArgumentParser();a.add_argument('packet',type=Path);args=a.parse_args();P=json.loads(args.packet.read_text());proof=P['proof'];D=P['cases'];need(type(D)==list and D,'empty packet');arches=[]
    for lab in ('Original','Replacement'):
        ar=json.load(gzip.open(T/f'Certificates/Terminal{lab}.json.gz','rt'));verify(ar);arches.append(ar)
    @cache
    def prime(n):
        if n<2**64:return is_prime_det64(n)
        F=1;seen=set();rows=proof.get(str(n),[])
        for r,e,a in rows:
            if not (type(r)==type(e)==type(a)==int and 2<=r<n and 0<e<=n.bit_length() and 1<a<n and r not in seen and prime(r)):return False
            seen.add(r);F*=r**e
            if (n-1)%F or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//r,n)-1,n)!=1:return False
        return F**2>n
    ans=[];seen=set();den=DYADIC*log_bounds(10)[1]
    for x in D:
        bad=x['forbidden'];cut=x['cut'];L=5000;need(type(bad)==list and all(type(q)==int for q in bad) and len(set(bad))==len(bad) and set(bad)<={3,5,7,11,13,17,19,31} and tuple(sorted(bad)) not in seen,'invalid or duplicate root set');seen.add(tuple(sorted(bad)));need(type(cut)==int and 22<=cut<=100,'cutoff');B=set(odd_primes(L))-set(bad);em={}
        for ar in arches:
            for p,e,q,k in ar['edges']:
                if p in B and q not in bad and e<=cut and allowed(p,e,bad):em[p,e,q]=max(k,em.get((p,e,q),0))
        for row in x['new']:
            need(type(row)==list and len(row)==4 and all(type(v)==int for v in row),'malformed factor');p,e,q,k=row;need(p in B and 1<=e<=cut and (not e%2 or p%4==e%4==1) and allowed(p,e,bad),'illegal origin');need(q>2 and q!=p and q not in bad and 1<=k<=255 and sigma(p,e)%q**k==0 and prime(q),'unproved factor');em[p,e,q]=max(k,em.get((p,e,q),0))
        es=sorted((*s,k) for s,k in em.items());C,rows,t=build_model(bad,L,cut,es);pr=sorted(B|{q for p,e,q,k in es});red=[v*DYADIC for v in C];z=0;last=-1
        for j,v in x['weights']:
            need(type(j)==type(v)==int and last<j<len(rows) and v>=0,'malformed dual');last=j;m,b=rows[j];z-=v*b
            for u,a in m:red[u]+=a*v
        need(red[t]>=0,'tail');z+=sum(min(0,k) for j,k in enumerate(red) if j!=t)
        for i,p in enumerate(pr):
            H0=[red[u] for u,a in rows[2+i][0]];z+=min(0,min(H0))-sum(min(0,v) for v in H0)
        need(z==x['lb'] and z>2400*den,'bound');ans.append(dict(forbidden=bad,micro_floor=z*10**6//den,edges=len(es),variables=len(C)))
    print(json.dumps(ans,separators=(',',':')))
if __name__=='__main__':main()

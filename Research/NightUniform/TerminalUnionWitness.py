"""Offline terminal dual replay with new prime-power implications. Archive inputs already tracked; verify BOTH pinned source terminal models before repurposing edges. Input packet contains only forbidden primes, cutoff, new <=64-bit certified relations, sparse dual and claimed exact integer lower numer. No SciPy. Exponents and prime roots validated, no arbitrary disabled branches. Prints only after exact lower exceeds 2400 log(10)."""
from pathlib import Path
import argparse,gzip,json,sys
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import DYADIC,allowed,build_model,verify,sigma;from RoadblockDual import SCALE,log_bounds,odd_primes
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def need(b,s):
    if not b:raise ValueError(s)

def main():
    if not __debug__:raise SystemExit('disable -O')
    a=argparse.ArgumentParser();a.add_argument('packet',type=Path);args=a.parse_args();x=json.loads(args.packet.read_text());bad=x['forbidden'];cut=x['cut'];L=5000
    need(type(bad)==list and all(type(p)==int for p in bad) and len(set(bad))==len(bad) and set(bad)<={3,5,7,11,13,17,19,31},'bad mask');need(type(cut)==int and 22<=cut<=100,'bad cutoff');B=set(odd_primes(L))-set(bad);em={};
    for lab in ('Original','Replacement'):
        arch=json.load(gzip.open(T/f'Certificates/Terminal{lab}.json.gz','rt'));verify(arch)
        for p,e,q,v in arch['edges']:
            if p in B and q not in bad and e<=cut and allowed(p,e,bad):em[p,e,q]=max(v,em.get((p,e,q),0))
    for row in x['new']:
        need(type(row)==list and len(row)==4 and all(type(z)==int for z in row),'bad edge');p,e,q,v=row
        need(p in B and 1<=e<=cut and (not e%2 or e%4==p%4==1) and allowed(p,e,bad),'bad origin')
        need(q!=p and 2<q<2**64 and q not in bad and is_prime_det64(q) and 1<=v<=255 and sigma(p,e)%q**v==0,'bad implication');em[p,e,q]=max(v,em.get((p,e,q),0))
    edges=sorted((*k,v) for k,v in em.items());cost,rows,tail=build_model(bad,L,cut,edges);ps=sorted(B|{q for p,e,q,v in edges});w=[0]*len(rows);last=-1
    for j,v in x['weights']:
        need(type(j)==type(v)==int and last<j<len(w) and v>=0,'bad dual');last=j;w[j]=v
    red=[k*DYADIC for k in cost];z=0
    for (tt,d),v in zip(rows,w):
        if v:
            z-=d*v
            for j,a in tt:red[j]+=v*a
    need(red[tail]>=0,'open tail');z+=sum(min(0,k) for j,k in enumerate(red) if j!=tail)
    # Any represented actual base selects exactly one option or none. Restore negative duplicate payoffs within each group to the minimum of zero and its cheapest reduced cost.
    for i,p in enumerate(ps):
        group=[red[j] for j,_ in rows[2+i][0]];z+=min(0,min(group))-sum(min(0,t) for t in group)
    den=DYADIC*log_bounds(10)[1];need(z==x['lb'] and z>2400*den,'not an exact certificate');print(json.dumps(dict(forbidden=bad,lower_exponent_micro_floor=10**6*z//den,variables=len(cost),factor_edges=len(edges),new_witnesses=len(x['new'])),separators=(',',':')))
if __name__=='__main__':main()

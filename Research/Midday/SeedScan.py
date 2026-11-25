"""Discovery: derive a new seed from public root hints and a bank of historical emitted factors.
The bank is advisory: divisibility by each exact geometric sum is tested by the certificate verifier.
"""
import argparse,json,sys,math,gzip
from pathlib import Path
from functools import cache,lru_cache
from collections import defaultdict
H=Path(__file__).resolve().parent; R=H.parent; W=R.parent.parent
sys.path[:0]=[str(R/'Nov25/Boost'),str(W/'NightCache/flint-lib'),str(W/'NightCache')]
from BoostScore import scorer,sigma,nonsupport,arithmetic
from flint import fmpz
from facts import Bank

def loadbank(out):
    src=defaultdict(set);F=[*W.glob('overnight/Research/NightLowRoute/*.json'),*W.glob('overnight/Research/NightSevenForest/*.json'),*W.glob('nov25-until-1000-scratch/Research/Nov25/*/best*.json')]
    for f in F:
        if f.stat().st_size>6_000_000:continue
        try:
            x=json.loads(f.read_bytes());pairs=x['owners'];
            for q,z in pairs:src[z].add(q)
        except (AttributeError,TypeError,KeyError,ValueError):continue
    out.write_text(json.dumps({str(z):sorted(qs) for z,qs in src.items()}),encoding='utf8');print('bank',len(src),sum(map(len,src.values())),flush=True)

@cache
def pr(n):return n%2 and bool(fmpz(n).is_probable_prime())
@cache
def divs(n):return sorted({j for d in range(1,math.isqrt(n)+1) if n%d==0 for j in (d,n//d)})
@lru_cache(2048)
def phi(z,h):return (z**h-1)//math.prod(phi(z,d) for d in divs(h)[:-1])

class Builder:
    def __init__(self,bank):self.edges={int(z):v for z,v in json.loads(bank.read_bytes()).items()};self.db=Bank();self.small=list(map(int,fmpz(1).factor())) if False else [n for n in range(3,8000,2) if pr(n)];self.prod=math.prod(self.small)
    @lru_cache(8192)
    def hints(self,z,f):
        n=arithmetic(z,f); out={q for q in self.edges.get(z,[]) if n%q==0};g=math.gcd(n,self.prod)
        if g!=1:out.update(q for q in self.small if g%q==0)
        for d in divs(f+1)[1:]:
            a=phi(z,d);out.update(q for q in self.db.lookup(z,d) if q>2 and a%q==0 and pr(q));left=nonsupport(a,2*math.prod(out));
            if left>1 and left.bit_length()<1850 and pr(left):out.add(left)
            elif 2<left and left.bit_length()<=70:out.update(int(k) for k,v in fmpz(left).factor())
        return sorted(out)
    def build(self,p,e,roots,steps,out,head=30,start=None):
        A=p*sigma(p,e);r=dict(p=p,e=e,roots=sorted(roots),owners=[],head=head) if start is None else {**start,'head':head};ow=dict(r['owners']);seen=set();best=0;early=0
        for step in range(steps):
            v,tr=scorer(r);m=min(v,key=v.get);score=v[m];
            if score>best:
                best=score;(out/f'{p}x{e}.json').write_text(json.dumps(dict(r,scout=score),separators=(',',':')),encoding='utf8')
            if score>2400.02:tr.clear();break
            fresh={};todo=[]
            for mode in sorted(v,key=v.get):
                if v[mode]>score+80:break
                state=tr(mode)
                for z,(h,f,k,w) in state.items():
                    if w is not False and (z,f) not in seen:todo.append((z,f))
            for z,f in dict.fromkeys(todo):
                seen.add((z,f));
                if z.bit_length()*(f+1)>14000:continue
                for q in self.hints(z,f):
                    if A%q and q not in ow and q not in fresh:fresh[q]=z
            tr.clear()
            if not fresh:break
            ow.update(fresh);r=dict(r,owners=sorted(ow.items()))
        print(p,e,'peak',round(best,4),'steps',step+1,'edges',len(ow),flush=True);sigma.cache_clear();return best

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--init',action='store_true');ap.add_argument('--out',type=Path);ap.add_argument('--factors',type=Path);ap.add_argument('--roots',type=int,nargs='+',default=[7,11]);ap.add_argument('--part',type=int,default=0);ap.add_argument('--parts',type=int,default=1);ap.add_argument('--steps',type=int,default=25);a=ap.parse_args()
    if a.init:return loadbank(a.bank)
    a.out.mkdir(parents=True,exist_ok=True);b=Builder(a.bank); jobs=[]
    for f in a.factors.glob('*.json'):
        p,e=map(int,f.stem.split('x'))
        if p not in a.roots or e%2:continue
        A=sigma(p,e);rs=[q for q,v in json.loads(f.read_bytes()) if A%q==0 and pr(q)]
        if rs:jobs.append((e*math.log10(p)+math.log10(A)+sum(math.log10(q)*2.5 for q in rs),p,e,rs))
    for _,p,e,rs in sorted(jobs,reverse=True)[a.part::a.parts]:
        b.build(p,e,rs,a.steps,a.out)
if __name__=='__main__':main()

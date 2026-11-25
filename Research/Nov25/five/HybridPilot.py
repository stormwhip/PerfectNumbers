"""Bounded discovery only; combine a cheap standard forest leaf with terminal pricing."""
from functools import cache
from hashlib import sha256
import json
from math import gcd, prod
from pathlib import Path
from time import monotonic
import sys
from sympy import isprime

HERE=Path(__file__).resolve().parent; R=HERE.parents[1]
sys.path[:0]=[str(HERE),str(R/'NightFive')]
from StateTerminalPilot import solve
from HybridReplay import forest, dual, bind, block, sigma, B, F, I, load_duals
from BankSieve import mentioned
from Rough import prime

ARCH=R.parents[1]/'overnight'/'Research'/'NightFive'
BAD=prod(F)


class Pilot:
    def __init__(self,e,limit=300,max_lp=20,timeout=420):
        self.e=e;self.nodes=0;self.limit=limit;self.start=monotonic();self.timeout=timeout
        self.H={};self.terminal=0;self.max_lp=max_lp;self.first=None;self.sources={}
        c=json.loads((R.parents[1]/'upstream'/'Research'/'RootFiveNext'/'Candidates.json').read_bytes())
        self.root=set(int(x) for x in c[str(e)] if isprime(int(x)))
        for f in ARCH.glob('*Seeds.json'):
            try:d=json.loads(f.read_bytes())
            except ValueError:continue
            for k,v in d.items():
                if ':' in k and isinstance(v,list):
                    try:
                        p,m=map(int,k.split(':')); gg=self.sources.setdefault(p,{})
                        gg.setdefault(m+1,set()).update(map(int,v))
                    except (TypeError, ValueError):continue
        f=ARCH/f'ForestCyc25_{e}.json'; self.seed=dict(json.loads(f.read_bytes())['owners'])
        self.ps={p for p in set(self.seed)|self.root if self.confirm(p)}
        self.by_base={}
        for q,p in self.seed.items():
            if q in self.ps:self.by_base.setdefault(p,[]).append(q)
        cert=json.loads((I.CERT_DIR/'DualP5.json').read_bytes())['duals']; self.ds=[bind(d,v) for d,v in zip(load_duals(),cert,strict=True)]

    @cache
    def confirm(self,z):
        if z<2**64:return prime(z)
        k=sha256(str(z).encode()).hexdigest()[:24]
        return (ARCH/'Witnesses'/f'{k}.json').is_file() or prime(z)

    @cache
    def sources_at(self,z,f):
        M=sigma(z,f); q=set(mentioned(M,100000)); q.update(self.by_base.get(z,[]))
        q.update(p for k,vs in self.sources.get(z,{}).items() if (f+1)%k==0 for p in vs)
        return tuple(p for p in q if M%p==0 and self.confirm(p))

    def leaf(self,x,X,S,D,P,path):
        if X*D>B or gcd(D,X*BAD)>1 or S>2*X:
            self.H[path]=['basic'];return True
        if dual(x,X,S,D,P,self.ds):
            self.H[path]=['dual',sorted(P)];return True
        parents={}; active=set(P); stack=list(P)
        while stack:
            p=stack.pop()
            for q in self.by_base.get(p,[]):
                if q not in active and X*D%q:
                    parents[q]=p;active.add(q);stack.append(q)
        if forest(x,X,D,P,list(parents.items())):
            self.H[path]=['forest',sorted(P),sorted(parents.items())];return True
        return False

    def visit(self,x,path):
        self.nodes+=1
        if self.nodes>self.limit or monotonic()-self.start>self.timeout:
            self.first=['limit',x];return False
        X=prod(p**f for p,f in x);S=prod(sigma(p,f) for p,f in x);D=S//gcd(2*X,S)
        P={q for q in set(self.root)|self.ps|{v for p,f in x for v in self.sources_at(p,f)} if D%q==0 and X%q!=0}
        if self.leaf(x,X,S,D,P,path):return True
        if (len(x)>=8 or not P) and self.terminal<self.max_lp and X.bit_length()+D.bit_length()>=2200:
            self.terminal+=1;L=solve(x,P,count_supply=True)
            print('lp',self.e,self.nodes,self.terminal,len(x),L,flush=True)
            if isinstance(L[0],float) and L[0]>2401:
                self.H[path]=['lp',sorted(P),L[0]];return True
        if not P or len(x)>=13:
            self.first=['open',x, X.bit_length(),D.bit_length(),len(P)];return False
        p=max(P);v=0;D0=D
        while D0%p==0:v+=1;D0//=p
        n=B//(X*D0);ew=any(f%2 for _,f in x)
        self.H[path]=['split',p]
        for f in range(v,I.ilog(n,p)+1):
            if (not ew or not f%2) and block(p,f) and not self.visit(x+[(p,f)],f'{path}:{f}'):
                return False
        return True


if __name__=='__main__':
    for E in map(int,sys.argv[1:]):
        p=Pilot(E,limit=500,max_lp=12,timeout=300)
        ok=p.visit([(5,E)],str(E))
        print('ROOT',E,ok,p.nodes,p.terminal,p.first,flush=True)
        if ok:
            (HERE/f'HybridCandidate{E}.json').write_text(json.dumps(p.H,separators=(',',':'))+'\n',encoding='utf-8')

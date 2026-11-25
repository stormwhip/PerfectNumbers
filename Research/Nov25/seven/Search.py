"""Heuristic candidate generator; writes only sibling candidate files, never history."""
import argparse
from functools import cache
import gzip
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path
import random
import sys
import time
from Scout import H,HIST,CASES,load,scorer,arithmetic,sigma,valuation,nonsupport,pc

ROOT=HIST.parents[2]
NC=ROOT/'NightCache'
sys.path[:0]=[str(NC),str(NC/'flint-lib')]
from facts import Bank  # read-only mmap, hints only
import flint
from sympy import isprime
from sympy.ntheory.factor_ import pollard_pm1, pollard_rho
R=H.parents[1]
DB=json.loads(gzip.decompress((R/'OrderSupplyNext/OrderPrimeProofs.json.gz').read_bytes()))
BANK=Bank()
SMALL=[q for q in range(3,10001,2) if pc.prime64(q)]

@cache
def cached_q(q):
    if q<2**64:return pc.prime64(q)
    h=sha256(str(q).encode()).hexdigest()[:24]
    return str(q) in DB or any(f.is_file() for f in (NC/'ecpp-local'/f'{h}.json', R/'NightOrder/ECPP'/f'{h}.json.gz',R/'EveningTree/ECPP'/f'Prime{h}.json',R/'NightLowRoute/CertCache'/f'{h}.json', ROOT/'upstream/Research/OrderSupplyNext/certs'/f'{h}.json',HIST.parent/'NightLowRoute/CertCache'/f'{h}.json'))

@cache
def divisors(n):
    return {j for d in range(1,math.isqrt(n)+1) if not n%d for j in (d,n//d)}

@cache
def prime(q):
    return pc.prime64(q) if q<2**64 else q.bit_length()<=1400 and isprime(q)

@cache
def phi(z,n):
    return (z**n-1)//math.prod(phi(z,d) for d in divisors(n) if d!=n)

@cache
def split(n,level):
    if n<=1:return ()
    if prime(n):return (n,)
    if (r:=math.isqrt(n))**2==n:return split(r,level)
    if n.bit_length()>220 or not level:return ()
    if n.bit_length()<75:
        return tuple(int(p) for p,e in flint.fmpz(n).factor() if prime(int(p)))
    r=pollard_pm1(n,B=1500,retries=0) or pollard_rho(n,max_steps=3000,retries=1,seed=1)
    return split(r,level-1)+split(n//r,level-1) if r else ()

@cache
def hints(z,f,level):
    if z.bit_length()*f>14000:return ()
    S=arithmetic(z,f)
    hds=divisors(f+1)-{1}; out=set();
    for d in hds:
        T=phi(z,d); ds={q for q in BANK.lookup(z,d) if q>2 and T%q==0 and prime(q)}
        ds.update(q for q in SMALL if T%q==0)
        rr=nonsupport(T,2*math.prod(ds));ds.update(split(rr,level));out.update(q for q in ds if S%q==0)
    return tuple(sorted(out))


def descendant(q,z,ow):
    while z in ow and z!=q:z=ow[z]
    return z==q


def trim(row,prices,target=2400.00001,minimum=0,seconds=80):
    ow=dict(row['owners']); weights=dict(prices); r=dict(row); deadline=time.monotonic()+seconds
    limit=max(target,minimum)
    def calc(ow):
        r['owners']=list(ow.items());return min(scorer(r,weights)[0].values())
    def drop(group):
        bad=set(group);prev=-1
        while len(bad)!=prev:
            prev=len(bad);bad.update(q for q,z in ow.items() if z in bad)
        return {q:z for q,z in ow.items() if q not in bad}
    for key in (lambda q:(cached_q(q),-q.bit_length()),lambda q:(q.bit_length(),q)):
        queue=[sorted(ow,key=key)]
        while queue and time.monotonic()<deadline:
            v=[q for q in queue.pop() if q in ow]
            if not v:continue
            cand=drop(v)
            if calc(cand)>=limit:ow=cand
            elif len(v)>1:queue.extend((v[len(v)//2:],v[:len(v)//2]))
    r['owners']=sorted(ow.items());return r


def search(p,e,seconds=300,seed=1,weight=None,start=None,deny=(),max_new_bits=1400,target=2400.000001,do_trim=True):
    rng=random.Random(seed);t=time.monotonic();r=start or load(p,e);roots=set(r['roots']);ow=dict(r['owners']);A=sigma(p,e)*p
    blocked=set(deny)-roots
    while (extra:={q for q,z in ow.items() if z in blocked and q not in blocked}):blocked.update(extra)
    ow={q:z for q,z in ow.items() if q not in blocked}
    r={k:v for k,v in r.items() if k in ('p','e','roots','owners','head')}; r['head']=max(120,r['head']); W=weight or {};best=float('-inf');bestrow=None; bestw={}; seen=set(); cycling=0; outer=0; fresh={}
    def eval(ow,head=None):
        row=dict(r,owners=list(ow.items()),head=head or r['head']);return scorer(row,W)
    while time.monotonic()-t<seconds:
        outer+=1
        values,tr=eval(ow); m=min(values,key=values.get); v=values[m]; states=tr(m)
        if v>best+1e-7:
            best=v;bestrow=dict(r,owners=sorted(ow.items()));bestw=dict(W);cycling=0
            print('best',p,e,outer,round(v,6),m,len(ow),len(states),round(time.monotonic()-t,1),flush=True)
            if v>target:break
        new=[]; switches=[]
        U=A*math.prod(ow)
        for mode in sorted(values,key=values.get)[:1+min(4,cycling)]:
            for z,(h,f,k,w) in (states if mode==m else tr(mode)).items():
                if w is False:
                    r['head']=min(512,r['head']+12);continue
                if (z,f) in seen:continue
                seen.add((z,f))
                for q in hints(z,f,2):
                    if q in roots or q in blocked or (q.bit_length()>max_new_bits and not cached_q(q)) or A%q==0 or ow.get(q)==z:continue
                    if q in ow:
                        if not descendant(q,z,ow):switches.append((q,z))
                    else:new.append((q,z))
        for q,z in new:
            ow.setdefault(q,z)
        if new:continue
        for q,z in switches:
            fresh.setdefault(q,set()).add(z)
        for z,(h,f,k,w) in states.items():
            if w is False:continue
            S=arithmetic(z,f); keep=S//nonsupport(S,U)
            if keep==1:continue
            for q in ow:
                if q!=z and ow[q]!=z and keep%q==0 and not descendant(q,z,ow):fresh.setdefault(q,set()).add(z)
        if not switches:
            for q,zs in fresh.items():
                for z in zs:
                    if z in states and z in ow.keys()|roots and ow.get(q)!=z and not descendant(q,z,ow):
                        S=arithmetic(z,states[z][1]);
                        if S%q==0:switches.append((q,z))
        if switches:
            improvements=[]
            for q,z in sorted(set(switches),reverse=True)[:70]:
                n=ow|{q:z}; val=min(eval(n)[0].values());improvements.append((val,q,z))
                if time.monotonic()-t>seconds:break
            if improvements:
                b,q,z=max(improvements)
                if b>v+1e-7:ow[q]=z;continue
                if cycling%4==3:
                    _,q,z=rng.choice(sorted(improvements,reverse=True)[:6]); ow[q]=z;seen.clear(); cycling+=1;continue
        cycling+=1
        if cycling in (2,4,5):seen.clear();continue
        if cycling>6 or (len(ow)>5000):
            ow=dict(bestrow['owners']); choose=rng.sample(tuple(ow),min(len(ow),3+cycling%10)); lose=set(choose); last=-1
            while len(lose)!=last:
                last=len(lose);lose.update(q for q,z in ow.items() if z in lose)
            for q in lose:ow.pop(q,None)
            seen.clear(); continue
    if bestrow is None:return
    fname=H/f'best-{p}x{e}-{seed}.json'
    den=8 if bestw else 1
    if den>1:bestrow.update(den=den,rho=[[q,round(den*w)] for q,w in bestw.items() if w and q in set(bestrow['roots'])|dict(bestrow['owners']).keys()])
    bestrow['scout']=best
    fname.write_text(json.dumps(bestrow,separators=(',',':'))+'\n',encoding='utf-8')
    print('saved',fname,best,flush=True)
    if do_trim and best>2400.000001:
        pkt=trim(bestrow,bestw); names=set(pkt['roots'])|dict(pkt['owners']).keys()
        if 'rho' in pkt:pkt['rho']=[(q,w) for q,w in pkt['rho'] if q in names]
        missing=sorted(q for q in names if not cached_q(q)); print('trimmed',len(names),'missing',len(missing),[(str(q),q.bit_length()) for q in missing],flush=True)
        pkt['scout']=min(scorer(pkt,bestw)[0].values()); pkt['missing']=missing
        (H/f'candidate-{p}x{e}-{seed}.json').write_text(json.dumps(pkt,separators=(',',':'))+'\n',encoding='utf-8')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('case');ap.add_argument('--seconds',type=int,default=300);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--start',type=Path);ap.add_argument('--deny',type=int,action='append',default=[]);ap.add_argument('--max-new-bits',type=int,default=1400);ap.add_argument('--target',type=float,default=2400.000001);ap.add_argument('--no-trim',action='store_true');a=ap.parse_args();p,e=map(int,a.case.split('x'))
    st=json.loads(a.start.read_bytes()) if a.start else None; W={q:w/st['den'] for q,w in st.get('rho',[])} if st else None
    search(p,e,a.seconds,a.seed,W,st,a.deny,a.max_new_bits,a.target,not a.no_trim)

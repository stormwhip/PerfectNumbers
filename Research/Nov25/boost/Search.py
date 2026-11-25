"""Bounded ownership refinement, adapted from Nov25/seven/Search.py."""
import argparse, json, math, random, sys, time
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from BoostScore import H,ROOT,HIST,ORDER,arithmetic,load,minimum,nonsupport,pc,scorer,sigma
from Pack import known,pack

CACHE=ROOT/'NightCache'
sys.path[:0]=[str(CACHE),str(CACHE/'flint-lib')]
from facts import Bank
import flint
from sympy.ntheory.factor_ import pollard_pm1,pollard_rho
BANK=Bank()
SMALL=[q for q in range(3,10001,2) if pc.prime64(q)]
SMP=math.prod(SMALL)

@lru_cache(maxsize=9000)
def divisors(n):return {j for d in range(1,math.isqrt(n)+1) if not n%d for j in (d,n//d)}

@lru_cache(maxsize=18000)
def prime(q):
    return pc.prime64(q) if q<2**64 else q.bit_length()<=2100 and bool(flint.fmpz(q).is_probable_prime())

@lru_cache(maxsize=9000)
def phi(z,n):return (z**n-1)//math.prod(phi(z,d) for d in divisors(n) if d!=n)

@lru_cache(maxsize=9000)
def split(n,level):
    if n<=1:return ()
    if prime(n):return (n,)
    if (r:=math.isqrt(n))**2==n:return split(r,level)
    if n.bit_length()>330 or not level:return ()
    if n.bit_length()<70:
        return tuple(int(p) for p,e in flint.fmpz(n).factor() if prime(int(p)))
    r=pollard_pm1(n,B=(450 if n.bit_length()>160 else 1300),retries=0) or pollard_rho(n,max_steps=1800,retries=1,seed=1)
    return split(r,level-1)+split(n//r,level-1) if r else ()

@lru_cache(maxsize=8000)
def hints(z,f):
    if z.bit_length()*f>14000:return ()
    S=arithmetic(z,f); out=set()
    for d in divisors(f+1)-{1}:
        T=phi(z,d); ds={q for q in BANK.lookup(z,d) if q>2 and T%q==0 and prime(q)}
        sm=math.gcd(T,SMP)
        if sm!=1:ds.update(q for q in SMALL if sm%q==0)
        rr=nonsupport(T,2*math.prod(ds));ds.update(split(rr,2));out.update(q for q in ds if S%q==0)
    return tuple(sorted(out))


def descendant(q,z,ow):
    while z in ow and z!=q:z=ow[z]
    return z==q


def lost(ow,group):
    bad=set(group); prev=-1
    while len(bad)!=prev:
        prev=len(bad);bad.update(q for q,z in ow.items() if z in bad)
    return {q:z for q,z in ow.items() if q not in bad}


def trim(row,seconds=45,target=2400.0000001):
    ow=dict(row['owners']); r=dict(row); deadline=time.monotonic()+seconds
    W={q:u/r['den'] for q,u in r.get('rho',[])}
    def calc(ow):return minimum(dict(r,owners=list(ow.items())),W)
    already=[q for q in ow if known(q)]; un=[q for q in ow if not known(q)]
    for order in (un,already):
        queue=[sorted(order,key=lambda q:(-q.bit_length(),q))]
        while queue and time.monotonic()<deadline:
            v=[q for q in queue.pop() if q in ow]
            if not v:continue
            cand=lost(ow,v)
            if calc(cand)>=target:ow=cand
            elif len(v)>1:queue.extend((v[len(v)//2:],v[:len(v)//2]))
    r['owners']=sorted(ow.items())
    if 'rho'in r:r['rho']=[(q,u) for q,u in r['rho'] if q in ow or q in r['roots']]
    return r


def store(out,row):
    tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(row,separators=(',',':'))+'\n',encoding='utf8');tmp.replace(out)


def search(start,seconds,seed,label,policy,extra_paths=()):
    rng=random.Random(seed); t=time.monotonic(); deadline=t+seconds; r=load(start);p,e=r['p'],r['e']; roots=set(r['roots']);ow=dict(r['owners']);A=sigma(p,e)*p
    r['head']=max(120,r['head']); W={q:u/r['den'] for q,u in r.get('rho',[])}
    baseline=minimum(r,W);best=-math.inf;bestrow=None;cycling=0;outer=0; fresh=defaultdict(set); used=set(); visits=defaultdict(int)
    out=H/f'best-{p}x{e}-{label}.json'; cand=H/f'candidate-{p}x{e}-{label}.json'
    bank=defaultdict(set)
    for f in HIST.glob(f'*{p}_{e}.json'):
        try:d=load(f)
        except (KeyError,ValueError,TypeError,ZeroDivisionError):continue
        for q,z in d['owners']:bank[z].add(q)
    for f in extra_paths:
        for z,d,qs in json.loads(f.read_bytes()):bank[z].update(qs)
    print('start',p,e,start.name,'initial',baseline,'owners',len(ow),'policy',policy,flush=True)
    def ev(ow,extra=None):return scorer(dict(r,owners=list(ow.items())),W,extra)
    def score(ow):return minimum(dict(r,owners=list(ow.items())),W)
    def snap(ow,score):
        x=dict(r,owners=sorted(ow.items()),scout=score,source=start.name)
        if 'rho'in x:x['rho']=[(q,u) for q,u in x['rho'] if q in ow or q in roots]
        return x
    while time.monotonic()<deadline:
        outer+=1
        if outer%40==0:sigma.cache_clear()
        values,tr=ev(ow); m=min(values,key=values.get); v=values[m]; states=tr(m)
        if v>best+1e-8:
            best=v;bestrow=snap(ow,v);cycling=0;store(out,bestrow)
            print('best',p,e,outer,round(v,6),m,len(ow),len(states),round(time.monotonic()-t,1),flush=True)
            if v>2400.000001:
                store(cand,bestrow);tr.clear();break
        U=A*math.prod(ow); vv=ow.keys()|roots
        new=defaultdict(set); switches=set(); ranks={}
        modes=sorted(values,key=values.get)[:min(len(values),1+cycling//2)]
        def use(states,alt=False):
            if policy!='plain':
                states=dict(sorted(states.items(),key=lambda kv: -kv[0].bit_length()*kv[1][1]))
            for z,(h,f,k,w) in states.items():
                if w is False:
                    if not alt:r['head']=min(512,r['head']+16)
                    continue
                if not f or time.monotonic()>deadline:continue
                S=arithmetic(z,f)
                if (z,f) not in used:
                    used.add((z,f)); Q=set(hints(z,f)) | {q for q in bank[z] if S%q==0 and prime(q)}
                else:Q=set()
                keep=math.gcd(S,U)
                if keep>1:
                    Q.update(q for q in ow if keep%q==0)
                for q in Q:
                    if A%q==0 or q in roots or ow.get(q)==z:continue
                    if q in ow:
                        if not descendant(q,z,ow):
                            fresh[q].add(z);switches.add((q,z));ranks[q,z]=(not alt,q in states,q.bit_length())
                    else:new[q].add(z)
        for mode in modes:use(states if mode==m else tr(mode))
        tr.clear()
        # Learn not just the minimizing rows, but near-tied rows exposed by skipping a small cell.
        if policy!='plain' and not new and cycling%3==1 and r['head']>=120:
            cells=[(z,f) for z,(_,f,_,w) in states.items() if w is not False and f and (z,f) not in visits]
            cells=sorted(cells,key=lambda zf:(zf[0].bit_length()*zf[1],zf[0]))[:4]
            for z,f in cells:
                if time.monotonic()>deadline:break
                alt,tt=ev(ow,{z:{f}}); aa=min(alt,key=alt.get)
                if alt[aa]<v+90:use(tt(aa),True)
                tt.clear();visits[z,f]+=1
        if new:
            adds={q:min(zs,key=lambda z:(z not in states,z)) for q,zs in new.items()}; n=ow|adds
            for q,zs in new.items():fresh[q].update(zs)
            nv=score(n)
            if nv>=v-1e-7 or policy=='plain':ow=n;continue
            if len(adds)>1:
                choices=[(score(ow|{q:z}),q,z) for q,z in sorted(adds.items(),key=lambda qz:qz[0].bit_length(),reverse=True)[:min(15,len(adds))] if time.monotonic()<deadline]
                if choices and (bq:=max(choices))[0]>v+1e-7:ow[bq[1]]=bq[2];continue
        if cycling>0:
            for q,zs in fresh.items():
                if q not in ow:continue
                for z in zs:
                    if z in vv and z in states and ow.get(q)!=z and not descendant(q,z,ow) and states[z][3] is not False and arithmetic(z,states[z][1])%q==0:
                        switches.add((q,z))
        improvements=[]
        for q,z in sorted(switches,key=lambda qz:ranks.get(qz,(False,False,qz[0].bit_length())),reverse=True)[:(38 if policy!='plain' else 70)]:
            if time.monotonic()>deadline:break
            n=ow|{q:z}; improvements.append((score(n),q,z))
        if improvements:
            b,q,z=max(improvements)
            if b>v+1e-7:ow[q]=z;continue
            if cycling%4==3:
                _,q,z=rng.choice(sorted(improvements,reverse=True)[:5]);ow[q]=z;cycling+=1;continue
        if policy!='plain' and cycling%3!=2:
            # Removing exotic, inactive labels can restore cofactor charge at a winning cell.
            children=set(ow.values())
            deletions=[]
            for z,(h,f,k,w) in states.items():
                if w is False:continue
                g=math.gcd(arithmetic(z,f),U)
                if g>1:
                    deletions.extend(q for q in ow if q not in states and q not in children and g%q==0)
            for q in sorted(set(deletions),reverse=True)[:20]:
                if time.monotonic()>deadline:break
                n=ow.copy();n.pop(q);b=score(n)
                if b>v+1e-7:ow=n;break
            else:q=None
            if q is not None:continue
        cycling+=1
        if cycling>5:
            ow=dict(bestrow['owners']); labels=set(ow); active=labels&states.keys()
            pool=list(active if cycling%2 and active else labels); cut=rng.sample(pool,min(len(pool),1+cycling%6));ow=lost(ow,cut)
            used.clear()
    print('finished',p,e,'baseline',baseline,'best',best,'rounds',outer,'sec',round(time.monotonic()-t,2),flush=True)
    if cand.is_file():
        row=trim(bestrow,seconds=35);store(cand,row);pack(cand)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('case');ap.add_argument('--seconds',type=int,default=365);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--label',default='refine1');ap.add_argument('--policy',choices=('plain','enhanced'),default='enhanced');ap.add_argument('--start',type=Path);ap.add_argument('--hints',type=Path,action='append',default=[]);a=ap.parse_args()
    p,e=map(int,a.case.split('x'));search(a.start or HIST/f'Intra{p}_{e}.json',a.seconds,a.seed,a.label,a.policy,a.hints)

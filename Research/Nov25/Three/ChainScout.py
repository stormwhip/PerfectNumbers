"""Discovery: inject read-only factor hints in the existing NightThree tree.

Nothing output here is credited without a separate plain-dict NightThree replay
and independent primality witnesses. External sibling caches are optional.
"""
import argparse
from collections import defaultdict
from functools import cache
from hashlib import sha256
import json
from math import gcd, isqrt, prod
from pathlib import Path
import sys
from time import monotonic

from Scout import E, J, V, HERE, WORK, frontier, roots

LOCAL = WORK.parent / 'NightCache'
OLD = WORK.parent / 'overnight/Research/NightThree'
FLAGS = dict(boost=True, reduced=True, parity=True, internal=True, exception=True)


@cache
def divisors(x):
    return tuple(sorted({y for d in range(1, isqrt(x)+1) if x%d==0 for y in (d, x//d)}))


@cache
def phi(r, h):
    return (r**h-1)//prod(phi(r,d) for d in divisors(h)[:-1])


@cache
def chunks():
    ps = J.I.PS
    return [(prod(ps[i:i+128]), ps[i:i+128]) for i in range(0,len(ps),128)]


@cache
def bank():
    if not (LOCAL/'facts.idx').exists():
        return None
    sys.path.append(str(LOCAL))
    from facts import Bank
    return Bank()


@cache
def edge_bank():
    db = defaultdict(set)
    for p in OLD.glob('*DB.json'):
        for number, row in json.loads(p.read_bytes()).items():
            db[int(number)].update(map(int, row['f']))
    return db


@cache
def probable(n):
    if n<2**64:
        return E.mr(n)
    from sympy import isprime
    return bool(isprime(n))


@cache
def block(r, h, max_bits):
    n = phi(r,h)
    out = set()
    def strip(z):
        nonlocal n
        while n%z==0:
            out.add(z)
            n//=z
    for p, ps in chunks():
        if n == 1:
            break
        g=gcd(n,p)
        if g>1:
            for z in ps:
                if g%z==0:
                    strip(z)
    b = bank()
    for z in sorted(set(b.lookup(r,h) if b else []) | edge_bank().get(n,set())):
        if z>1 and n%z==0 and z.bit_length()<=max_bits and probable(z):
            strip(z)
    if n>1 and n.bit_length()<=max_bits and probable(n):
        out.add(n)
        n=1
    return frozenset(z for z in out if z>3 and z not in E.BANNED),n


@cache
def hints(r, f, max_bits):
    return frozenset().union(*(block(r,h,max_bits)[0] for h in divisors(f+1)[1:]))


class StopSearch(RuntimeError):
    pass


class EdgeProbe:
    def __init__(self, max_bits, max_requests, stop):
        self.edges={}; self.requests=0; self.max_bits=max_bits; self.max_requests=max_requests; self.stop=stop
    def get(self, key, alt=None):
        self.requests+=1
        if self.requests>self.max_requests or monotonic()>self.stop:
            raise StopSearch('request or elapsed cap')
        if key[0]==3:
            return ()
        if key not in self.edges:
            self.edges[key]=hints(*key,self.max_bits)
        return self.edges[key]


def window_run(e, fs, s, high, probe):
    try:
        flags = dict(reduced=True, internal=True, high=True) if high else FLAGS
        return dict(ok=True, stats=V.independent(e, fs, probe, s, **flags)) if s else dict(ok=True,stats={})
    except (StopSearch, ValueError) as ex:
        return dict(ok=False, status=str(ex), requests=probe.requests, edges=len(probe.edges))


def run(e,args):
    fs=roots(e)
    one, high=J.audit(e,fs)
    rr=dict(e=e, root=list(map(str,fs)), one=len(one), high=len(high), trials=[])
    if (one and min(one)==0) or (high and min(high)<=7):
        rr['status']='short cells require generic tree'
        return rr,None
    alls={}; wp=[]
    span=args.width or max(1,len(one),len(high))
    ranges=[(s[i:i+span], h) for s,h in ((one,False),(high,True)) for i in range(0,len(s),span)]
    stop=monotonic()+args.seconds
    for window, hi in ranges:
        probe=EdgeProbe(args.bits,args.requests,stop)
        res=window_run(e,fs,window,hi,probe)
        rr['trials'].append(dict(low=min(window),top=max(window),high=hi,**res))
        if res['ok']:
            for key, val in probe.edges.items():
                alls.setdefault(key,set()).update(val)
            if not hi:wp.append(window)
        elif args.stop_first or monotonic()>stop:
            break
    if len(rr['trials'])==len(ranges) and all(r['ok'] for r in rr['trials']):
        row=dict(e=e,root=rr['root'], edges=[[str(r),f,str(z)] for (r,f),zs in sorted(alls.items()) for z in sorted(zs)],windows=wp,**FLAGS)
        rr['complete_candidate']=True
        return rr,row
    return rr,None


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only',nargs='+',type=int,required=True)
    p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--width',type=int,default=0)
    p.add_argument('--requests',type=int,default=15000)
    p.add_argument('--bits',type=int,default=360)
    p.add_argument('--stop-first',action='store_true')
    p.add_argument('--label',default='ChainScout')
    a=p.parse_args()
    if not (set(a.only)<=frontier() and a.label.isidentifier()):
        raise ValueError('outside fixed frontier or invalid output label')
    rows=[]; proofs=[]
    for e in a.only:
        row,proof=run(e,a); rows.append(row); print(e,len(row['trials']),sum(t['ok'] for t in row['trials']),row.get('status'),flush=True)
        (HERE/(a.label+'.json')).write_text(json.dumps(rows,indent=1)+'\n',encoding='utf8')
        if proof is not None:
            proofs.append(proof)
            (HERE/(a.label+'Candidates.json')).write_text(json.dumps(proofs,separators=(',',':'))+'\n',encoding='utf8')


if __name__=='__main__':
    main()

"""Budgeted exact forest discovery. Partial trees are NOT total certificates.

Finds candidate leaves; primality is sealed later and independent replay decides
acceptance. Logs only per-fiber summaries. An unresolved node is serialized as
null, so stock TreeCheck cannot accidentally accept a partial object.
"""
import argparse
import json
from math import prod
from pathlib import Path
import sys
from time import monotonic

from Probe import Bank, Finder, C, B, floor10, pivot_cases


def direct(s):
    return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X


class Search:
    def __init__(self,finder,args):
        self.finder,self.args=finder,args
        self.until=None
        self.calls=0
        self.unresolved=[]

    def factors(self,q,f):
        if q.bit_length()*(f+1)>self.args.max_bits:
            return []
        return self.finder.factors(q,f)

    def growth(self,s,roots):
        owners={}
        best=(0,(),{})
        for _ in range(self.args.iterations+1):
            if monotonic()>self.until: break
            forest=C.Forest(s,roots,owners.items(),self.args.head,record=True)
            value,mark=forest.lower()
            if value>best[0]: best=(value,roots,dict(owners))
            if value>B:
                return {'type':'forest','roots':roots,'owners':sorted(owners.items()),'head':self.args.head},best
            growth={}
            for q,f,r in forest.witness(mark):
                if not r or monotonic()>self.until: continue
                for z in self.factors(q,f):
                    if z not in s.bad and z not in s.rows and s.D%z and z not in owners and z not in roots:
                        growth.setdefault(z,q)
            if not growth: break
            owners.update(growth)
        return None,best

    def search(self,s,depth):
        if monotonic()>self.until or self.calls>=self.args.nodes:
            self.unresolved.append((list(s.rows.items()),None)); return None
        self.calls+=1
        roots=sorted({z for q,f in s.rows.items() for z in self.factors(q,f) if z not in s.rows and z not in s.bad and s.D%z==0})
        leaf,best=self.growth(s,roots)
        if leaf is not None: return leaf
        if not depth or not roots or monotonic()>self.until or self.calls>=self.args.nodes:
            self.unresolved.append((list(s.rows.items()),floor10(best[0] or s.base))); return None
        for pivot in reversed(roots):
            n=0; rows=[]
            for v,s2 in pivot_cases(s,pivot):
                n+=1
                if n>self.args.fanout:break
                rows.append((v,s2))
            if n>self.args.fanout:continue
            return {'type':'split','q':pivot,'cases':{str(v):self.search(s2,depth-1) for v,s2 in rows}}
        self.unresolved.append((list(s.rows.items()),floor10(best[0] or s.base))); return None


def weight(t):
    if t is None:return 0,0,1
    if t['type']=='forest':return 1,0,0
    out=[0,1,0]
    for z in t['cases'].values():
        for j,v in enumerate(weight(z)):out[j]+=v
    return tuple(out)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('p',type=int);p.add_argument('e',type=int)
    p.add_argument('--index',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--pivot',type=int);p.add_argument('--fiber',action='append',type=int)
    p.add_argument('--head',default=100,type=int);p.add_argument('--iterations',default=6,type=int)
    p.add_argument('--depth',default=2,type=int);p.add_argument('--seconds',default=20,type=int,help='discovery budget per initial fiber')
    p.add_argument('--nodes',default=50,type=int);p.add_argument('--fanout',default=24,type=int)
    p.add_argument('--smooth-bits',default=0,type=int);p.add_argument('--max-bits',default=14000,type=int)
    a=p.parse_args()
    f=Finder(Bank(a.index),a.smooth_bits);search=Search(f,a)
    s=C.State([(a.p,a.e)]);pivot=a.pivot or max(f.factors(a.p,a.e));assert not direct(s) and s.D%pivot==0
    tree={'type':'split','q':pivot,'cases':{}}; open_fibers={}
    for v,s2 in pivot_cases(s,pivot):
        if a.fiber and v not in a.fiber:
            tree['cases'][str(v)]=None;continue
        search.until=monotonic()+a.seconds;search.calls=0;search.unresolved=[]
        subtree=search.search(s2,a.depth);tree['cases'][str(v)]=subtree
        counts=weight(subtree)
        print('FIBER',v,'forest/split/open',counts,'calls',search.calls,flush=True)
        if search.unresolved:open_fibers[str(v)]=search.unresolved
        raw={'p':a.p,'e':a.e,'tree':tree,'unresolved':open_fibers}
        temp=a.out.with_suffix('.tmp');temp.write_text(json.dumps(raw,separators=(',',':')),encoding='utf-8');temp.replace(a.out)
    print('COUNTS',weight(tree),flush=True)


if __name__=='__main__':main()

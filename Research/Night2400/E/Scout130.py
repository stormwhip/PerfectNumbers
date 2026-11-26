"""Budgeted discovery for open descendants of a candidate, not evidence."""
import argparse
import json
from math import prod
from pathlib import Path
import sys
from time import monotonic

from Verify130 import H, R, C, B, floor10
sys.path.insert(0, str(R/'Session20261126'))
from Discover import Finder, Bank


def possible(s,q):
    h=C.valuation(s.D,q); f=h; size=s.base
    while size<=B:
        if s.possible(q,f,h):
            t=C.State([*s.rows.items(),(q,f)])
            if not t.conflict and t.base<=B and prod(C.sigma(z,e) for z,e in t.rows.items())<=2*t.X:
                yield f,t
        f+=1;size*=q


class Hunt:
    def __init__(self,a):
        self.a=a
        self.finder=Finder(Bank(a.index),a.smooth_bits)
        self.hints=json.loads((H/a.hints).read_bytes()) if a.hints else {}

    def factors(self,z,f):
        if z.bit_length()*(f+1)<=self.a.max_bits:
            qs=set(self.finder.factors(z,f))|set(self.hints.get(f'{z}:{f}',[]))
            return [q for q in sorted(qs) if 2<q and q.bit_length()<=self.a.prime_bits and C.sigma(z,f)%q==0]
        return []

    def grow(self,s,roots,deadline):
        o={};best=0;seen=set();h=self.a.head
        for _ in range(self.a.rounds):
            if monotonic()>deadline:break
            forest=C.Forest(s,roots,o.items(),h,record=True); val,mark=forest.lower(); best=max(best,val)
            if val>B:return dict(type='forest',roots=roots,owners=sorted(o.items()),head=h),best
            cand=[]; old_head=h
            for q,e,r in forest.witness(mark):
                if r:cand.append((q,e))
                elif 2*h<=1024 and q.bit_length()*e<8000:h=min(1024,2*h)
            add={}
            for q,e in cand:
                if (q,e) in seen:continue
                seen.add((q,e))
                for z in self.factors(q,e):
                    if z not in s.bad and z not in s.rows and z not in o and z not in roots and s.D%z:
                        add.setdefault(z,q)
                if monotonic()>deadline:break
            if not add and old_head==h:return None,best
            o.update(add)
        return None,best

    def descend(self,s,depth,deadline):
        roots=sorted({q for z,f in s.rows.items() for q in self.factors(z,f) if q not in s.bad and q not in s.rows and s.D%q==0})
        t,b=self.grow(s,roots,min(deadline,monotonic()+self.a.growth))
        if t:return t,floor10(b)
        if depth==0 or monotonic()>deadline:return None,floor10(b or s.base)
        pivots=[]
        for q in reversed(roots):
            cases=list(possible(s,q))
            if len(cases)<=self.a.fanout:pivots.append((len(cases),-q,cases))
            if self.a.pivot_rank==0 and pivots:break
        if not pivots:return None,floor10(b or s.base)
        _,q,cases=sorted(pivots)[min(self.a.pivot_rank,len(pivots)-1)];q=-q
        out={}
        for i,(f,r) in enumerate(cases):
            next_deadline=monotonic()+max(0,deadline-monotonic())/(len(cases)-i)
            out[str(f)]=None if monotonic()>deadline else self.descend(r,depth-1,next_deadline)[0]
        return dict(type='split',q=q,cases=out),floor10(b or s.base)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--out',required=True)
    p.add_argument('--index',type=Path,required=True);p.add_argument('--fiber',type=int,action='append',required=True)
    p.add_argument('--seconds',type=int,default=12);p.add_argument('--growth',type=int,default=5);p.add_argument('--depth',type=int,default=1)
    p.add_argument('--head',type=int,default=64);p.add_argument('--rounds',type=int,default=60)
    p.add_argument('--fanout',type=int,default=30);p.add_argument('--pivot-rank',type=int,default=0)
    p.add_argument('--smooth-bits',type=int,default=0);p.add_argument('--max-bits',type=int,default=16000)
    p.add_argument('--prime-bits',type=int,default=850);p.add_argument('--least',type=int,default=3);p.add_argument('--hints')
    a=p.parse_args();hunt=Hunt(a);d=json.loads((H/a.input).read_bytes());root=d['tree'];q=root['q'];assert (d['p'],d['e'])==(7,130)
    for k in list(root['cases']):
        if int(k) not in a.fiber:root['cases'][k]=None
    def walk(t,path):
        if t is None or t['type']=='open':
            f=tuple(e for _,e in path[1:]);
            if len(f)>a.least:return t
            new,b=hunt.descend(C.State(path),a.depth,monotonic()+a.seconds)
            print(f,b,(new or {}).get('type','open'),flush=True)
            return new
        if t['type']=='split':
            for f,n in t['cases'].items():t['cases'][f]=walk(n,path+[(t['q'],int(f))])
        return t
    for f in map(str,a.fiber):
        root['cases'][f]=walk(root['cases'][f],[(7,130),(q,int(f))]); tmp=(H/a.out).with_suffix('.tmp');tmp.write_text(json.dumps(d,separators=(',',':')),encoding='utf8');tmp.replace(H/a.out)


if __name__=='__main__':main()

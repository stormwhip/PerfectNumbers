"""Try known joint prices on existing open discovery paths. Not a proof checker."""
import argparse
from itertools import combinations
import json
from math import prod
import subprocess
import sys

from Verify130 import H, C, B, excludes


def attempt(parts, seconds):
    s=C.State(parts)
    if len(parts)>8:return None
    ds=[q**(e-C.valuation(s.S,q)) for q,e in parts]
    def cheap(j):
        M=prod(ds[i] for i in j)
        if s.fixed_euler:return s.X*M*M>B
        # A maximally supplying exponent-one prime surviving BOTH relaxations.
        if s.X*M*M<=B:return False
        return max(s.X*M*M*(2*M-1)//(M*M),s.base*(2*M-1))>B
    inds=[i for i,q in enumerate(ds) if q>1]
    trials=[list(j) for n in range(1,min(3,len(inds))+1) for j in combinations(inds,n) if cheap(j)]
    for j in trials:
        try:
            r=subprocess.run([sys.executable,'-B',str(H/'Price130.py'),'--worker'],input=json.dumps([parts,j]),
                             text=True,capture_output=True,timeout=seconds)
            if not r.returncode:return {'type':'price','targets':j}
        except subprocess.TimeoutExpired:pass
    return None


def main():
    if sys.argv[1:]==['--worker']:
        parts,j=json.load(sys.stdin);s=C.State(parts);excludes(parts,s.bad,j);return
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--out',required=True)
    p.add_argument('--seconds',type=int,default=4);p.add_argument('--fiber',type=int,action='append',required=True)
    a=p.parse_args(); d=json.loads((H/a.input).read_bytes());t=d['tree']
    def walk(node,pp):
        if node is None or node['type']=='open':
            r=attempt(pp,a.seconds)
            if r:print(tuple(f for _,f in pp[1:]),r,flush=True)
            return r or node
        if node['type']=='split':node['cases']={k:walk(v,[*pp,(node['q'],int(k))]) for k,v in node['cases'].items()}
        return node
    for k,v in t['cases'].items():
        if int(k) in a.fiber:t['cases'][k]=walk(v,[(7,130),(t['q'],int(k))])
    (H/a.out).write_text(json.dumps(d,separators=(',',':')),encoding='utf8')


if __name__=='__main__':main()

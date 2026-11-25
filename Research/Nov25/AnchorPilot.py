"""Replay an exact-source shared sigma anchor pilot, not an exclusion ledger."""
import argparse
import json
from math import gcd, prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Ledger import load_baseline, obligations
from SizePilot import I

FACTS = {
    (7283,2): (13,997,4093),
    (9059,2): (82074541,),
    (82074541,1): (2,11,11,339151),
    (82074541,2): (3,13,172723855447057),
    (172723855447057,2): (3,127,211,132619,1359859,2057773581637),
}
CASES=((3,82,167),(7,82,167),(11,82,167),(19,82,167),
       (7,330,7283),(13,330,7283),(11,646,9059),(19,646,9059))


def verified_facts():
    for (q,f),fs in FACTS.items():
        if not I.ec.prime64(q) or not all(I.ec.prime64(r) for r in fs) or prod(fs)!=I.sigma(q,f):
            raise ValueError(f'unverified {q}^{f} source')
    return FACTS


class Trace(I.Proof):
    def __init__(self,p,e,fs,facts,depth,valuation):
        super().__init__(p,e,fs,False,valuation)
        self.facts=facts
        self.depth_limit=depth
        self.first=None

    def visit(self,parts,X,S,ban):
        bank=self.pr
        active={r for z in parts for r in self.facts.get(z,()) if r>2}
        self.pr=sorted(set(bank)|active)
        try:
            ok=super().visit(parts,X,S,ban)
            if not ok and self.first is None:
                U=S//gcd(S,2*X)
                for q in self.pr:
                    U//=q**I.vp(U,q)
                self.first=dict(parts=parts,rough_digits=len(str(U)))
            return ok
        finally:
            self.pr=bank


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    facts=verified_facts()
    live=obligations(load_baseline()['remaining_shards'])
    if not all((p,e) in live and I.ec.prime64(q) and I.vp(I.sigma(p,e),q)==1 for p,e,q in CASES):
        raise ValueError('invalid target or shared anchor')
    out=[]
    for p,e,q in CASES:
        opts=[('base',[],{},4,False),('shared',[q],{},4,False)]
        if q==9059:
            opts.extend((('two_steps',[q],{k:v for k,v in facts.items() if k[0] in (9059,82074541)},7,True),
                         ('three_steps',[q],facts,7,True)))
        for label,fs,bank,depth,valuation in opts:
            tree=Trace(p,e,fs,bank,depth,valuation)
            ok=tree.prove()
            row=dict(p=p,e=e,q=q,mode=label,candidate=ok,nodes=tree.stats['nodes'],stats=tree.stats,first=tree.first)
            out.append(row)
            print(json.dumps(row),flush=True)
    if args.output:
        args.output.write_text(json.dumps(out,indent=1)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    if not __debug__:raise SystemExit('do not use -O')
    main()

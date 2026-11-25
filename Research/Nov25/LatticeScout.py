"""Discovery-only small-root trial for a few directed source rectangles.

FLINT chooses row combinations. Every proposed witness is checked using the
existing stdlib polynomial/division/Sturm verifier, independently of FLINT.
An unproved box is never removed. Do not use this as a full-domain certificate.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from math import gcd, log2
from pathlib import Path
import sys
from time import monotonic

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from DirectedSource import U,run
from DirectedExperiment import CASES


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--p',type=int,default=19)
    ap.add_argument('--s',type=int,action='append',required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--flint-path',type=Path)
    ap.add_argument('--seconds',type=int,default=240)
    args=ap.parse_args()
    if args.flint_path:sys.path.insert(0,str(args.flint_path))
    from flint import fmpz_mat
    from sympy import Poly,Symbol
    p,e,rs=next(k for k in CASES if k[0]==args.p)
    root=Symbol('t');origin=U.rect;stats=Counter();stored={};examples=[];start=monotonic()
    def check(C,c,z,T,lo,hi,cap):
        if not origin(C,c,z,T,lo,hi,32):
            stats['rectangle_empty']+=1;return False
        stats['rectangle_kept']+=1
        key=sha256('|'.join(map(str,(C,c,z,T,lo,hi))).encode('ascii')).hexdigest()
        if key in stored:return False
        if gcd(C,T)!=1 or monotonic()-start>args.seconds:return True
        one=[]
        for d,m in ((5,2),(7,3),(9,4),(12,6),(15,7),(18,9)):
            first,radius,mid,center,K,rows=U.LatticeLeaf.build(C,c,z,T,lo,hi,d,m)
            if radius<0:return False
            margin=log2(first)*m-sum(log2(abs(row[j]))+j*log2(K) for j,row in enumerate(rows))/d
            one.append(round(margin,1))
            if margin<-10:continue
            stats['lll_runs']+=1
            matrix=[[value*K**j for j,value in enumerate(row)] for row in rows]
            M,transform=fmpz_mat(matrix).lll(transform=True)
            for v,a in zip(M.tolist(),transform.tolist()):
                v=list(map(int,v))
                if sum(map(abs,v))>=first**m:continue
                coeff=[n//K**j for j,n in enumerate(v)]
                poly=Poly.from_list(coeff[::-1],gens=root)
                split=[[int(t.p),int(t.q)] for t,mul in poly.ground_roots().items() for _ in range(mul)]
                witness=[d,m,list(map(int,a)),split]
                if U.LatticeLeaf.verify(C,c,z,T,lo,hi,witness):
                    stored[key]=witness;stats['witness']+=1;return False
        if len(examples)<8:
            # Bit lengths expose why the inequalities are weak, without
            # bloating the diagnostic with repeated thousand-digit integers.
            examples.append(dict(c=c,C_bits=C.bit_length(),T_bits=T.bit_length(),lo_bits=lo.bit_length(),
                                 hi_bits=hi.bit_length(),margin_bits=one))
        return True
    U.rect=check
    out=[]
    for s in args.s:
        if monotonic()-start>args.seconds:break
        r=run(p,e,rs,min_s=s,max_s=s)
        r.update(p=p,e=e,s=s)
        out.append(r)
        print(json.dumps(r),flush=True)
        U.cand.cache_clear()
    obj=dict(results=out,examples=examples,stats=stats,witnesses=stored)
    args.output.write_text(json.dumps(obj,indent=1)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(stats=stats,examples=examples)),flush=True)

if __name__=='__main__':main()

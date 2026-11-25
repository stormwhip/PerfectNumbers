"""Run a representative set of Euler-source window diagnostics."""
import argparse
import json
from pathlib import Path
import sys
from time import monotonic

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Ledger import load_baseline, obligations
from DirectedSource import run,interval_factor,U

CASES=(
    (19,676,[629611,16678454203]),
    (7,1018,[85597,2539349]),
    (11,718,[8629]),
    (31,486,[380260554467939]),
)


def smalltest():
    # Independent bruteforce all candidates, exercising direct and cofactor loops.
    for z in range(7,220):
        for p in (3,7):
            for s in (0,1,2):
                y=p**s
                for lo,hi in ((3,19),(5,219),(43,145)):
                    for bad in ((),(5,11)):
                        truth=any(z%q==0 and q%4==1 and (q+1)%y==0 and (q+1)%(p*y)!=0
                                  and all((q+1)%b for b in bad) for q in range(lo,hi+1))
                        if truth and not interval_factor(z,y,p,lo,hi,bad,1):
                            raise AssertionError((z,p,y,lo,hi,bad))
                        if truth!=interval_factor(z,y,p,lo,hi,bad,1000):
                            raise AssertionError((z,p,y,lo,hi,bad,'direct'))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--p',type=int)
    ap.add_argument('--max-s',type=int,default=0)
    ap.add_argument('--min-s',type=int,default=0)
    ap.add_argument('--packet',type=Path,help='optional diagnostic array [p,e,[prime factors]]')
    ap.add_argument('--strategy',choices=('both','directed','control'),default='both')
    ap.add_argument('--raw',type=Path,help='write surviving exact s records outside the checkout')
    opt=ap.parse_args()
    if not __debug__:raise SystemExit('do not use -O')
    smalltest()
    live=obligations(load_baseline()['remaining_shards'])
    results=[]
    for p,e,rs in json.loads(opt.packet.read_bytes()) if opt.packet else CASES:
        if opt.p is not None and p!=opt.p:continue
        if (p,e) not in live:raise ValueError('invalid target')
        a=U.sig(p,e)
        anchors=sorted({q for q in rs if a%q==0 and (q>=2**64 or U.O.G.is_prime_det64(q))})
        base=None
        for label in ('control','directed') if opt.strategy=='both' else (opt.strategy,):
            now=monotonic();r=run(p,e,anchors,new=label=='directed',max_s=opt.max_s,min_s=opt.min_s)
            rr=r.get('open',[]);ss={x[0] for x in rr};
            if label=='directed' and base is not None and not ss<=base:raise ValueError('unexpected strengthening disagreement')
            base=ss
            results.append(dict(p=p,e=e,method=label,**r))
            print(json.dumps(dict(p=p,e=e,method=label,guard=r.get('guard'),open=len(rr),
                                  outer=sum(x[1] for x in rr),first=rr[:2],last=rr[-2:],
                                  full_domain=opt.min_s==0 and (opt.max_s==0 or opt.max_s>=e),
                                  anchors=anchors,seconds=round(monotonic()-now,3))),flush=True)
    if opt.raw:
        opt.raw.write_text(json.dumps(results,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':main()

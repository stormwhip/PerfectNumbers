"""Integer-only primitive-source and missing-index conditional cuts for p>3.
Read frozen ledger, write only stdout. No factorization or candidate LP.
"""
from math import gcd,isqrt
import json,sys
from pathlib import Path
from hashlib import sha256
B=10**2400
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[3]
raw=(root/'Research/Midday/Delta.json').read_bytes();j=json.loads(raw)
S=(19,7,11,31,13,3,5,17)

def floorcut(p,e,ell,external,cap_b=None):
    # If d=ord_q(r) divides (f+1)/ell, q divides the corresponding geometric sum.
    # r^f>r^(ell-1)(2Q/3)^ell, and b<=e-s. Source and root sigma multiply.
    P=p**e;A=(P*p-1)//(p-1)
    small=next(t for t in (3,5,7,11,13,17,19,23,29,31,37) if t!=p and t not in S[:S.index(p)])
    # (For all five roots, smallest allowed source is 3.)
    def impossible(s):
        Q=2*p**s-1
        if Q<=B.bit_length()+1:return False
        b=e-s if cap_b is None else min(cap_b,e-s)
        F=small**(ell-1)*(2*Q)**ell//3**ell
        if external:
            return p**(e-b)*A*F*F>B or P*A*Q*F>B
        return p**(e-b)*F*F>B or P*Q*F>B
    if not impossible(e):return None
    lo,hi=0,e
    while lo+1<hi:
        m=(lo+hi)//2
        if impossible(m):hi=m
        else:lo=m
    assert impossible(hi) and not impossible(hi-1)
    return hi

if __name__=='__main__':
    assert __debug__
    report={}
    for p in (7,11,13,19,31):
        es=sorted({e for r in j['remaining_shards'] if r['root']==p for e in r['remaining_actuals']}); rows=[]
        for e in es:
            cuts={}
            for n in sorted({3,5,p}):
                for ext in (False,True):
                    s=floorcut(p,e,n,ext)
                    if s is not None:cuts[f'{n}:{"outside_A" if ext else "all_sources"}']=s
            if cuts:rows.append({'e':e,'from_s':cuts})
        report[p]={'frozen_actuals':len(es),'covered_by_at_least_one_cut':len(rows),'rows':rows}
    print(json.dumps(dict(status='PARTIAL_ONLY',ledger_sha256=sha256(raw).hexdigest(),report=report,accepted_actuals=[]),indent=2))

"""Independent finite domain and endpoint audit for (3,12), Q=797161."""
import gzip
import hashlib
import json
from pathlib import Path
from math import gcd, isqrt, prod
import sys

H=Path(__file__).resolve().parent
R=H.parents[1]
B=10**2400
P=3
Q=797161
E=12
BAN=(19,7,11,31,13)
ARCHIVE=(
    ('Session20261126/LowBranches','4d746a1d6e913953761b0b07ec5df5a42bdbf89aaca2e345467005964c96bfa0'),
    ('FinalSprint/LowBranches','f9545a514eb6db321302d5090663b42d108babcf1497a9a0f780df3c4c604fc6'),
    ('FinalSprint/LowBranches/Wave2','4e5bfdec9fc6eafdf0a80078bd1c81526a234c82c0e689f7621408e2bbf0d1f2'),
    ('FinalSprint/LowBranches/Wave3','a12ff742b5f2c246b72cd0387ff5281beb7d540e5574ddac4bfcfb680463542e'),
    ('FinalSprint/LowBranches/Wave4','aa9afe7863e8ba7b38006645914c683f6d8df732058c78a408af2086ec77dc59'),
)


def sigma(q,f):return (q**(f+1)-1)//(q-1)


def vp(n,q):
    assert n>0 and q>1
    h=0
    while n%q==0:
        n//=q;h+=1
    return h


def independent():
    assert __debug__ and sigma(P,E)==Q and P**E <= B
    assert all(Q%d for d in range(2,isqrt(Q)+1))
    ok=set(); bad={}
    h=1
    while P**E*Q**h <= B:
        if h%2 and (h%4!=1 or Q%4!=1):
            bad[h]='Euler parity'
        else:
            X=P**E*Q**h
            Z=Q*sigma(Q,h)
            odd=Z//(1+h%2)
            assert odd%2==1
            if gcd(odd,prod(BAN))>1:
                bad[h]='forbidden divisor'
            elif vp(odd,P)>E or vp(odd,Q)>h:
                bad[h]='fixed valuation overflow'
            elif Z>2*X:
                bad[h]='excess abundancy'
            else:
                D=odd//(P**vp(odd,P)*Q**vp(odd,Q))
                if X*D>B:bad[h]='odd sum size'
                else:ok.add(h)
        h+=1
    assert P**E*Q**(h-1)<=B<P**E*Q**h
    assert set(range(1,h))==ok|bad.keys() and not ok&bad.keys()
    return ok,bad,h


def run(packets):
    full,pruned,tail=independent()
    archive=set();counts=[]
    for sub,s in ARCHIVE:
        raw=(R/sub/'Branches.json.gz').read_bytes()
        assert hashlib.sha256(raw).hexdigest()==s
        rows=[row for e,q,row in json.loads(gzip.decompress(raw))['roots'] if (e,q)==(E,Q)]
        assert len(rows)<=1
        current={int(h) for row in rows for h in row}
        assert current<=full and not current&archive
        archive.update(current);counts.append(len(current))
    assert counts==[90,2,4,0,0] and full-archive=={1,2,66,96}
    complete=set();secondary_only={}
    if packets:
        sys.path.insert(0,str(H))
        import Verify
        for path in packets:
            result=Verify.verify(path)
            q,f=result['primary'];assert q==Q and f in full-archive and f not in secondary_only and f not in complete
            if result['full_fiber']:complete.add(f)
            else:secondary_only[f]=result['covered']
    print('INDEPENDENT DOMAIN PASS',json.dumps(dict(raw_upper=tail-1,first_size_tail=tail,domain=len(full),
          old_counts=counts,old_exclusions=len(archive),new_primary_exclusions=sorted(complete),
          secondary_only=secondary_only,remaining=sorted(full-archive-complete),
          complete_exponent=not full-archive-complete)),flush=True)


if __name__=='__main__':
    run(list(map(Path,sys.argv[1:])))

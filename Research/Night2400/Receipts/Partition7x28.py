"""Independent exact D2 canonical support, abundancy and optional pivot diagnostic."""
from fractions import Fraction
from math import gcd, prod
from pathlib import Path
import gzip,json
R=Path('Research')
S=(19,7,11,31,13,3,5,17)
p,e=7,28
X=p**e
B=10**2400
Q=71316922984999
roots=(59,127540261,Q)

def sigma(a,f):return sum(a**j for j in range(f+1))
def val(a,q):
    v=0
    while a%q==0:
        v+=1;a//=q
    return v

def data(f):
    f=R/f
    return json.loads(gzip.decompress(f.read_bytes()) if f.suffix=='.gz' else f.read_bytes())
A=sigma(p,e)
assert prod(roots)==A and all(A%r==0 for r in roots)
full={m for m in range(256) if m&3==2}
proof_old=set(map(int,data('FinalSprint/Support/Root7x28.json.gz')['closed']))
proof_new=set(map(int,data('Night2400/D2/Seven28.json.gz')['cases']))
project=set(data('Session20261126/OpenSupport.json')['rows']['7:28'])
assert proof_old <= project <= full and proof_new <= full and not proof_old & proof_new
assert (len(full),len(project),len(proof_old),len(proof_new),len(proof_new&project))==(64,26,13,27,13)
rest=full-proof_old-proof_new
assert len(rest)==24

def lower(m):
    have={s for i,s in enumerate(S) if m>>i&1}-{p}
    blocked=prod(s for i,s in enumerate(S) if not m>>i&1)
    seeds=have|set(roots)
    assert gcd(prod(seeds)*A,blocked)==1
    def component(q,odd):
        f=1 if odd else 2
        while f<val(A,q) or gcd(sigma(q,f),blocked)!=1:
            f+=4 if odd else 2
        return Fraction(sigma(q,f),q**f)
    evens={q:component(q,False) for q in seeds}
    baseline=Fraction(A,X)*prod(evens.values())
    return min([baseline]+[baseline/evens[q]*component(q,True) for q in seeds if q%4==1 and gcd(q+1,blocked)==1])

ab=min(map(lower,rest))
assert ab>2
ledger=[x for x in data('FinalSprint/Delta.json')['remaining_shards'] if x['id']=='P7_I00009']
assert len(ledger)==1 and ledger[0]['root']==7 and ledger[0]['remaining_actuals']==[28]
# Diagnostic unweighted split absent only 19; proof uses the forest tails instead.
assert val(A,Q)==1 and Q%4==3
scale=X*(A//Q)
assert scale*Q**170<=B<scale*Q**171
live=[]
for f in range(2,171,2):
    S0=A*sigma(Q,f);Y=X*Q**f;D=S0//gcd(S0,Y)
    if Y*D<=B and S0<=2*Y and gcd(S0,19)==gcd(D,Y)==1:
        live.append(f)
assert len(live)==28
print('PASS 64 masks, 13 old + 27 new + 24 rational abundance; minimum ppm',ab.numerator*10**6//ab.denominator,'f diagnostic tail=171, live',live,'singleton [28]')

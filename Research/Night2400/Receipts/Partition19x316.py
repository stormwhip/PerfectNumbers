"""Independent exact support/valuation partition for candidate D (19,316)."""
from collections import Counter
from fractions import Fraction
from math import gcd,prod
from pathlib import Path
import gzip,json

R = Path('Research')
p,e,q = 19,316,1255900817071954721881883552067931
B=10**2400
S8=(19,7,11,31,13,3,5,17)
X0=p**e

def sigma(r,f): return sum(r**j for j in range(f+1))

def order_div(n,r):
    assert n>0
    k=0
    while n%r==0:
        n//=r; k+=1
    return k

def load(path):
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())

A=sigma(p,e)
assert q%4==3 and order_div(A,q)==1
scale=X0*(A//q)
assert scale*q**49 <= B < scale*q**50
full={}
for f in range(2,50,2):
    X=X0*q**f
    S=A*sigma(q,f)
    if order_div(S,p)>e or order_div(S,q)>f or S>2*X or X*(S//gcd(X,S))>B:
        continue
    full[f]=S
assert set(full)==set(range(2,25,2))
old=load(R/'FinalSprint/Support/Pivot316.json.gz')
projected=load(R/'Session20261126/OpenSupport.json')['rows']['19:316']
new=load(R/'Night2400/D/Pivot316Residual.json.gz')['cases']
prior={x['f'] for x in old['rows']}
assert prior==set(range(6,25,2))
masks = {m for m in range(256) if m&1}
assert len(masks)==128 and set(old['masks']) | {int(k) for k in new} == set(projected)
audit=Counter(); exterior=[]; mask59=None

def root_bound(rows,pres,absent,roots=None):
    signals=prod(sigma(r,f) for r,f in rows)
    other=list(pres if roots is None else roots)
    assert len(set(other))==len(other) and not set(other) & (set(dict(rows)) | set(absent))
    assert all(r in pres or signals%r==0 for r in other)
    base=prod(Fraction(sigma(r,f),r**f) for r,f in rows)
    def min_f(r,special):
        f=1 if special else 2
        while f<order_div(signals,r) or gcd(sigma(r,f),prod(absent))!=1:
            f+=4 if special else 2
        return Fraction(sigma(r,f),r**f)
    even={r:min_f(r,False) for r in other}
    all_even=base*prod(even.values())
    return min([all_even]+[all_even/even[r]*min_f(r,True) for r in other if r%4==1 and gcd(r+1,prod(absent))==1])

for m in sorted(masks):
    present=tuple(r for i,r in enumerate(S8) if i and m & (1<<i))
    absent=tuple(r for i,r in enumerate(S8) if not m & (1<<i))
    live={f for f,S in full.items() if gcd(S,prod(absent))==1}
    if m in old['masks']:
        assert live<=prior
        audit['historical projected']+=1
    elif m not in projected:
        if live<=prior:
            audit['historical or direct exterior']+=1
        else:
            lb=root_bound([(p,e)],present,absent)
            assert lb>2
            exterior.append(lb)
            audit['abundance exterior']+=1
    else:
        leaf=new[str(m)]
        f=leaf['f']
        assert live-prior=={f}
        if leaf['kind']=='abundance':
            assert m==59
            mask59=root_bound([(p,e),(q,f)],present,absent,leaf['roots'])
            assert mask59>2
        audit[f,f"residual {leaf['kind']}"]+=1
assert audit == {'historical projected':36, 'historical or direct exterior':36, 'abundance exterior':35,(2,'residual abundance'):1,(2,'residual forest'):4,(4,'residual forest'):16}
assert sum(audit.values())==128
baseline=[j for j in load(R/'FinalSprint/Delta.json')['remaining_shards'] if j['id']=='P19_I00064']
assert len(baseline)==1 and baseline[0]['remaining_actuals']==[316] and baseline[0]['root']==19
ppm=lambda x:x.numerator*10**6//x.denominator
print('PASS exact partition',dict(audit),'all globally legal pivot vals',list(full),'first size tail',50,'root-only minimum ppm',ppm(min(exterior)),'residual mask 59 ppm',ppm(mask59),'baseline residual set',[316])

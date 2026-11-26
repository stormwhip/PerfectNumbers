"""Arithmetic audit of tree split coverage; no candidate code imported.
Usage: python -I -S -B -X int_max_str_digits=0 FiberPartition.py <packet.gz>
Supports VerifyFibers, A Verify, and E Verify130 packet schemas. Primality and
terminal certificates must separately be checked by the actual verifier.
"""
from collections import Counter
from functools import cache
from math import gcd, prod
from pathlib import Path
import gzip,json,sys

B=10**2400
ORDER=(19,7,11,31,13,3,5,17)
data=json.loads(gzip.decompress(Path(sys.argv[1]).read_bytes()))
if 'pair' in data:
    p,e=data['pair']
elif 'key' in data:
    p,e=data['key']
else:
    p,e=data['p'],data['e']
banned=ORDER[:ORDER.index(p)]
root_has_explicit_open = 'tree' in data
root=data['tree'] if root_has_explicit_open else {'type':'split','q':data['pivot'],'cases':data['cases']}

@cache
def sig(q,f):
    return (q**(f+1)-1)//(q-1)

def valuation(x,q):
    assert x>0
    v=0
    while x%q==0:
        x//=q;v+=1
    return v

def state(parts):
    X=prod(q**f for q,f in parts)
    raw=prod(sig(q,f) for q,f in parts)
    odd=sum(f%2 for q,f in parts)
    S=raw//2**odd
    D=S//gcd(S,X)
    return X,raw,S,D,odd

counts=Counter();tails=[];open_by_first=Counter()
def walk(parts,node,is_root=False):
    kind=node['type'];counts[kind]+=1
    if kind!='split':
        if kind=='open':open_by_first[parts[1][1]]+=1
        return
    r=node['q'];assert r not in banned and r not in dict(parts)
    X,_,_,D,odd=state(parts);c=valuation(D,r);assert c>0
    f=c;size=X*D;illegal=[];direct=[];live=[]
    while size<=B:
        if (f%2 and (odd or r%4!=1 or f%4!=1)) or gcd(sig(r,f),prod(banned))>1:
            illegal.append(f)
        else:
            Y,raw,S,U,_=state(parts+[(r,f)])
            if gcd(S,prod(banned))>1 or gcd(Y,U)!=1 or Y*U>B or raw>2*Y:
                direct.append(f)
            else:live.append(f)
        f+=1;size*=r
    assert size//r<=B<size
    tails.append(f);counts['direct']+=len(direct);counts['illegal']+=len(illegal)
    claimed=set(map(int,node['cases']))
    assert claimed==set(live) or (is_root and not root_has_explicit_open and claimed<=set(live))
    if is_root:
        for i in set(live)-claimed:open_by_first[i]+=1
        print('key',(p,e),'pivot',r,'compelled valuation',c,'root live',live,'root direct',direct,'root illegal',illegal)
    for i in sorted(claimed):walk(parts+[(r,i)],node['cases'][str(i)])

walk([(p,e)],root,True)
print('PASS data-only domain audit; counts',dict(counts),'tails',tails,'open per first',dict(sorted(open_by_first.items())),'ECPP entries',len(data['ecpp']))

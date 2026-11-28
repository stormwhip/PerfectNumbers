"""Verify new exact forest cuts and their frozen-window provenance."""
from functools import cache
from math import gcd,prod
from pathlib import Path
import gzip,hashlib,json,sys

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'Session20261126'))
from PivotCheck import C,exact_leaf,floor10
B=10**2400
T,R=7579985624053,3705121363

def need(ok,msg):
    if not ok:raise ValueError(msg)

def readz(p):return json.loads(gzip.decompress(p.read_bytes()))

def val(n,q):
    a=0
    while n%q==0:n//=q;a+=1
    return a

@cache
def sig(q,a):return (q**(a+1)-1)//(q-1)

def exact(rows):
    X=prod(q**h for q,h in rows)
    A=prod(sig(q,h) for q,h in rows)
    odds=sum(h%2 for q,h in rows)
    if odds>1 or any(h%2 and (q%4!=1 or h%4!=1) for q,h in rows):return None
    S=A//(1+odds)
    if A>2*X or any(S%q**(h+1)==0 for q,h in rows):return None
    D=S//gcd(X,S)
    return (X,D) if X*D<=B else None

def domain(rows,q):
    need(q not in dict(rows),'pivot must be unassigned')
    X,D=exact(rows)
    need(D%q==0,'pivot not compulsory')
    v=val(D,q);size=X*D;ok=[]
    while size<=B:
        if exact(rows+((q,v),)) is not None:ok.append(v)
        size*=q;v+=1
    return ok,v

def main():
    need(__debug__,'Python optimization is forbidden')
    root=RESEARCH/'FinalNight2400'/'Root222'
    histpath=root/'ThirdForests.json.gz'
    frozen=readz(histpath)
    data=readz(HERE/'Forest222.json.gz')
    base=['495c59f55456a70994ce7848487e0c4e262c1984','CONDITIONAL_NEW_EXACT_PREFIXES']
    need([data['frozen'],data['status']]==base,'packet status')
    need(hashlib.sha256(histpath.read_bytes()).hexdigest()==data['thirds_sha256'],'historical file mismatch')
    book=data['ecpp'];used=set()
    @cache
    def prime(q):
        need(type(q)==int and q>2 and q%2,'odd prime type')
        n=q
        if n>=2**64:
            used.add(str(q)); ch=book[str(q)];need(bool(ch),'missing prime chain')
            for step in ch:
                need(step[0]==n,'invalid prime chain sequence');n=C.pc.level(*step)
        need(C.pc.prime64(n),'prime witness failed')
        return True
    need(all(prime(q) for q in [19,T,R]),'root/witness arithmetic')
    group={}
    for case in data['cases']:
        p=tuple(tuple(x) for x in case['prefix']); need(len(p) in (3,4),'prefix length')
        need(exact(p) is not None and p[0]==(19,222) and p[1][0]==T and p[2][0]==R,'not an exact root-222 depth')
        f,g=p[1][1],p[2][1]; need(f in (1,2,18),'frozen first already closed')
        # Reconstruct all immediate parent exponents for every recorded route.
        first,first_tail=domain(p[:1],T);second,second_tail=domain(p[:2],R)
        need(first_tail==144 and len(first)==53 and f in first and g in second,'first/second exact windows')
        also=readz(root/'TwoForests.json.gz')['cases'][str(f)]
        need(str(g) not in also,'second already excluded')
        key=f'{f}:{g}'; hist=frozen['cases'].get(key)
        if len(p)==3:
            need(hist is None and (f,g)!=(1,58),'ancestor is not open at second level')
            origin=(None,None,None);j=None
        else:
            q,j=p[3];need(prime(q) and isinstance(hist,dict) and hist['q']==q,'frozen tertiary pivot')
            dom,tail=domain(p[:3],q)
            need(set(hist['children'])|set(map(str,hist['left']))==set(map(str,dom)) and not set(hist['children'])&set(map(str,hist['left'])),'frozen third exact covering gap')
            prior=set(hist['left'])-({40,42} if (f,g)==(1,16) else set())-({1} if (f,g) in ((2,16),(2,22)) else set())
            need(j in prior,'terminal not new'); origin=(q,sorted(prior),tail)
        old=group.setdefault((f,g),[origin,set()]);need(old[0]==origin and j not in old[1],'duplicate or mixed window');old[1].add(j)
        K,O,H=case['forest'];s=C.State(p);need(not s.conflict and s.bad==(),'canonical state')
        C.validate_forest(s,K,O,H,prime)
        a=C.Forest(s,K,O,H).lower()[0];b=exact_leaf(p,K,O,H)
        need(min(a,b)>B,'integer terminal failed')
        need([floor10(a),floor10(b)]==case['floor10'],'lower-bound receipt changed')
        print('PASS',p,'floor log10 recurrences',floor10(a),floor10(b),flush=True)
    need(used==set(book),'unreferenced prime witness')
    counts=0
    residual={}
    for (f,g),(origin,closed) in sorted(group.items()):
        q,prior,tail=origin
        left=None if q is None else sorted(set(prior)-closed)
        if not left:counts+=1
        residual[f'{f}:{g}']=dict(pivot=q,before=prior,after=[] if q is None else left,strict_raw_tail=tail,closed=sorted(closed))
    need(residual==data['windows'],'reported residual does not match integer coverage')
    print('COVER',len(data['cases']),'new exact rows;',counts,'completed secondary prefixes; prime chains',len(used),flush=True)
    print(json.dumps(residual,sort_keys=True),flush=True)

if __name__=='__main__':main()

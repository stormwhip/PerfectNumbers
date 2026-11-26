"""Standalone standard-library proof of the new unmasked (7,438) fibers."""
from pathlib import Path
from functools import cache
from hashlib import sha256
from math import gcd,prod
import argparse,gzip,json,sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path.insert(0,str(R/'Session20261126'))
from PivotCheck import C,floor10,exact_leaf

P,E,Q=7,438,572749682520506652634407616247
B=10**2400
BAN=(19,)


def sig(q,f):return (q**(f+1)-1)//(q-1)


def val(n,q):
    v=0
    while n%q==0:n//=q;v+=1
    return v


def trim(n,u):
    while (g:=gcd(n,u))>1:n//=g
    return n


def status(rows):
    x=prod(q**f for q,f in rows)
    sums=prod(sig(q,f) for q,f in rows)
    odd=sum(f%2 for q,f in rows)
    if odd>1 or any(f%2 and q%4!=1 or f%2 and f%4!=1 for q,f in rows):return None
    s=sums//(1+odd)
    if gcd(s*prod(q for q,_ in rows),prod(BAN))>1 or sums>2*x or any(val(s,q)>f for q,f in rows):return None
    d=trim(s,prod(q for q,_ in rows))
    return (x*d,d,odd) if x*d<=B else None


def children(rows,q,prime):
    base,d,odd=status(rows)
    assert prime(q) and q not in dict(rows) and q not in BAN and d%q==0
    c=val(d,q);scale=base//q**c;f=c; taken={};excluded=0
    while scale*q**f<=B:
        if not f%2 or (not odd and q%4==f%4==1):
            cc=rows+[(q,f)]
            if status(cc):taken[str(f)]=cc
            else:excluded+=1
        f+=1
    assert scale*q**(f-1)<=B<scale*q**f
    return taken,f,excluded


def verify(packet):
    if not __debug__:raise RuntimeError('assertions required; do not use -O')
    raw=packet.read_bytes();d=json.loads(gzip.decompress(raw));assert set(d)=={'p','e','pivot','cases','ecpp'} and (d['p'],d['e'],d['pivot'])==(P,E,Q)
    used=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2
        n=q
        if n>=2**64:
            c=d['ecpp'][str(q)];assert c
            for lev in c:
                assert lev[0]==n;n=C.pc.level(*lev)
            used.add(str(q))
        assert C.pc.prime64(n)
        return True
    assert prime(P) and prime(19) and C.ORDER[:C.ORDER.index(P)]==BAN
    assert prime(Q) and val(sig(P,E),Q)==1 and Q%4==3
    roots,tail,_=children([(P,E)],Q,prime)
    assert sorted(map(int,roots))==[2,4,6,10,12,14,16,18,20,22,24,28] and tail==57
    assert 0<len(d['cases']) and set(d['cases'])<=set(roots)
    def walk(rows,leaf,stat):
        assert status(rows)
        if leaf['type']=='split':
            assert set(leaf)=={'type','q','cases'}
            cases,tail,dead=children(rows,leaf['q'],prime)
            assert set(cases)==set(leaf['cases'])
            stat['split']+=1;stat['tails'].append(tail);stat['direct']+=dead
            for f,path in cases.items():walk(path,leaf['cases'][f],stat)
        else:
            assert leaf['type']=='forest' and set(leaf)=={'type','roots','owners','head'}
            k,o,h=map(leaf.get,('roots','owners','head'));s=C.State(rows)
            assert not s.conflict
            C.validate_forest(s,k,o,h,prime)
            a=C.Forest(s,k,o,h).lower()[0]
            b=exact_leaf(rows,k,o,h)
            assert min(a,b)>B,('not strict',rows,floor10(a),floor10(b))
            stat['forest']+=1;stat['floor']=min(stat['floor'],floor10(min(a,b)))
    for f,node in sorted(d['cases'].items(),key=lambda a:int(a[0])):
        st={'forest':0,'floor':10**9,'split':0,'tails':[],'direct':0};walk(roots[f],node,st)
        print('PASS',f,st,flush=True)
    assert used==set(d['ecpp'])
    covered=sorted(map(int,d['cases']));old=(4,6,14,20,24,28); gap=sorted(set(map(int,roots))-set(covered)-set(old))
    print('VERIFIED',(P,E),'new',covered,'remaining with previously sealed six',gap,'first tail',tail,'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,default=H/'Seven438.json.gz');verify(p.parse_args().packet)

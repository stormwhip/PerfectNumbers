"""Standalone standard-library proof of complete certified (13,262) pivot fibers."""
from pathlib import Path
from functools import cache
from hashlib import sha256
from math import gcd,prod
import argparse,gzip,json,sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path.insert(0,str(R/'Session20261126'))
from PivotCheck import C,floor10,exact_leaf

P,E,Q=13,262,231050784610489
B=10**2400
BAN=(19,7,11,31)


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
    assert prime(P) and all(prime(b) for b in BAN) and C.ORDER[:C.ORDER.index(P)]==BAN
    assert prime(Q) and val(sig(P,E),Q)==1 and Q%4==1
    roots,tail,_=children([(P,E)],Q,prime)
    assert sorted(map(int,roots))==[1,4,6,10,12,13,16,18,21,22,24,25,28,30,33,34,36,37,40,42,45,46,48,52,54,57,58,60,61] and tail==128
    assert 0<len(d['cases']) and set(d['cases'])<=set(roots)
    def walk(rows,leaf,stat):
        assert status(rows)
        if leaf['type']=='open':
            assert set(leaf)=={'type'}
            stat['open'].append(rows)
            return
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
    covered=[];partial={}
    for f,node in sorted(d['cases'].items(),key=lambda a:int(a[0])):
        st={'forest':0,'floor':10**9,'split':0,'tails':[],'direct':0,'open':[]};walk(roots[f],node,st)
        if st['open']:partial[int(f)]=st['open']
        else:covered.append(int(f))
        print('PARTIAL' if st['open'] else 'PASS',f,st,flush=True)
    assert used==set(d['ecpp'])
    gap=sorted(set(map(int,roots))-set(covered))
    print('VERIFIED',(P,E),'covered',covered,'remaining',gap,'open deep counts',{f:len(v) for f,v in partial.items()},'first tail',tail,'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)
    return {'data':d,'root_domain':sorted(map(int,roots)),'covered':covered,'open':partial}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,default=H/'Thirteen262.json.gz');verify(p.parse_args().packet)

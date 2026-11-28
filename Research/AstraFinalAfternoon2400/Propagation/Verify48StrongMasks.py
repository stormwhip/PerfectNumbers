"""Rebuild locally necessary abundance masks and certify tighter (7,48) forest leaves."""
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Verify48Masks import lemma,BASE,C,B,abgt2,exact_state,independently,prime64,level
from Verify48Price import P,T,SMALL,ROOTS,PIVOT,domain
from Propagation import sigma,val

# All compulsory labels are independently checked as divisors of the exact
# fixed emissions, or 3 itself in the established ≥6 bin. Lists are witnesses,
# not assumed complete factorizations of anonymous residuals.
EXTRA={
  2:(3,127,409,1722040929387184333),
  4:(71,21701,26021),
  6:(379,883,47741,1209438625527226113101190974186116594304625407989743565304741),
  8:(3,127,199,409,6067,995849188237,138756341190531403,1722040929387184333,38608285873275850416120646545918097),
 10:(23,),
 12:(13,157),
 16:(1531,),
 18:(1483,),
}


def verify(path,expected):
    assert __debug__;lemma()
    data=path.read_bytes(); pack=json.loads(gzip.decompress(data)); assert set(pack)=={'records','ecpp'}
    ecpp=pack['ecpp'];used=set();rec=[]
    @cache
    def prime(p):
        if p<2**64:return prime64(p)
        s=str(p);used.add(s);n=p
        for row in ecpp[s]:assert n==row[0];n=level(*row)
        return prime64(n)
    r=PIVOT[2]; assert prime(r) and prime(T) and sigma(T,2)%r==0
    assert sigma(P,48)%prod(SMALL)==0 and sigma(T,2)==prod(ROOTS[2])
    for z in pack['records']:
        rows=list(map(tuple,z['P'])); assert rows[:2]==BASE and len(rows) in (3,4)
        assert rows[2][0]==r and rows[2][1] in domain(BASE,r)[0]
        h=rows[2][1]; m=2 if len(rows)==4 else 6
        if m==2:assert rows[-1]==(3,2) and z.get('present',[])==[] and z.get('lo',[])==[]
        else:assert z['present']==[3] and z['lo']==[[3,6]]
        assert all(prime(q) for q,e in rows)
        have=tuple(z.get('present',[])); lo=dict(z.get('lo',[]))
        b=tuple(z['bad']); assert tuple(b[:3])==(19,5,11) and len(set(b))==len(b)
        tree=z['tree']; assert set(tree)=={'type','roots','owners','head'} and tree['type']=='forest'
        roots,edges,head=(tree[k] for k in ('roots','owners','head'))
        emissions=prod(sigma(q,g) for q,g in rows)
        H0=dict(rows); known=(set(SMALL)|set(ROOTS[2])|set(roots)|set(EXTRA.get(h,())))-H0.keys()-set(have)
        assert all(prime(q) and emissions%q==0 for q in known)
        for q in known:H0[q]=2 if q%4==3 else 1
        H0.update(lo)
        for q in b[3:]:
            assert prime(q) and q not in H0
            assert abgt2(list(H0.items())+[(q,2 if q%4==3 else 1)]),(h,m,q)
        ok,X,D,fixed=exact_state(rows,b); assert ok
        s=C.State(rows,present=have,absent=b[1:],lo=lo);assert not s.conflict and s.bad==b and (s.X,s.D)==(X,D)
        C.validate_forest(s,roots,edges,head,prime)
        a=C.Forest(s,roots,edges,head).lower()[0]; c=independently(rows,b,roots,edges,head,have,lo)
        assert min(a,c)>B
        rec.append((h,m));print('48 strong support',h,m,'derived extra bans',len(b)-3,'floor',len(str(min(a,c)))-1,flush=True)
    assert rec==expected and rec and len(set(rec))==len(rec) and used==set(ecpp)
    print('PASS strong masks',rec,'ECPP',len(used),'sha256',sha256(data).hexdigest(),flush=True)

PACKS={'orbit48strong':[(6,2),(8,2),(10,2)],
       'orbit48strongmore':[(2,2),(2,6),(4,2),(16,2)],
       'orbit48strongextra':[(4,6),(6,6),(8,6),(12,6),(18,2)],
       'orbit48strongtail':[(10,6),(16,6),(22,2)],
       'orbit48strong18':[(18,6)],
       'orbit48strong22':[(22,6)]}

if __name__=='__main__':
    for tag in sys.argv[1:] or list(PACKS):
        verify(H/f'Reserved438x12-{tag}.json.gz',PACKS[tag])

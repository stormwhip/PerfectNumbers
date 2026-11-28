"""Independent full compound first-fiber verification for (11,16), t^25."""
from fractions import Fraction
from functools import cache
import gzip
from hashlib import sha256
import json
from math import gcd,lcm,prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B,geometric,split,state,vp
from Check31Forest import PR,forest
BANS=(19,7)
P,T,S=11,50544702849929377,239337374873
ROW=((P,16),(T,25),(S,16))


def price(row):
    assert row==ROW and T%4==1
    X,Y,ok=state(row,BANS)
    assert ok and 16-vp(Y,S)==15 and 3**5030<=B<3**5031<S**5031
    assert [o for o in range(3,5032,2) if (S-1)%o==0]==[107]
    D=lcm(X,Y)//X
    a=2
    while (g:=pow(a,(S-1)//107,S))==1:
        a+=1
    assert pow(g,107,S)==1 and g!=1
    m=S
    loss={}
    for j in range(1,16):
        roots={pow(g,k,m) for k in range(1,107)}
        assert len(roots)==106 and 1 not in roots
        for r in roots:
            assert pow(r,107,m)==1 and 0<r<m
            if r<3 or r%2==0 or r in (*dict(row),*BANS) or X*lcm(D,r**106)>B:
                continue
            # Conservative, one-way Fermat witness; keep any inconclusive odd base.
            if any(pow(p,r-1,r)!=1 for p in (2,3,5,7,11,13,17,19,23) if p<r):
                continue
            loss[r]=max(loss.get(r,1),Fraction(m**106,r**106))
        m*=S
        g=pow(g,S,m)
    lb=Fraction(X*S**(106*15),prod(loss.values()))
    assert lb>B
    print('PASS independent terminal (only order 107), losses',len(loss),'strict decimal floor',len(str(lb.numerator//lb.denominator))-1,flush=True)


def main():
    assert __debug__
    paths=H.parent/'ElevenThirteen'
    raw=(paths/'Second-11-16-25.json.gz').read_bytes()
    assert sha256(raw).hexdigest()=='76d740a16a12f33694491bc7d043cee8e4de829372fbf5242fb2b55183c9ad9a'
    j=json.loads(gzip.decompress(raw)); m=j['row']
    assert (m['p'],m['e'],m['f'])==(P,16,25)
    assert geometric(P,16)==T and all(PR['prime64'](p) for p in (P,T,S))
    coverage=json.loads((paths/'ForestCoverage.json').read_bytes())['11:16']
    assert coverage['pivot']==T and 25 in coverage['remaining'] and 25 not in coverage['accepted']
    domain,tail=split(((P,16),),T,BANS)
    assert tail==143 and 25 in domain
    learned=set(); types=[0,0,0]
    @cache
    def prime(p):
        if p>=2**64:
            learned.add(str(p)); rows=j['ecpp'][str(p)]; assert rows
            for row in rows:
                assert row[0]==p; p=PR['level'](*row)
        assert PR['prime64'](p)
    def walk(row,leaf):
        if 'price' in leaf:
            assert leaf=={'price':'Seal25'}
            price(row);types[2]+=1
        elif 'split' in leaf:
            p=leaf['split']; prime(p)
            new,_=split(row,p,BANS);types[0]+=1
            assert leaf['cases'].keys()=={str(k) for k in new}
            for k,s in new.items(): walk(s,leaf['cases'][str(k)])
        else:
            for p in (*leaf['roots'],*(p for p,_ in leaf['owners'])):prime(p)
            assert forest(row,leaf,BANS)>B
            types[1]+=1
    walk(domain[25],m['tree'])
    assert learned==j['ecpp'].keys() and types==[3,56,1]
    print('PASS independent f25 full exact fiber: split/forest/price',types,'ECPP',len(learned),flush=True)


if __name__=='__main__':main()

"""Separate exact first/second domain, packet assignment and projection audit for (7,48)."""
from fractions import Fraction
from hashlib import sha256
from math import prod
from pathlib import Path
import gzip,json,sys,subprocess
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import BASE,geometric as G,split
from Check31Forest import PR
from Check48StrongScopes import P,T,R
from Check48FinalSquare import PARENT,Q,BAD,EXPECT
ROOT=H.parent
A=5913168485260377611579965807967983090512568398832018674784831
N=531983
FOUR={'a':'65361a2a06a7aabecfbe2e6d54bea1468554b5a10c61bc3fd40f9c9a9ec4c44e','b':'92d1684d24a071b2f9e3636c55760ef1f63b6c91c024e5144846d72fbb897fdf'}


def git_blob(path):
    return subprocess.check_output(['git','show',f'{BASE}:Research/{path}'],cwd=ROOT)


def packing(path,want=None):
    raw=(ROOT/path).read_bytes()
    digest=sha256(raw).hexdigest()
    assert want is None or digest==want
    return json.loads(gzip.decompress(raw)),digest


def supports(base):
    assert G(7,48)%29==G(T,base[-1][1])%61==0
    assert G(11,2)%19==0 and G(3,2)==13 and G(3,4)==121
    row=((7,48),(29,1),(61,1))
    def ab(s):return prod(Fraction(G(p,a),p**a) for p,a in s)
    assert ab((*row,(3,2),(5,1)))>2 and ab((*row,(3,4),(11,4)))>2
    assert ab((*row,(3,2),(11,4),(13,1)))>2


def main():
    assert __debug__ and all(PR['prime64'](p) for p in (P,T,R,N))
    first,tail=split(((7,48),),T,(19,))
    assert tail==125 and len(first)==31
    old=git_blob('FinalNight2400/LowSeven/Seven48.json.gz')
    assert sha256(old).hexdigest()=='8112caf03da5792950ba2d32beded8502c8a2f5e21ebb45d105be66b5e8f9c7e'
    old=json.loads(gzip.decompress(old)); assert (old['p'],old['e'],old['pivot'])==(7,48,T)
    old_first={int(a) for a,n in old['cases'].items() if n['type']=='forest'}
    assert len(old_first)==len(old['cases'])==27 and old_first<=first.keys() and first.keys()-old_first=={2,4,8,10}
    print('PASS independent first 31, strict tail125, frozen exact complement 2/4/8/10',flush=True)
    square,s_tail=split(first[2],R,(19,));ten,t_tail=split(first[10],N,(19,))
    assert s_tail==195 and square.keys()==set(range(2,97,2))
    assert t_tail==344 and ten.keys()==set(range(2,171,2))
    A_dom,A_tail=split(first[4],A,(19,))
    assert tuple(A_dom)==tuple(range(2,19,2)) and A_tail==37
    # A^2 terminal at first 4: exact compulsion then two strict abundance alternatives.
    assert G(T,4)%(11*41*A)==0 and G(A,2)%3==0 and G(P,48)%29==0 and G(11,2)%19==0
    base=((7,48),(11,4),(29,1),(41,1))
    def ab(s):return prod(Fraction(G(p,a),p**a) for p,a in s)
    assert ab((*base,(3,4)))>2 and G(3,2)==13 and ab((*base,(3,2),(13,1)))>2
    four={2}
    for tag,h in FOUR.items():
        d,_=packing(f'Seven/Forest48{tag}.json.gz',h)
        for item in d['records']:
            row=tuple(map(tuple,item['P'])); e=row[-1][1]
            assert e not in four and row==A_dom[e] and item['bad']==[19] and not item['unresolved']
            four.add(e)
    assert four==A_dom.keys()
    d,digest=packing('Seven/Forest48Eight.json.gz');supports(first[8]);modes=set()
    for item in d['records']:
        row=tuple(map(tuple,item['P'])); bad=tuple(item['bad'])
        p=item.get('present',[]); lo=item.get('lo',[])
        if row==first[8] and bad==(19,3): e=0; assert not p and not lo
        elif row==(*first[8],(3,2)) and bad==(19,5,11): e=2;assert not p and not lo
        else: e=6;assert row==first[8] and bad==(19,5,11) and p==[3] and lo==[[3,6]]
        assert not item['unresolved'] and e not in modes; modes.add(e)
    assert modes=={0,2,6}
    pools={2:(),10:()}
    for f,tags in [(2,('orbit48sq','orbit48sqmid')),
                   (10,('orbit48','orbit48ten','orbit48tenlow','orbit48tenfresh','orbit48tennested','orbit48tenhard','orbit48tenhard10','orbit48tenhardfinal'))]:
        all_h=set(); domain=ten if f==10 else square
        for name in tags:
            d,hash=packing(f'Propagation/Reserved438x12-{name}.json.gz')
            for item in d['records']:
                row=tuple(map(tuple,item['P'])); h=row[-1][1]
                assert h not in all_h and row==domain[h] and item['bad']==[19] and not item['unresolved']
                all_h.add(h)
        pools[f]=all_h
    # The exact price intervals and finite-CRT overlap cells are further scoped
    # and arithmetic checked by the independent prerequisite receipts.
    p2=set(range(76,97,2)); p10=set(range(104,171,2))
    o2={74}; o10={92,98,100,102}
    assert len(pools[2])==27 and len(pools[10])==47
    for f,sets in ((2,(p2,o2,pools[2])),(10,(p10,o10,pools[10]))):
        assert sum(map(len,sets))==len(set.union(*sets))
    assert ten.keys()==p10|o10|pools[10]
    assert square.keys()-(p2|o2|pools[2])=={2,4,6,8,10,12,16,18,22}
    assert set(split(PARENT,Q,BAD)[0])==set(EXPECT) and split(PARENT,Q,BAD)[1]==143
    fwd=json.loads(git_blob('FinalNight2400/OpenFrontier.json'))['ShardRemainders']
    inv=json.loads(git_blob('GeminiFrontier/KeyToShards.json'))
    association=[k for k,v in fwd.items() if [7,48] in v]
    assert len(association)==1 and association==inv['7,48']
    print('PASS both exact child domains; t^4 9/9, t^8 three support bins, t^10 85/85, t^2 39 unrestricted and 9 support splits',flush=True)
    print('Exact frozen shard membership at (7,48):',association, [fwd[k] for k in association],flush=True)

if __name__=='__main__':main()

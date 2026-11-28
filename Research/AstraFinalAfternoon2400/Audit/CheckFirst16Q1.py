"""Independent finite domains and forest DP for the full Q^1 second fiber under t^16."""
from functools import cache
from hashlib import sha256
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Forest import PR,forest
from Check31Domains import split,B
T=1176672733
Q=90938047640154004421283567941471211810894981635972737129272047925640491256883059096525979990283681579529
R=537069791622427053730040164091678112653
P=((19,276),(T,16)); rows=P+((Q,1),)


def main():
    assert __debug__
    book=(H.parent/'Nineteen/First16Q1.json.gz').read_bytes()
    assert sha256(book).hexdigest()=='166c9604dee56e87f6190ff0fb2f5a9c56efe9eba208ba24b0bed5bcd13112bf'
    b=json.loads(gzip.decompress(book)); assert tuple(map(tuple,b['prefix']))==rows
    live,tail=split(P,Q,()); assert live.keys()=={1,2,4,5,6} and tail==15 and live[1]==rows
    child,tail=split(rows,R,()); assert child.keys()==set(range(2,17,2)) and tail==35
    used=set()
    @cache
    def prime(p):
        if p>=2**64:
            k=str(p);used.add(k); steps=b['ecpp'][k]; assert steps
            for step in steps:assert step[0]==p;p=PR['level'](*step)
        assert PR['prime64'](p)
    for p in (19,T,Q,R):prime(p)
    assert set(map(int,b['children']))==child.keys()
    for h,r in child.items():
        k,o,d=b['children'][str(h)]['forest']; v=set(k)|{p for p,_ in o}
        for p in v:prime(p)
        assert forest(r,dict(roots=k,owners=o,head=d),())>B
    assert used==b['ecpp'].keys() and len(used)==57
    print('PASS independent root19 276 first16 Q1 8 child cases, raw35, 57 certified ECPP, all strict')

if __name__=='__main__':main()

"""Verify the exact entire second fiber Q^1 under (19,276), t^16."""
from pathlib import Path
from functools import cache
from hashlib import sha256
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import B,C,HERE,exact,domain,floor10,need,readz,exact_leaf,sig

T=1176672733
Q=90938047640154004421283567941471211810894981635972737129272047925640491256883059096525979990283681579529
R=537069791622427053730040164091678112653
P=((19,276),(T,16),(Q,1))

def main():
    need(__debug__,'assertions enabled')
    prev=HERE/'Even276.json.gz';need(sha256(prev.read_bytes()).hexdigest()=='36eb3b356815fd993ff88cc762e634a56264beb899576c9e74e70bdb03289b4e','prior complement hash')
    p=readz(prev)['cases']['16'];need(p['pivot']==Q and p['remaining']==[1,2,4] and domain(P[:2],Q)==([1,2,4,5,6],15),'complete prior window')
    data=readz(HERE/'First16Q1.json.gz');book=data['ecpp'];used=set()
    need(data['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,data['prefix']))==P and data['pivot']==R,'exact scope')
    @cache
    def prime(q):
        r=q;need(type(q)==int and q>2 and q%2,'odd prime label')
        if r>=2**64:
            ch=book[str(q)];used.add(str(q));need(bool(ch),'missing chain')
            for a in ch:need(a[0]==r,'broken chain subject');r=C.pc.level(*a)
        return C.pc.prime64(r)
    need(all(prime(q)for q in (*dict(P),R)) and exact(P) is not None and sig(19,276)%T==0 and sig(T,16)%Q==0 and sig(Q,1)%(2*R)==0 and Q%4==1,'compelled exact bases/Euler')
    D,tail=domain(P,R)
    need(D==list(range(2,17,2)) and tail==35 and set(map(int,data['children']))==set(D) and all(str(j)in data['children'] for j in D),'strict third-pivot full domain')
    for h in D:
        rows=P+((R,h),);x=data['children'][str(h)];K,O,H=x['forest'];st=C.State(rows)
        C.validate_forest(st,K,O,H,prime);a=C.Forest(st,K,O,H).lower()[0];b=exact_leaf(rows,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==x['floor10'],'strict dual lower bound')
        print('PASS f16, Q1, R exponent',h,'ordinary-only integer floors',x['floor10'],flush=True)
    need(used==set(book),'extra prime witness records')
    print('COMPLETE f16 second window Q^1; raw tail',tail,'ECPP chains',len(used),'remaining exact Q exponents [2,4]')

if __name__=='__main__':main()

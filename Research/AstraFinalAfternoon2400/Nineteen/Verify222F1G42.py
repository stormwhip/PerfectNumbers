"""Complete f=1, g=42 exact window at canonical (19,222), empty compelled pivot domain."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import B,C,HERE,RESEARCH,exact,domain,readz,floor10,sig,need,T,R
from math import prod,gcd

P=((19,222),(T,1),(R,42))

def main():
    need(__debug__,'assertions required')
    z=json.loads((HERE/'Root222F1G42.json').read_text());need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P,'scope')
    q=z['pivot'];n=q;chain=z['ecpp'];need(bool(chain) and q>2**64,'certified prime subject')
    for c in chain:need(c[0]==n,'wrong chain subject');n=C.pc.level(*c)
    need(C.pc.prime64(n) and all(C.pc.prime64(p)for p,h in P),'prime conditions')
    need(T%4==1 and sig(19,222)%(T*R)==0 and sig(R,42)%q==0 and exact(P) is not None,'Euler locked and mandatory target')
    folder=RESEARCH/'FinalNight2400/Root222';old=readz(folder/'TwoForests.json.gz')['cases']['1'];trip=readz(folder/'ThirdForests.json.gz')['cases'];d,raw=domain(P[:2],R)
    need(42 in d and '42' not in old and '1:42' not in trip,'historical exact second scope')
    L,tail=domain(P,q);need(L==[] and tail==4 and z['raw_tail']==tail,'complete empty mandatory domain')
    x=P+((q,2),);X=prod(p**h for p,h in x);S=prod(sig(p,h)//(1+h%2)for p,h in x);Y=S//gcd(X,S)
    need(X*Y>B and q>10**381,'strict sole even head')
    print('PASS canonical (19,222) f1:g42 complete; no live q valuation; strict raw tail',tail,'unique raw even head exceeds by integer size floor',floor10(X*Y),'levels',len(chain))

if __name__=='__main__':main()

"""Cold replay of a total exact-source split tree. Integer comparisons only."""
import argparse
from collections import Counter
from fractions import Fraction
from functools import cache
import gzip
import json
from math import prod
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Compose import ORDER, B, State, Forest, euler, pc, permitted, need, sigma, validate_forest, valuation
from Terminal import model, price, DYADIC, log_bounds
from Weighted import weighted


def integral(x):
    return type(x)==int


def abundancy(s, K):
    modes=[None] if s.fixed_euler else [None,*[q for q in K if euler(q,s.bad)]]
    def af(q,z):
        h=max(1,s.lo.get(q,1),valuation(s.D,q))
        f=h+((1-h)%4 if q==z else h%2)
        while not permitted(q,f,s.bad):
            f+=4 if q==z else 2
        return Fraction(sigma(q,f),q**f)
    base=prod(Fraction(sigma(q,f),q**f) for q,f in s.rows.items())
    return min(base*prod(af(q,z) for q in K) for z in modes)


def proof(packet, *, conditional=False):
    need(__debug__,'no -O')
    if conditional:
        need(set(packet)=={'assigned','present','absent','ecpp','leaf'},'conditional fields')
        assigned=packet['assigned'];p,e=assigned[0]
    else:
        need(set(packet)=={'p','e','ecpp','tree'},'packet fields')
        p,e=packet['p'],packet['e']
    need(integral(p) and p in (13,19,31) and integral(e) and 2<=e<=2400 and e%2==0,'pair')
    bank=packet['ecpp'];seen=set();counts=Counter();bounds=[];term=[]
    @cache
    def prime(q):
        if not integral(q) or q<=2:
            return False
        if q<2**64:
            return pc.prime64(q)
        z=q
        c=bank[str(z)]
        need(isinstance(c,list) and c,'missing proof')
        for row in c:
            need(z==row[0],'bad proof link')
            z=pc.level(*row)
        seen.add(str(q))
        return pc.prime64(z)
    def walk(rows,yes,no,lo,t):
        s=State(rows,yes,no,lo)
        kind=t['kind'];counts[kind]+=1
        if kind=='direct':
            need(set(t)=={'kind'} and (s.conflict or s.base>B),'not direct')
        elif kind=='abundance':
            K=t['support']
            need(set(t)=={'kind','support'} and len(set(K))==len(K),'support')
            need(all(prime(q) and q not in s.rows and (s.D%q==0 or q in s.present) for q in K),'not compelled')
            need(abundancy(s,K)>2,'not abundant')
        elif kind=='forest':
            need(set(t)=={'kind','roots','owners','head'},'forest fields')
            K,o,h=(t[k] for k in ('roots','owners','head'))
            validate_forest(s,K,o,h,prime)
            b,_=Forest(s,K,o,h).lower()
            need(b>B,'forest remains open')
            bounds.append(b)
        elif kind=='weighted':
            need(set(t)=={'kind','mu','roots','owners','head'},'weighted fields')
            K,o,h=(t[k] for k in ('roots','owners','head'))
            validate_forest(s,K,o,h,prime)
            w=weighted(s,K,dict(o),h,t['mu'])
            den=log_bounds(10)[1]
            need(w>2400*den,'weighted remains open')
            term.append(w//den)
        elif kind=='terminal':
            need(set(t)=={'kind','promoted','edges','weights'},'terminal fields')
            # Recompute every coefficient and all group minima with outward logs.
            d=model(s,t['promoted'],t['edges'],prime)
            w=price(d,t['weights']);den=DYADIC*log_bounds(10)[1]
            need(w>2400*den,'terminal remains open')
            term.append(w//den)
        elif kind=='support':
            need(set(t)=={'kind','q','yes','no'},'support fields')
            q=t['q'];need(prime(q) and q not in s.bad and q not in s.rows and q not in s.present,'support scope')
            walk(rows,(*yes,q),no,lo,t['yes'])
            walk(rows,yes,(*no,q),lo,t['no'])
        elif kind=='exp':
            need(set(t)=={'kind','q','cut','cells','tail'},'exponent fields')
            q,cut=t['q'],t['cut'];need(prime(q) and q not in s.rows and q not in s.bad and (q in s.present or not s.D%q),'split scope')
            need(integral(cut) and 1<=cut<=6000 and cut>=lo.get(q,1),'split cut')
            v=valuation(s.D,q)
            cells=[f for f in range(1,cut+1) if s.possible(q,f,v)]
            need(type(t['cells'])==dict and set(t['cells'])=={str(f) for f in cells},'incomplete exact split')
            for f in cells:
                walk([*rows,(q,f)],yes,no,{r:k for r,k in lo.items() if r!=q},t['cells'][str(f)])
            walk(rows,yes,no,{**lo,q:cut+1},t['tail'])
        else:
            raise ValueError('unknown leaf: '+str(kind))
    if conditional:
        yes,no=packet['present'],packet['absent']
        need(len(assigned)==len(dict(assigned)) and all(prime(q) and integral(f) and 1<=f<=6000 for q,f in assigned),'assigned scope')
        need(len(set(yes+no))==len(yes+no) and all(prime(q) and q not in ORDER[:ORDER.index(p)] and q!=p for q in yes+no),'conditional support')
        walk(assigned,yes,no,{},packet['leaf'])
    else:
        walk([(p,e)],(),(),{},packet['tree'])
    need(seen==set(bank),'extraneous certificates')
    return p,e,dict(counts),len(str(min(bounds)))-1 if bounds else None,min(term,default=None)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--conditional',action='store_true',help='replay a conditional leaf without claiming an exponent')
    ap.add_argument('packet',type=Path,nargs='+')
    a=ap.parse_args()
    for f in a.packet:
        data=f.read_bytes()
        if f.suffix=='.gz':
            data=gzip.decompress(data)
        D=json.loads(data)
        ans=proof(D,conditional=a.conditional)
        if a.conditional:
            print('CONDITIONAL ONLY',D['assigned'],'present',D['present'],'absent',D['absent'],ans,flush=True)
        else:
            print('PASS',ans,flush=True)


if __name__=='__main__':
    main()

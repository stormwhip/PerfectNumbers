"""Discovery of nested certificates; strict replay of every claimed full first fiber."""
from functools import cache
from pathlib import Path
from math import prod
import argparse,gzip,json,sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')]
from Coverage import domain,PIVOTS,B,require,legal_prefix,prime64,prime,POCK,ORDER
from SupplementalPrimes import CERT, prime_extra
from PivotCheck import C,exact_leaf,floor10


def children(rows,z):
    s=C.State(rows);require(s.D%z==0 and z not in s.rows and z not in s.bad,'split base')
    c=C.valuation(s.D,z);f=c;prod0=s.base;result=[]
    while prod0<=B:
        new=[*rows,(z,f)]
        if legal_prefix(new,s.bad):result.append(f)
        f+=1;prod0*=z
    require(prod0>B and prod0//z<=B,'strict split tail')
    return result,f


def certifier(book):
    from hashlib import sha256
    R=H.parents[1]
    @cache
    def proof(z):
        if z<2**64:return prime64(z)
        if z in POCK:return prime(z)
        if z in CERT:return prime_extra(z)
        key=str(z)
        if key not in book:
            path=R/'NightOrder/ECPP'/(sha256(key.encode()).hexdigest()[:24]+'.json.gz')
            book[key]=json.loads(gzip.decompress(path.read_bytes()))
        c=z
        for row in book[key]:
            require(row[0]==c,'broken ECPP');c=C.pc.level(*row)
        return prime64(c)
    return proof


def verify_row(row,cert):
    p,e,f=row['p'],row['e'],row['f'];q=PIVOTS[p,e];require(f in domain(p,e)[0],'raw first state');n=0;splits=0;atoms=None
    def walk(prefix,t):
        nonlocal n,splits,atoms
        state=C.State(prefix);require(not state.conflict and state.base<=B and legal_prefix(prefix,state.bad),'not a live prefix')
        if 'split' in t:
            require(set(t)=={'split','cases'} and cert(t['split']),'bad split')
            z=t['split'];ks,tail=children(prefix,z);require(set(t['cases'])==set(map(str,ks)),'omitted live child');splits+=1
            for h in ks:walk([*prefix,(z,h)],t['cases'][str(h)])
        elif t=={'price':'Seal25'}:
            from Seal25 import ROWS,certify
            require(prefix==ROWS,'Seal25 prefix mismatch')
            certify();n+=1;atoms=2400 if atoms is None else min(atoms,2400)
        else:
            require(set(t)=={'roots','owners','head'},'bad leaf')
            k,o,h=[t[a] for a in ('roots','owners','head')];C.validate_forest(state,k,o,h,cert);n+=1
            u=min(C.Forest(state,k,o,h).lower()[0],exact_leaf(prefix,k,o,h));require(u>B,'nonstrict forest')
            fl=floor10(u);atoms=fl if atoms is None else min(atoms,fl)
    walk([(p,e),(q,f)],row['tree']);return n,splits,atoms


def discover(a):
    from ProbeForest import Bank, Finder, seek
    tfs=[int(z) for z in a.fs];K=(a.p,a.e);bank=Finder(Bank(Path(a.bank)),True);q=PIVOTS[K]
    for f in tfs:
        parts=[(*K,),(q,f)];s=C.State(parts);require(f in domain(*K)[0],'outside raw domain');opts=set()
        for z,h in parts:opts.update(r for r in bank.factors(z,h) if r not in s.rows and s.D%r==0)
        opts=sorted(opts,reverse=True)
        if not opts:print('no seed',*K,f,flush=True);continue
        def hunt(parts,depth):
            from Seal25 import ROWS
            if parts==ROWS:return {'price':'Seal25'}
            leaf=seek(bank,parts,None,a.head,a.steps)
            if 'floor' in leaf:return {k:leaf[k] for k in ('roots','owners','head')}
            if depth<=0:return None
            state=C.State(parts);avail=set()
            for z,h in parts:avail.update(r for r in bank.factors(z,h) if r not in state.rows and state.D%r==0)
            for z in sorted(avail,reverse=True)[:a.try_bases]:
                fs,t=children(parts,z); out={}
                if len(fs)>a.fanout:continue
                for h in reversed(fs):
                    item=hunt([*parts,(z,h)],depth-1)
                    if item is None:break
                    out[str(h)]=item
                else:return dict(split=z,cases=out)
            return None
        for z in opts[:a.try_bases]:
            fs,t=children(parts,z);live=[];proofs={};cut=[]
            if len(fs)>a.fanout: print('split capped',*K,f,z,len(fs),flush=True);continue
            for h in reversed(fs):
                tr=hunt([*parts,(z,h)],a.depth)
                if tr is None:live.append(h)
                else:proofs[str(h)]=tr;cut.append(h)
            print('split',*K,f,z,'proof',len(proofs),'of',len(fs),'live',sorted(live),'tail',t,flush=True)
            book={};verify=certifier(book)
            if not live:
                row=dict(p=a.p,e=a.e,f=f,tree=dict(split=z,cases=proofs));r=verify_row(row,verify)
                payload=dict(row=row,ecpp=book);file=H/f'Second-{a.p}-{a.e}-{f}.json.gz'
                file.write_bytes(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0));print('PASS full conditional',r,file.name,flush=True);break


def main():
    a=argparse.ArgumentParser();a.add_argument('--verify',type=Path,nargs='*');a.add_argument('--try-bases',type=int,default=1);a.add_argument('--depth',type=int,default=0);a.add_argument('--fanout',type=int,default=180);a.add_argument('--head',type=int,default=75);a.add_argument('--steps',type=int,default=120);a.add_argument('--bank',default='/home/storm/opn');a.add_argument('--p',type=int);a.add_argument('--e',type=int);a.add_argument('fs',nargs='*');u=a.parse_args()
    if u.verify is not None:
        for f in u.verify:
            d=json.loads(gzip.decompress(f.read_bytes()));require(set(d)=={'row','ecpp'},'packet fields');book=d['ecpp'];used=set()
            @cache
            def prime_off(z):
                if z<2**64:return prime64(z)
                if str(z) not in book:
                    if z in POCK:return prime(z)
                    if z in CERT:return prime_extra(z)
                t=z;used.add(str(z))
                for a in book[str(z)]:require(a[0]==t,'ECPP subject');t=C.pc.level(*a)
                return prime64(t)
            print('PASS',f.name,verify_row(d['row'],prime_off),flush=True)
            require(used==set(book),'unused ECPP')
    else:discover(u)

if __name__=='__main__':
    if not __debug__:raise SystemExit('assertions are required in frozen second verifier')
    main()

#!/usr/bin/env python3
"""Join the exact t^1 partition, frozen h>=6, and proof-grade replacements h=2,4."""
import argparse
import hashlib
import json
from math import gcd
from pathlib import Path
import runpy
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ASTRA=HERE.parent
FROZEN=ASTRA.parent/'GeminiFrontier'/'November28'
B=10**2400
BASE=((19,276),(1176672733,1))
PIVOT=1109


def need(ok,why):
    if not ok:
        raise ValueError(why)


def lfhash(f):
    return hashlib.sha256(f.read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def baseline():
    py=FROZEN/'Submitted.py';js=FROZEN/'Certificates.json'
    need(lfhash(py)=='8ba69b99be28e0ef11968dac1afc24e5e187b432b4298c0c035dba09be7daa99','frozen accepted primal verifier')
    need(lfhash(js)=='ef8ade9bd3fbce68c80ccc66f33041cc32313f7dd29810529a9201ce5f055bc8','frozen accepted certificate')
    V=runpy.run_path(str(py));doc=json.loads(js.read_bytes());P=V['verify_pratt_certificates'](doc['CertifiedPrimes'])
    row,=tuple(p for p in doc['Proofs'] if p['ProofID']=='E_t1_split_1109')
    need(tuple((int(p),h) for p,h in row['ExactPrefix'])==BASE and row['Key']==[19,276] and row['CanonicalBans']==[] and row['Parameters']['open_children']==[2,4],'frozen exact orientation')
    r=V['verify_e_t1_split_1109'](row,P)
    need(r=='PARTIAL_CLOSED (136/138 closed, tail=555, OPEN=[2, 4], U19_exc=4, U1109=1)','frozen accepted output differs')
    print('PASS frozen audited children h=6,8,...,276 (136 total); no historical h=2 or h=4 reused',flush=True)


def independent_domain():
    # Geometric sums rebuilt separately from the frozen exact splitter.
    p,e=BASE[0];t,j=BASE[1];s=PIVOT
    geom=lambda p,a: (pow(p,a+1)-1)//(p-1)
    X=p**e*t**j
    G=geom(p,e)*geom(t,j)
    need(G%4==2 and t%4==1,'Euler locked')
    Y=G//2
    D=Y//gcd(Y,X)
    need(D%s==0 and D%(s*s)!=0,'forced 1109 valuation')
    tail=1
    while X*(D//s)*s**tail<=B:
        tail+=1
    live=[]
    for h in range(2,tail,2):
        Xh=X*s**h;Gh=G*geom(s,h);Yh=Gh//2
        if Gh<=2*Xh and Xh*(Yh//gcd(Xh,Yh))<=B and all(Yh%q**(f+1) for q,f in (*BASE,(s,h))):
            live.append(h)
    need(tail==555 and live==list(range(2,278,2)),'independent full source domain')
    return live,tail


def call(file):
    subprocess.run((sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(file)),check=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--independent',action='store_true',help='also run separate audit reimplementations for h=2 source partition and h=4')
    args=ap.parse_args()
    need(__debug__,'assertions enabled for dependencies')
    live,tail=independent_domain()
    baseline()
    leaf4=json.loads((HERE/'Certificate276H4.json').read_bytes())
    leaf2=json.loads((HERE/'Certificate276H2Partial.json').read_bytes())
    exact=lambda q: tuple(tuple(row) for row in q)
    need(exact(leaf4['exactPrefix'])==(*BASE,(PIVOT,4)) and exact(leaf2['exactPrefix'])==(*BASE,(PIVOT,2)),'receipt exact prefixes')
    residual=exact(leaf2['jointInboundPrice']['remainingExactPrefix'])
    need(residual==(*BASE,(PIVOT,2),(13,276)),'h=2 receipt residual')
    call(HERE/'Verify276.py')
    call(HERE/'Explore276H2.py')
    if args.independent:
        call(ASTRA/'Audit'/'Check19x276x1109x4.py')
        call(ASTRA/'Audit'/'Check19x276x1109x2.py')
    hard=ASTRA/'Nineteen'/'VerifyHard13.py'
    bindings={'VerifyHard13.py':'ed2d70936636586c23cae337cb2859cae6632734d3328b0e7e1ac2de549cb8f2','Hard13Certificate.json':'e852382715e8c8855254499edc8a20d0520b7660c16a75f81f52ea4b03d74a12','Net13.py':'765a641acce03dd08eb52a46e98cf99f18c4c061f16562af359044194eec735d','E4Price.py':'43f29e073ef95e29cf62c3eb453aaa5420a32ff8a1d24e505c90a4509ff36ba2','Pock.py':'63ed2f815e4dc63153729b994fe6f827f31d65d21a1db248428b9427122067a6'}
    need(all(lfhash(hard.with_name(name))==digest for name,digest in bindings.items()),'sealed Hard13 input binding')
    # The imported code binds its own exact PREFIX through Net13; check
    # that same module and singleton residual at this interface.
    net=runpy.run_path(str(hard.with_name('Net13.py')))
    need(tuple(net['PREFIX'])==residual,'hard-emitter exact prefix')
    call(hard)
    need(set(live)=={2,4}|set(range(6,278,2)),'exclusion union')
    print('EXCLUDED parent fiber (19,276), t=1176672733 exponent 1: 138/138 live children, strict raw tail',tail)
    print('Accounting: one first-pivot parent fiber; no additional key or shard closure.')


if __name__=='__main__':
    main()

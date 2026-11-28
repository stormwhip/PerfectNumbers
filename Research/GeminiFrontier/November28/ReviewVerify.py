#!/usr/bin/env python3
"""Independent acceptance overlay for the frozen November 28 submission."""
import hashlib
import json
import runpy
from fractions import Fraction
from math import prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'Submitted.py'
if not SOURCE.exists():
    SOURCE = HERE / 'verify(2).py'
CERT = HERE / 'Certificates.json'

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == '8ba69b99be28e0ef11968dac1afc24e5e187b432b4298c0c035dba09be7daa99', 'submitted verifier hash mismatch')
require(hashlib.sha256(CERT.read_bytes()).hexdigest() == 'ef8ade9bd3fbce68c80ccc66f33041cc32313f7dd29810529a9201ce5f055bc8', 'certificate hash mismatch')
V = runpy.run_path(str(SOURCE))
D = json.loads(CERT.read_text())
P = V['verify_pratt_certificates'](D['CertifiedPrimes'])
B = 10**2400
require(3**5030 <= B < 3**5031, 'exponent cap')

# Work throughout with deficits raised to the tenth power, w=19/10.
def add(tab, b, ratio):
    if ratio > tab.get(b, Fraction(1)):
        tab[b] = ratio

def single(s, o, h, c, fixed, bans):
    require(h >= 2 and 10*h >= 19, 'invalid exponent budget')
    lim = min(c, (19*c + 10*h - 1)//(10*h))
    roots = V['hensel_ord_k'](s, P[s]['g'], o, lim)
    out = {}
    for z in range(1, lim+1):
        cap = s**(19*(c if z == lim else z))
        for b in roots[z]:
            if b < 3 or b % 2 == 0 or b.bit_length() > cap.bit_length()//(10*h)+2:
                continue
            if b**(10*h) >= cap or not V['can_be_valid_base'](b, fixed, bans, True):
                continue
            # Smaller-order roots are retained as a safe relaxation.
            u = min(c, V['vp'](b**o-1,s))
            add(out,b,Fraction(s**(19*u),b**(10*h)))
    return out

def joint_cubic(s, c1, c2, fixed, bans):
    r1 = V['hensel_ord_k'](19,P[19]['g'],3,c1)
    r2 = V['hensel_ord_k'](s,P[s]['g'],3,c2)
    out = {}
    p1 = [19**i for i in range(c1+1)]
    p2 = [s**i for i in range(c2+1)]
    for i,m1 in enumerate(p1):
        for j,m2 in enumerate(p2):
            if not (i or j):
                continue
            M = m1*m2
            if not i:
                roots=r2[j]
            elif not j:
                roots=r1[i]
            else:
                inv=pow(m1,-1,m2)
                roots=[a+m1*((b-a)*inv%m2) for a in r1[i] for b in r2[j]]
            for b in roots:
                if b < 3 or b%2==0 or 20*(b.bit_length()-1)>=19*M.bit_length():
                    continue
                if b**20 >= M**19 or not V['can_be_valid_base'](b,fixed,bans,True):
                    continue
                add(out,b,Fraction(M**19,b**20))
    return out

def verify_joint(proof):
    rows=[(int(p),int(h)) for p,h in proof['ExactPrefix']]
    bans=set(V['canonical_bans'](proof['Key'][0]))
    X,T,S,_=V['exact_state'](rows,bans,P)
    fixed=dict(rows)
    s1,s2=map(int,proof['Parameters']['targets'])
    require(s1==19 and proof['Parameters']['weight_num']==19 and proof['Parameters']['weight_den']==10,'weight/target mismatch')
    require(sum(h%2 for p,h in rows)==1,'Euler not fixed')
    c1=fixed[19]-V['vp'](S,19)
    c2=fixed[s2]-V['vp'](S,s2)
    require(c1>0 and c2>0,'invalid demand')
    require(P[19]['factors']=={2:1,3:2},'19 support')
    require(s2-1>=5031 and s2>=5031 and (s2-1)%19!=0 and (s2-1)%9!=0,'second target support')
    require(3**180>19**19 and 3**540>19**19 and 3**1620>19**19,'LTE dominance')
    # 19 order 1: 19^u-1 >=18u. For order 3/9 the extra length
    # o*(19^k-1) >= 54k pays for the additional 19-adic valuation.
    cubic=joint_cubic(s2,c1,c2,fixed,bans)
    a3=single(19,3,2,c1,fixed,bans)
    a9=single(19,9,6,c1,fixed,bans)
    b3=single(s2,3,2,c2,fixed,bans)
    high={}
    orders=V['get_odd_divisors_up_to'](P[s2]['factors'],5031)
    require(3 in orders,'missing cubic order')
    for o in orders:
        if o>3:
            for b,r in single(s2,o,o-3,c2,fixed,bans).items():
                add(high,b,r)
    # Cases: both cubic; order 9 with cubic; order 1 or no 19 supply with
    # cubic; any higher second-target order with either first-target order.
    U=Fraction(1)
    one=Fraction(1)
    keys=set(cubic)|set(a3)|set(a9)|set(b3)|set(high)
    for b in keys:
        x,y,z,t,v=(tab.get(b,one) for tab in (cubic,a3,a9,b3,high))
        U*=max(x,y,z,t,v,z*t,max(y,z)*v)
    require(X**10*(19**c1*s2**c2)**19*U.denominator>B**10*U.numerator,'supplemented joint bound failed')
    import math
    lb=math.log10(X)+1.9*(c1*math.log10(19)+c2*math.log10(s2))-(math.log10(U.numerator)-math.log10(U.denominator))/10
    print(f"[ACCEPTED] {proof['ProofID']} complete joint order audit: {len(keys)} deficit bases, log10 lower bound {lb:.6f}")

for proof in D['Proofs']:
    pid=proof['ProofID']
    method=proof['Method']
    if method=='rational_joint_pricing_fixed_euler':
        verify_joint(proof)
        continue
    # Original arithmetic is bound by the frozen hashes; the proof audit
    # supplies the analytic arguments (Review.md) rather than trusting labels.
    fn={
        'single_target_pricing_fixed_euler':'verify_single_target_fixed_euler',
        'single_target_pricing_open_euler_ss_and_inner_div':'verify_single_target_open_euler_ss_and_inner',
        'single_target_pricing_open_euler_qr_outer':'verify_single_target_open_euler_qr_outer',
        'split_and_coprime_dual_pricing_fixed_euler':'verify_e_t1_split_1109',
    }[method]
    params=proof['Parameters']
    if 'target' in params:
        require(params['primitive_root']==P[int(params['target'])]['g'],'primitive root mismatch')
    else:
        require(params['primitive_root_1109']==P[1109]['g'],'1109 primitive root mismatch')
    print('[ACCEPTED]',pid,V[fn](proof,P))

#!/usr/bin/env python3
"""Reviewed conditional leaf T^10 of (19,58); no full-key credit."""
import hashlib
from pathlib import Path
import runpy
import subprocess
import sys
import time
from math import gcd

assert __debug__
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
raw = HERE / "FollowupSubmitted.py"
assert hashlib.sha256(raw.read_bytes()).hexdigest() == "8f654bcdeacc16a303b285a5f42713738c94a991d6decc83b15ba15e387b57e4"
history = ROOT / "Research" / "Night2400" / "C10"
assert hashlib.sha256((history / "EulerF1.json.gz").read_bytes()).hexdigest() == "f52b0f8b3fd0f8e869e0e38f7d6ac34cf0254a1082dce5c2ad8df3f2ca7f5c90"
v = runpy.run_path(str(raw))
for p in v["PRATT_CERTS"]:
    v["verify_prime"](p)
for k in ("B","sigma","odd","val","state_eval","SMALL_PRIMES","lift_phi3_table","primitive_roots_of_unity_mod_p","verify_prime"):
    globals()[k] = v[k]

def verify_19_58_T10():
    t0 = time.time()
    p, e = 19, 58
    t = 155306613932666028670208812450645212905178047040045530562317564121001023821
    T = 25884435655444338111701468741774202150863007840007588427052927353500170637
    # Historical premises (Section 3.1): t and T are certified primes; v_t(N)=1 fixes Euler slot.
    assert odd(sigma(19, 58)) == t
    assert t + 1 == 6 * T
    rows = {19: 58, t: 1, T: 10}
    X, S, D = state_eval(rows, ())
    assert val(S, 19) == 0 and val(S, T) == 1
    assert val(S, 3) == 1 and val(S, 67) == 1 and val(S, 125687) == 1
    # Verify odd(T-1) has no prime factor in [5, 4918] and 3^(50*4918) > T^(99*9)
    odd_Tm1 = odd(T - 1)
    assert odd_Tm1 % 3 == 0
    while odd_Tm1 % 3 == 0:
        odd_Tm1 //= 3
    for q in SMALL_PRIMES:
        if q < 5:
            continue
        if q >= 4919:
            break
        assert odd_Tm1 % q != 0, f"Unexpected factor {q} of T-1"
    w_num, w_den = 99, 50
    c1, c2 = 58, 9
    assert pow(3, w_den * 4918) > pow(T, w_num * c2)

    # Exact two-target {19, T} deficit at w = 99/50 (o=3,9 for 19; o=3 for T; CRT at f=2)
    t1 = lift_phi3_table(19, c1)
    t2 = lift_phi3_table(T, c2)
    best = {}

    def rec(r, exp_f, M):
        if r <= 2 or r % 2 == 0 or r in rows:
            return
        if r > 37 and any(r % sp0 == 0 for sp0 in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
            return
        if w_den * exp_f * (r.bit_length() - 1) >= w_num * M.bit_length():
            return
        rf = pow(r, w_den * exp_f)
        mw = pow(M, w_num)
        if rf < mw:
            g0 = gcd(mw, rf)
            num, den = mw // g0, rf // g0
            if r not in best or num * best[r][1] > best[r][0] * den:
                best[r] = (num, den)

    # Complete residue search: orders 3 and 9 for 19, order 3 for T.
    table9 = []
    roots9 = primitive_roots_of_unity_mod_p(19, 9)
    mod = 19
    for u in range(1,c1+1):
        table9.append((mod,roots9))
        nmod=mod*19
        roots9=[r+((-(pow(r,9,nmod)-1)//mod*pow(9*pow(r,8,19),-1,19))%19)*mod for r in roots9]
        assert all(pow(r,9,nmod)==1 for r in roots9)
        mod=nmod
    assert X*3**4918>B
    assert val(T-1,3)==1 and T>B.bit_length()+1
    assert 3**(50*3*18)>19**99
    assert 39**(50*18)>19**99
    assert 39**(50*50)>19**99
    for table,h in [(t1[1:],2),(table9,8)]:
        for m,rs in table:
            for r in rs: rec(r,h,m)
    for m,rs in t2[1:]:
        for r in rs: rec(r,2,m)
    for table,h in [(t1[1:],2),(table9,8)]:
        for m1,rs1 in table:
            for m2,rs2 in t2[1:]:
                for r1 in rs1:
                    for r2 in rs2:
                        r=r1+m1*((r2-r1)*pow(m1,-1,m2)%m2)
                        rec(r,h,m1*m2)
    assert len(best)==12
    print("PASS complete mixed-order deficit enumeration: 12 candidates")
    U_num, U_den = 1, 1
    for r, (num, den) in best.items():
        U_num *= num
        U_den *= den
        g0 = gcd(U_num, U_den)
        U_num //= g0
        U_den //= g0
    deficit_set = set(best.keys())

    def min_net(q, min_g=2):
        verify_prime(q)
        assert pow(q, 3, T) != 1 and q not in deficit_set
        if pow(q, 9, 19) != 1:
            return pow(q, min_g * w_den), 1
        best_n, best_d = None, None
        p19_all = pow(19, w_num * c1)
        for g in range(min_g, 60, 2):
            if best_n is not None and pow(q, g * w_den) * best_d >= best_n * p19_all:
                break
            u = min(val(sigma(q, g), 19), c1)
            n, d = pow(q, g * w_den), pow(19, w_num * u)
            assert n >= d
            if best_n is None or n * best_d < best_n * d:
                best_n, best_d = n, d
        else:
            if best_n is None or best_n > best_d:
                best_n, best_d = 1, 1
        g0 = gcd(best_n, best_d)
        return best_n // g0, best_d // g0

    def mul_frac(a, b):
        n, d = a[0] * b[0], a[1] * b[1]
        g0 = gcd(n, d)
        return n // g0, d // g0

    def min_frac(fracs):
        bn, bd = fracs[0]
        for n, d in fracs[1:]:
            if n * bd < bn * d:
                bn, bd = n, d
        return bn, bd

    # Base V_lhs includes 3^2 * 67^2 (both disjoint from {19, T} suppliers!)
    for r in (3, 67, 125687):
        verify_prime(r)
        assert pow(r, 9, 19) != 1 and pow(r, 3, T) != 1
    V_lhs = pow(X * 9 * (67**2), w_den) * pow(pow(19, c1) * pow(T, c2), w_num) * U_den
    B_rhs = pow(B, w_den) * U_num

    # Helper: minimum extra factor from 67 (on top of 67^2) disjoint from {3, 13, 19, 53, 67, 125687, 173597227, 181, 487}:
    # 67^2 -> 31 (sigma(67^2) = 3 * 7^2 * 31); 67^4 -> 67^2 * 761; 67^6 -> 67^4
    assert odd(sigma(67, 2)) % 31 == 0 and odd(sigma(67, 4)) % 761 == 0
    ex67 = min_frac([
        min_net(31, 2),
        mul_frac((pow(67, 2 * w_den), 1), min_net(761, 2)),
        (pow(67, 4 * w_den), 1),
    ])


    def check_leaf(f125, extra_frac):
        lhs = V_lhs * pow(125687, w_den * f125) * extra_frac[0]
        rhs = B_rhs * extra_frac[1]
        assert lhs > rhs, f"T^10 leaf f125={f125} failed!"

    # 1. Tail f >= 14
    check_leaf(14, (1, 1))
    # 2. f = 12: 17407547 | sigma(125687^12)
    assert odd(sigma(125687, 12)) % 17407547 == 0
    check_leaf(12, min_net(17407547, 2))
    # 3. f = 10: 43801796098899607800288307117 | sigma(125687^10)
    q10 = 43801796098899607800288307117
    assert odd(sigma(125687, 10)) % q10 == 0
    check_leaf(10, min_net(q10, 2))
    # 4. f = 8: 13, 173597227, 181, 487 | sigma(125687^8), plus ex67
    for q in (13, 173597227, 181, 487):
        assert odd(sigma(125687, 8)) % q == 0
    ef8 = ex67
    for q in (13, 173597227, 181, 487):
        ef8 = mul_frac(ef8, min_net(q, 2))
    check_leaf(8, ef8)
    # 5. f = 6: 1921626717304609841401 | sigma(125687^6)
    q6 = 1921626717304609841401
    assert odd(sigma(125687, 6)) % q6 == 0
    check_leaf(6, min_net(q6, 2))
    # 6. f = 4: q4 = 21721462127791 | sigma(125687^4)
    q4 = 21721462127791
    assert odd(sigma(125687, 4)) % q4 == 0
    check_leaf(4, min_net(q4, 4))  # q4 >= 4 tail
    assert odd(sigma(q4, 2)) % 1009 == 0 and odd(sigma(q4, 2)) % 48730759160069521 == 0
    check_leaf(4, mul_frac(min_net(q4, 2), mul_frac(min_net(1009, 2), min_net(48730759160069521, 2))))
    # 7. f = 2: 13 and q2 = 173597227 | sigma(125687^2)
    q2 = 173597227
    assert pow(q2, 9, 19) != 1 and pow(q2, 3, T) != 1
    assert odd(sigma(125687, 2)) % 13 == 0 and odd(sigma(125687, 2)) % q2 == 0
    ef13 = min_net(13, 2)
    check_leaf(2, mul_frac(ef13, min_net(q2, 8)))  # q2 >= 8 tail
    q2_6 = 11168733188620379036573096201712016319
    assert odd(sigma(q2, 6)) % q2_6 == 0
    check_leaf(2, mul_frac(ef13, mul_frac((pow(q2, 6 * w_den), 1), min_net(q2_6, 2))))
    for q in (571719123349875238781, 1588504383901):
        assert odd(sigma(q2, 4)) % q == 0
    check_leaf(2, mul_frac(ef13, mul_frac((pow(q2, 4 * w_den), 1), mul_frac(min_net(571719123349875238781, 2), min_net(1588504383901, 2)))))
    # q2 == 2: q_leaf = 10045332465228919 | sigma(q2^2)
    q_leaf = 10045332465228919
    assert odd(sigma(q2, 2)) % q_leaf == 0
    ef_q2_2 = mul_frac(ef13, (pow(q2, 2 * w_den), 1))
    check_leaf(2, mul_frac(ef_q2_2, min_net(q_leaf, 4)))  # q_leaf >= 4 tail
    q_l2 = 1748681585064818436665791
    assert odd(sigma(q_leaf, 2)) % q_l2 == 0
    check_leaf(2, mul_frac(ef_q2_2, mul_frac(min_net(q_leaf, 2), min_net(q_l2, 2))))

    dt = time.time() - t0
    print(f"[PASS] CONDITIONAL (19, 58) T^10 [P19_I00015]: two-target w=99/50, 12/12 leaves closed ({dt:.2f}s)")
    return {"name": "cond_19_58_T10", "time_s": round(dt, 2), "leaves": 12}

if __name__ == "__main__":
    if "--arithmetic-only" not in sys.argv:
        subprocess.run([sys.executable,"-I","-S","-B","-X","int_max_str_digits=0",str(history/"Verify.py")],cwd=ROOT,check=True)
    else:
        print("NOTE: C10 historical arithmetic not replayed by this invocation")
    verify_19_58_T10()

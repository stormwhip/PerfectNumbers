"""Exact replay of Gemini's candidate exponent exclusions."""
import argparse
from fractions import Fraction
from functools import cache
from math import gcd, isqrt, prod
import json
import VerifyTeichmullerValuation2400 as TB

B = TB.B
# Verified prime factors of C_x = sigma(x^(o-1)) / p^t for Theorem 2
EXTRA_CX_FACTORS = {
    (19, 1): [3],
    (19, 4): [61],
    (19, 46): [313],
    (19, 848): [13, 433, 739, 2683, 95713],
    (7, 8): [1978063],
    (7, 61): [3, 13],
    (7, 119): [3, 73, 160309],
    (7, 208): [3],
    (7, 855): [3],
    (11, 1): [71],
    (11, 8): [331, 2500601, 5241090776319991, 1733837318671, 4763238228611],
    (11, 19): [5, 51971],
    (11, 22): [9472721],
    (11, 47): [5, 2311],
    (11, 73): [71, 199411],
    (11, 116): [41, 631],
    (11, 314): [102461],
    (11, 337): [71, 191861],
    (31, 2): [3, 67, 283],
    (31, 3): [1327],
    (31, 8): [3, 96899530501],
    (31, 230): [3, 2723437, 7133233],
    (13, 20): [3121, 3593793042070502653],
    (13, 31): [3, 13597, 2739724132861, 131632421278843711],
}

CERT_FACTORS = {
    (7, 1084): [29, 311, 2801, 4733, 21143, 21391, 21701, 65101, 604997, 5325181, 2127431041, 77192844961, 3999088279399464409],
    (7, 1104): [131, 1531, 2801, 4931, 14009, 22543, 157951, 787021, 1173511, 2767631689, 16148168401],
    (7, 1120): [419, 2243, 8969, 459257, 4534166740403],
    (7, 1122): [855727, 1264499, 37085953],
    (7, 1126): [29, 47, 3083, 3529, 4733, 63113, 1074473, 13473433, 861893537, 31479823396757],
    (7, 1132): [1123, 2267, 17923, 293459],
    (7, 1134): [2801, 1271201],
    (7, 1138): [14009, 27337, 228337, 43111151, 2767631689],
    (11, 774): [3001, 3221, 21701, 24151, 50159, 1288051, 2428541, 279483601, 1856458657451],
    (11, 778): [83, 1231, 1559, 27061, 509221, 14092193, 29866451, 840139875599, 6115909044841454629],
    (11, 780): [1847, 15797, 64327, 1806113, 133347941],
    (11, 786): [75553, 461183],
    (11, 790): [43, 227, 1583, 45319, 45902861],
    (11, 792): [1093, 4759, 440177, 3158528101],
    (11, 796): [18262459],
    (11, 798): [2069, 50544702849929377],
    (11, 802): [15797, 1806113],
    (11, 804): [43, 211, 829, 967, 3221, 45319, 95911, 333041, 9532811, 9964291, 28878847, 48359249, 123730111, 559660151, 3740221981231],
    (11, 808): [1619, 5307671021],
    (11, 810): [7082691703],
    (11, 814): [3221, 78241, 2156491, 375768791],
    (11, 816): [4903, 2802311, 6115909044841454629],
    (11, 820): [41051, 1577963],
    (11, 822): [],
    (11, 826): [56237, 7645952417],
    (11, 828): [],
    (11, 832): [43, 239, 1667, 45319, 27805541, 50544702849929377],
    (11, 834): [2339, 3221],
    (11, 838): [2803939],
    (13, 818): [43, 53, 61, 79, 127, 337, 547, 1093, 4603, 6301, 8191, 10193, 21841, 34763, 117937, 149059, 259507, 264031, 825679, 961507, 1326781, 1519831, 1609669, 1803647, 2714377, 5229043, 7327657, 49463779, 737974693, 997294663, 57745124662681],
    (13, 824): [23, 61, 419, 701, 859, 1951, 2861, 3851, 4651, 9851, 18041, 30941, 161971, 1711051, 2752135920929651],
    (13, 836): [61, 311, 1117, 1303, 125551, 650971, 1609669, 52306921, 662781799, 57583418699431],
    (13, 844): [53, 131, 677, 1171, 6761, 16901, 30941, 156131, 264031, 1105261, 1242151, 1803647, 6171881, 14958191],
    (13, 846): [23, 419, 859, 3389, 18041, 25411, 4911149, 5229043, 11880023],
    (13, 854): [61, 181, 191, 571, 4651, 27361, 30941, 161971, 1531591, 1609669, 4986361, 10692289, 12865927, 9468940004449],
    (13, 860): [43, 61, 337, 547, 1340947, 2205883, 2714377, 5229043, 8639849, 16997863],
    (13, 862): [],
    (19, 692): [67, 127, 397, 523, 701, 2113, 29989, 54979, 70841, 73613, 104281, 104743, 568657, 1617463, 30640261, 34451077, 62060021, 68443621, 94192561, 324423793, 7302593769703],
    (19, 724): [59, 101, 151, 233, 911, 1601, 5801, 6451, 297003021451861, 36035657195482151, 165049085515149863],
    (19, 734): [31, 71, 127, 151, 211, 701, 911, 1471, 70841, 116131, 448351, 707561, 2460181, 30640261, 41888491, 68443621, 167291881],
    (19, 740): [79, 127, 157, 229, 599, 6841, 14821, 29251, 98801, 826957, 1058149, 12024949, 133338869, 887960971, 421451911540236097],
    (19, 744): [151, 911, 18812741],
    (19, 746): [127, 167, 523, 997, 4483, 29989, 323222917],
    (19, 748): [701, 70841],
    (19, 750): [14714032087],
    (19, 752): [127, 6516463],
    (31, 608): [43, 331, 349, 2437, 6301, 10789, 29581, 32887, 49823, 6226417, 24589681, 917087137, 1482570191, 11242578713, 189343400041, 2813432694367],
    (31, 620): [139, 331, 3637, 15733, 81343, 1164859, 1509997, 61562537, 78688153, 1836205027201, 126901881805771, 7176374761323733117],
    (31, 626): [23, 331, 397, 571, 617, 7639, 14251, 150332843, 224531627, 350533129],
    (31, 636): [2549, 6959, 10193, 42407, 1661479, 2426789, 7908811, 917087137],
    (31, 638): [331, 853, 3637, 17609, 24709, 81343],
}


def is_prime_det64(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == q:
            return True
        if n % q == 0:
            return False
    if n >= (1 << 64):
        return False
    d, s = n - 1, 0
    while (d & 1) == 0:
        d >>= 1
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def val(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def ilog(n, b):
    if n < 1:
        return -1
    k = (n.bit_length() - 1) // b.bit_length()
    while b**(k + 1) <= n:
        k += 1
    return k


@cache
def root(n, k):
    if k == 1:
        return n
    if k == 2:
        return isqrt(n)
    if n <= 1:
        return n
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // x**(k - 1)) // k
        if y >= x:
            return x
        x = y


@cache
def surplus(p, kap, r, c):
    f0 = 2 * ((c + 1) // 2)
    o = TB.multiplicative_order(r, p)
    best = Fraction(r**f0)
    if o % 2 == 0:
        return best
    t = 0 if o == 1 else val(r**o - 1, p)
    j, step = 0, o
    while True:
        k = TB.ceil_div(f0 + 1, step)
        f = (k + (k % 2 == 0)) * step - 1
        best = min(best, Fraction(r**f, p**(kap * (t + j))))
        if step >= f0 + 1:
            return best
        step *= p
        j += 1


@cache
def euler_deficits(p, top):
    items = []
    for a in range(2, p - 1):
        o = TB.multiplicative_order(a, p)
        if o < 3 or o % 4 == 0:
            continue
        fm = TB.fmin_euler(o)
        x, mod = a, p
        for t in range(1, top + 1):
            next_x = pow(x, p, mod * p)
            if (x != next_x and x % 4 == 1 and x not in TB.forbidden(p)
                    and fm * (x.bit_length() - 1) < 5 * t * p.bit_length()
                    and x**fm < mod**5 and TB.may_be_prime(x)):
                items.append((t, Fraction(mod**5, x**fm)))
            x, mod = next_x, mod * p
    return items


def discounts(p, prof):
    used = {x for _, x, _ in prof.non_euler}
    out = []
    for t, x, o in prof.non_euler:
        delta = Fraction(p**(prof.kap*t), x**(o-1))
        sponsors = ()
        if x**(3*o-1) >= p**(prof.kap*t):
            sig = TB.sigma(x, o-1)
            if any(sig % z == 0 for z in TB.forbidden(p)):
                continue
            for w in EXTRA_CX_FACTORS.get((p,t), ()):
                if (w != p and w not in used and w not in TB.forbidden(p)
                        and sig % w == 0 and is_prime_det64(w)
                        and surplus(p, prof.kap, w, 1) >= delta):
                    used.add(w)
                    sponsors = (w,)
                    break
        out.append((t, x, delta, sponsors))
    return out


def loss(p,items, a1, s, q, emitter):
    result = Fraction(1)
    for _, x, delta, sponsors in items:
        if x == emitter:
            continue
        if not any(w != emitter and
                   (w % 4 == 3 or (a1 and (w < q or val(w+1, p) != s)))
                   for w in sponsors):
            result *= delta
    return result


@cache
def candidate_prime(q):
    return TB.may_be_prime(q)


def divisors(n):
    return [d for d in range(1, n+1) if n % d == 0]


@cache
def phi(p, m):
    n = p**m - 1
    for d in divisors(m)[:-1]:
        n //= phi(p, d)
    return n


def crt_y(a, y, m):
    return 1 + m * ((a-1) * pow(m, -1, y) % y)


def divides_a(p, e, y, lo, hi):
    """Whether a possible q in [lo, hi] remains in a cyclotomic factor."""
    for h in divisors(e+1)[1:]:
        ph = phi(p,h)
        if lo > min(hi, ph):
            continue
        if h >= 2*y-1:
            return True
        if h % p == 0:
            continue
        q0 = crt_y(-1,y,4*h)
        step = 4*h*y
        u0 = crt_y(-ph,y,2*h) if gcd(ph,h)==1 else (-ph)%y or y
        limit = min(hi, ph//u0)
        q = q0 + max(0, TB.ceil_div(lo-q0,step))*step
        for _ in range(501):
            if q > limit:
                break
            if ph % q == 0:
                return True
            q += step
        else:
            if q <= limit:
                return True
    return False


def emitter_loss(p,items, s, q, lo, hi):
    """Upper bound on deficits of all primes other than the emitter."""
    u = loss(p,items, True, s, q, None)
    for _, _, _, sponsors in items:
        for w in sponsors:
            if lo <= w <= hi:
                u = max(u, loss(p,items, True, s, q, w))
    return u


def prime_data(p, kap, a, factors, reserved):
    out = []
    for r in factors:
        if not is_prime_det64(r) or a % r:
            raise ValueError((p, r, "invalid factor witness"))
        if r not in reserved:
            c = val(a,r)
            out.append((r,c,max(Fraction(1),surplus(p,kap,r,c))))
    return out


def exclude_emitter(p,e,s,q,pe,a,items,factors):
    kap = TB.kappa(p)
    y = p**s
    pnext = p*pe
    power = p**(kap*(e-s))
    size = pe*q
    odd = prod(r for r,c,_ in factors if c%2)
    sq = a//prod(r for r,c,_ in factors if c==1)
    eff = a*odd
    if size*eff > B:
        return True
    head = q*size
    s_all = prod((v for _,_,v in factors), start=Fraction(1))
    bound0 = B//(size*eff)
    w_hi = isqrt(bound0)
    u = emitter_loss(p,items,s,q,3,w_hi)
    if 2**kap * head**kap * power * s_all * eff**(kap-1) <= 3**kap * B**kap * u:
        return False
    eligible = [(r,c,v) for r,c,v in factors if 2*a*head <= 3*B*r**c]
    sg = s_all/max((v for _,_,v in eligible),default=Fraction(1))
    ag = eff//max((r for r,c,_ in eligible if c%2),default=1)
    room = B//(size*ag)
    for threshold in (y, y*q//pnext):
        for g in range(25):
            # D < 0 gives r^(g+1) > y. D > 0 gives r^(g+1) > y*q/P.
            if g and room**(g+1) <= threshold**g:
                break  # same size bound excludes every larger g
            low = max(3, root(threshold,g+1)+1)
            high = root(room,g) if g else a
            if high < low:
                continue
            for c in range(2-g%2, ilog(a,low)+1, 2):
                f = c+g
                if f < 2:
                    continue
                hi = min(high,root(sq if c>=2 else a,c))
                if hi < low:
                    continue
                sig_hi = TB.sigma(hi,f)
                if sig_hi < q:
                    continue
                b = min(e-s,ilog(sig_hi//q,p))
                if gcd(p-1,f+1)==1:
                    b = min(b,val(f+1,p))
                uu = emitter_loss(p,items,s,q,low,hi)
                if 2*head*power*sg <= 3*B*uu*p**((kap-1)*b):
                    return False
        else:
            return False
    return True


def branch(p,e,s,pe,a,items,factors):
    kap = TB.kappa(p)
    y = p**s
    if s == 0:
        u = loss(p,items,True,s,5,None)
        ss = prod((v for _,_,v in factors), start=Fraction(1))/max(
            (v for r,c,v in factors if c==1 and r%4==1 and val(r+1,p)==0),default=Fraction(1))
        return 5*pe*p**(kap*e)*ss > B*u
    for k in range(401):
        q = (4*k+2)*y-1
        u = loss(p,items,True,s,q,None)
        ss = prod((v for _,_,v in factors), start=Fraction(1))/max(
            (v for r,c,v in factors if c==1 and r%4==1 and r>=q and val(r+1,p)==s),default=Fraction(1))
        hi = B*u//(pe*p**(kap*(e-s))*ss)
        if q > hi:
            return True
        if not divides_a(p,e,y,q,hi) and exclude_emitter(p,e,s,q,pe,a,items,factors):
            return True
        if val(q+1,p)==s and candidate_prime(q):
            return False
    return False


def replay(selected):
    proved = []
    for p in sorted({p for p,e in selected}):
        prof = TB.Profile(p,max(e for pp,e in selected if pp==p))
        TB.check_lemmas(p)
        ds = discounts(p,prof)
        eds = euler_deficits(p,max(e for pp,e in selected if pp==p))
        for _,e in sorted(pair for pair in selected if pair[0]==p):
            pe,a = p**e, TB.sigma(p,e)
            items = [d for d in ds if d[0]<=e]
            reserved = {w for *_, ws in items for w in ws}
            fs = prime_data(p,prof.kap,a,CERT_FACTORS[p,e],reserved)
            dd = max((v for t,v in eds if t<=e),default=Fraction(1))
            ss = prod((v for _,_,v in fs),start=Fraction(1))/max(
                (v for r,c,v in fs if r%4==1), default=Fraction(1))
            if p**((1+prof.kap)*e)*ss <= B*dd*loss(p,items,False,0,5,None):
                print(p,e,"open a>=5",flush=True)
                continue
            for s in range(e+1):
                if not branch(p,e,s,pe,a,[d for d in items if d[0]<=e-s],fs):
                    print(p,e,"open s",s,flush=True)
                    break
            else:
                print(p,e,"proved",flush=True)
                proved.append((p,e))
    return proved


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root",type=int)
    parser.add_argument("--output",default="GeminiVerifiedExponents.json")
    args=parser.parse_args()
    selected=[pair for pair in CERT_FACTORS if not args.root or pair[0]==args.root]
    with open(args.output,"w") as out:
        json.dump(replay(selected),out)
        out.write("\n")


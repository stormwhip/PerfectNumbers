"""Exact supplier-product bounds for the p=3 and p=5 root classes."""

from bisect import bisect_right
from functools import lru_cache
from math import gcd, isqrt, prod
from fractions import Fraction

import Verify as base


def iroot(n, k):
    if k == 1 or n < 2:
        return n
    if k == 2:
        return isqrt(n)
    lo = 1 << ((n.bit_length() - 1) // k)
    hi = lo * 2
    while hi - lo > 1:
        mid = (hi + lo) // 2
        if mid**k <= n:
            lo = mid
        else:
            hi = mid
    return lo


@lru_cache(None)
def joint_items(p, unit):
    def bits(r, e):
        k = base.ilog(e+1, p) if r % p == 1 and e >= 64 else 0
        if r % p == 1 and e < 64:
            n = e+1
            while n % p == 0:
                k += 1
                n //= p
        return max(0, (r**e//unit**k).bit_length()-1)

    following = p**(base.ilog(65, p)+1)-1
    if 3**((following+1)*(p-1)) < unit:
        raise ValueError("Increase the exponent cutoff")
    items = []
    for r in base.PRIMES:
        if r > 1000:
            break
        if r <= 2 or r == p or r in base.forbids(p):
            continue
        b = min(bits(r, 64), bits(r, following))
        for f in range(2, 64, 2):
            if any(pow(r, f+1, h*(r-1)) == 1 for h in base.forbids(p)):
                continue
            b = min(b, bits(r, f))
        h = base.benefit(r)
        items.append((Fraction(b,h),h))

    # For r>1000 and k>=1, f>=p^k-1. The first
    # valuation unit costs >=1000^(p-1)/unit and the later ones
    # only increase the cost. Zero units cost at least 1000^2.
    if 1000**((p-1)*p) < unit:
        raise ValueError("Increase the prime cutoff")
    b = min(1000**2, 1000**(p-1)//unit).bit_length()-1
    tail = Fraction(b,base.SCALE//1000)
    return sorted(item for item in items if item[0] < tail), tail


def joint_bits(p, unit, demand):
    items, tail = joint_items(p,unit)
    cost = Fraction(0)
    for price, h in items:
        if demand <= 0:
            break
        take = min(h,demand)
        cost += take*price
        demand -= take
    return int(cost+tail*max(0,demand))


def outside_dual(p, Q, y, C, bits, prices):
    tail, named = prices
    minimum = 1 << bits
    if 3*C*tail**2 >= 2*Q*minimum:
        return False
    for r, tail_exp, cap_exp in named:
        lo = base.ilog(2*Q//3,r)+1
        hi = base.ilog(C,r)
        # An exact option consumes r^f. A tail option consumes no
        # more than r^cap_exp once its incoming requirements are paid.
        cap = C*r**cap_exp//minimum
        tail_hi = base.ilog(cap,r) if cap else 0
        limit = min(hi,max(tail_exp-1,tail_hi))
        for e in range(lo+lo%2,limit+1,2):
            if any(pow(r,e+1,h*(r-1))==1 for h in base.forbids(p)):
                continue
            if e >= tail_exp and e > tail_hi:
                continue
            sig = base.sigma(r,e)
            w = (-sig) % y
            w += ((sig-w)*pow(y,-1,4)%4)*y
            if w == 0:
                w = 4*y
            max_w = sig//Q
            if max_w-w >= 64*4*y:
                return False
            for q_cofactor in range(w,max_w+1,4*y):
                if sig % q_cofactor == 0:
                    return False
    return True


@lru_cache(None)
def verify_exponent(p, e, scan=128, exterior_bits=0, joint_unit=1, joint_lower_bits=0, max_named_prime=0, outside_prices=(0, ())):
    if p not in (3, 5) or e < 2 or e % 2:
        return None
    A = base.sigma(p, e)
    if p**e*A > base.B or gcd(A, prod(base.forbids(p))) > 1:
        return "BASE"
    R = base.B//(p**e*A)
    E = base.ilog(base.B, 3)
    k = bisect_right(base.incoming_costs(p), base.B//p**e)-1
    s = e-k-base.ilog(E+1, p)
    if s <= 0:
        return None
    y = p**s
    Q = 2*y-1
    if Q <= A and Q*(y+1) <= p**(e+1)-1:
        return None

    gift, shared_min = 0, 1001
    known_source_unit = base.B
    rem = A
    demand0 = base.log2_lower()-base.benefit(p)
    demand = demand0
    for r in base.PRIMES:
        if r > 1000:
            break
        if rem % r:
            continue
        v = 0
        while rem % r == 0:
            rem //= r
            v += 1
        if r % p == 1:
            gift += base.ilog(v+1, p)
            known_source_unit = min(known_source_unit,
                                    r**(p**(base.ilog(v+1,p)+1)-1-v))
        demand -= base.benefit(r)
    gift += base.ilog(rem, 1001**(p-1))
    for i in range(base.ilog(rem, 1001)):
        denom = 1000+2*i
        demand -= (base.SCALE+denom-1)//denom

    m = e+1
    if m in base.PRIME_SET and m > p:
        sparse = demand0
        for i in range(1, base.ilog(A, 2*m+1)+1):
            denom = 2*m*i
            sparse -= (base.SCALE+denom-1)//denom
        demand = max(demand, sparse)
        step = 2*m*p
        r = 1+step
        while r < 1+(scan+1)*step and pow(p,m,r**(p-1)) != 1:
            r += step
        gift = min(gift, base.ilog(A, r**(p-1)))
        first = next(r for r in base.PRIMES if r % p == 1 and r not in base.forbids(p))
        max_rate = max(first**(p-1),joint_unit)
        r = 1+step
        # Check the shared divisors below the exterior unit price.
        while r < min(1+(scan+1)*step,max_rate):
            if pow(p,m,r) == 1 and A % r == 0:
                v, value = 0, A
                while value % r == 0:
                    value //= r
                    v += 1
                known_source_unit = min(known_source_unit,
                                        r**(p**(base.ilog(v+1,p)+1)-1-v))
            r += step
        shared_min = max(shared_min,r)

    first = next(r for r in base.PRIMES if r % p == 1 and r not in base.forbids(p))
    shared_unit = min(shared_min,known_source_unit)
    unit = min(first**(p-1),shared_unit)
    while True:
        y = p**s
        Q = 2*y-1
        C = R//Q
        if not C:
            return "LIFT_SIZE"
        needs = demand-(base.SCALE+Q-2)//(Q-1)
        if (exterior_bits or joint_lower_bits) and Q <= max(1000001, max_named_prime):
            return None
        bits = max(exterior_bits, base.residual_bits(p, needs))
        j = base.ilog(2+4*(base.ilog(C, Q)//4), p)
        if not 1 <= joint_unit <= shared_unit:
            return None
        price = joint_unit if joint_lower_bits else 1 << (unit.bit_length()-1)
        joint = joint_bits(p,price,needs) if price <= first**(p-1) else 0
        joint = max(joint_lower_bits,joint)
        if (C >> joint) == 0:
            return "JOINT_SIZE"
        kmax = min(base.ilog(C, unit), base.ilog(C >> joint, price))
        new_s = e-gift-kmax-j
        if new_s <= s:
            break
        s = new_s

    T = C >> bits
    if not T:
        return "SUPPLIER_SIZE"

    # An exterior supplier r has r^f > 2Q/3. Its own size and its
    # sigma factor cost at least r^(2f)/p^k after removing the root part.
    least_power = 2*Q//3+1
    first_out = next(r for r in base.PRIMES if r > 2 and r != p and r not in base.forbids(p))
    other_bits = base.residual_bits(p, needs-base.benefit(first_out))
    if least_power**2 <= R*(E+1) and 3*(C >> other_bits) >= 2*Q:
        if not (exterior_bits and outside_prices[0] and
                outside_dual(p,Q,y,C,exterior_bits,outside_prices)):
            return None

    H = R*(E+1)

    def too_small(t, tr, y=y, Q=Q):
        return ((p-1)*A*tr < y*Q and
                3*(p-1)*A*t+2*Q*tr < 2*Q*y)

    def fixed_pair(r, gap, f, pk):
        v = f-gap
        local_s, local_Q, local_y, local_C = s, Q, y, C
        min_r = iroot(2*Q//3, f)+1
        if r < min_r or too_small(r**gap, r**(gap+1)):
            return True
        # A shared supplier of known f uses at least r^gap of the
        # residual budget while contributing at most v_p(f+1) units.
        if gap:
            kf = base.ilog(pk,p)
            while True:
                available = local_C//min_r**gap
                if not available or (available >> joint) == 0:
                    return True
                j = base.ilog(2+4*(base.ilog(available,local_Q)//4),p)
                ordinary = min(base.ilog(available,unit),base.ilog(available >> joint,price))
                new_s = e-gift-kf-ordinary-j
                if new_s <= local_s:
                    break
                local_s = new_s
                local_y = p**local_s
                local_Q = 2*local_y-1
                local_C = R//local_Q
                min_r = iroot(2*local_Q//3,f)+1
            r = min(r,iroot(local_C >> bits,gap))
            if r < min_r or too_small(r**gap,r**(gap+1),local_y,local_Q):
                return True
        s2, q2, y2, cap = local_s, local_Q, local_y, local_C
        if r > y2:
            return False
        # Rule out the exceptional quotient D/y2 = -p^(e+1-s2).
        u_max = A//min_r**v
        t, tr = r**gap, r**(gap+1)
        ep = p**(e+1)
        if (p-1)*u_max+tr >= ep and 3*(p-1)*A*t+2*q2*tr >= 2*q2*ep:
            return False

        # w*t <= cap*p^k follows from the same forced divisor as H.
        wt = min(Fraction(3*r**f*t,2*q2), cap*pk)
        ht = wt+(f+1)*t
        h_over_r = min(Fraction(3*r**(f-1),2*q2),
                       Fraction(cap*pk,min_r**(gap+1)))+Fraction(f+1,min_r)
        common = p**(e+1-s2)*h_over_r+Fraction(1,min_r)
        x_contribution = Fraction((p-1)*A,q2*y2)*ht
        sigma_ratio = (Fraction(3*r**(gap-1),2*q2) if gap
                       else Fraction(3,2*q2*min_r))
        y_contribution = Fraction((p-1)*A,y2)*(
            min(sigma_ratio,Fraction(cap*pk,min_r**(f+1)))+
            Fraction(f+1,min_r**(v+1)))+Fraction(ht,y2)
        return max(x_contribution,y_contribution)+common < 1

    # The shared supplier carries an even exponent f >= 2.
    sieve_lower = 2*m+1 if m in base.PRIME_SET and m > p else 3
    for gap in range(24):
        first_v = 1 if gap % 2 else 2
        for v in range(first_v, 26, 2):
            f = v+gap
            pk = 1
            m0 = f+1
            while m0 % p == 0:
                m0 //= p
                pk *= p
            if m0 == 1 and Q > f+1:
                # Any prime divisor of this geometric sum, other
                # than p, has odd order divisible by p.
                continue
            r = min(iroot(A,v),iroot(R*pk,f+gap))
            if gap:
                r = min(r,iroot(T,gap))
            if r >= sieve_lower and not fixed_pair(r,gap,f,pk):
                return None
        # For all larger valuations use the first untested value.
        v = 27 if gap % 2 else 26
        r = min(iroot(A,v),iroot(H,v+2*gap))
        if gap:
            r = min(r,iroot(T,gap))
        if r >= sieve_lower and not too_small(r**gap,r**(gap+1)):
            return None

    if not too_small(T, T*iroot(T, 24)):
        return None
    return "SUPPLIER_PRODUCT"

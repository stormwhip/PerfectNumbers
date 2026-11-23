"""Exact additive valuation duals for the exterior of cyclotomic root divisors."""

from functools import lru_cache
import gzip
import json
from math import isqrt

from RoadblockDual import SCALE, log_bounds, odd_primes
from TerminalCertificate import DYADIC, allowed, sigma, verify
from VerifyRootExponentCoverage import canonical_tasks

ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
TARGET = 2400
BOUND = 10**TARGET
CUTOFF = 22
TRIAL = 5000
PRIMES = tuple(odd_primes(TRIAL))
PRIME_SET = set(PRIMES)


@lru_cache(None)
def bounded_trial_factors(p,e):
    value = sigma(p,e)
    value //= value & -value
    result = {}
    for q in PRIMES:
        if q*q > value:
            if value in PRIME_SET:
                result[value] = 1
            break
        if value % q:
            continue
        k = 0
        while value % q == 0:
            k += 1
            value //= q
        result[q] = k
    return result


def model(root, lo, hi, mode, archive, branch=0, unit=1, cutoff=CUTOFF):
    """Build an exterior LP for an explicitly enumerated interval of prime m."""
    if root not in ORDER or not root < lo <= hi or mode not in ("ordinary", "any"):
        raise ValueError("invalid cohort")
    if type(unit) is not int or unit < 1 or (unit > 1 and (mode != "ordinary" or root not in (3,5))):
        raise ValueError("invalid valuation exchange rate")
    if type(cutoff) is not int or not CUTOFF <= cutoff <= 40:
        raise ValueError("invalid exact exponent cutoff")
    unit_price = log_bounds(unit)[1] if unit > 1 else 0
    if branch and (abs(branch) not in PRIME_SET or abs(branch) >= 2*lo+1 or abs(branch) == root):
        raise ValueError("invalid presence split")
    ms = tuple(t["exponent"]+1 for t in canonical_tasks(ORDER)
               if t["root"] == root and not t["exact"] and
               lo <= t["exponent"]+1 <= hi and t["exponent"]+1 in PRIME_SET)
    if not ms:
        raise ValueError("empty cohort")
    forbidden = ORDER[:ORDER.index(root)]
    if branch < 0:
        forbidden = (*forbidden, -branch)
    limit = min(TRIAL,2*lo)
    small = tuple(p for p in PRIMES if p <= limit and p != root and p not in forbidden)

    @lru_cache(None)
    def disjoint(q):
        return q != root and q not in forbidden and all(
            q < 2*m+1 or pow(root,m,q) != 1 for m in ms)

    archive_edges = {}
    for p,e,q,k in archive["edges"]:
        if p in small and e <= cutoff and disjoint(q):
            archive_edges.setdefault((p,e), {})[q] = k

    costs, gains = [], []
    by_prime, exact, special, tail_exp, sources = {}, {}, [], {}, {}

    def add(cost, gain):
        index = len(costs)
        costs.append(cost)
        gains.append(gain)
        return index

    # All exact sources are below 2*lo+1, hence outside A.
    for p in small:
        for first, step in ((2,2),(1,4)):
            if first == 1 and (mode == "ordinary" or p % 4 != 1):
                continue
            for e in range(first,cutoff+1,step):
                if not allowed(p,e,forbidden):
                    continue
                exact[p,e] = True
                factors = dict(archive_edges.get((p,e), ()))
                factors.update({q:max(k,factors.get(q,0))
                                for q,k in bounded_trial_factors(p,e).items() if disjoint(q)})
                for q,k in factors.items():
                    sources.setdefault(q, []).append((p,e,k))

    all_primes = sorted(set(small) | sources.keys())
    slots, slopes = {}, {}
    for p in all_primes:
        logp = log_bounds(p)[0]
        entries = by_prime.setdefault(p, [])
        for first, step in ((2,2),(1,4)):
            if first == 1 and (mode == "ordinary" or p % 4 != 1):
                continue
            for e in range(first,cutoff+1,step):
                if p <= limit and (p,e) in exact:
                    k, n = 0, e+1
                    if unit_price and p % root == 1:
                        while n % root == 0:
                            k += 1
                            n //= root
                    j = add(e*logp-k*unit_price,log_bounds(sigma(p,e),p**e)[1])
                    entries.append((j,e,False))
                    slots[p,e] = j
                    if first == 1:
                        special.append((j,SCALE))
            e = first
            if p <= limit:
                e += step*((cutoff-e)//step+1)
            while not allowed(p,e,forbidden):
                e += step
            k, threshold = 0, root
            cost = e*logp
            if unit_price and p % root == 1:
                while threshold <= e+1:
                    k += 1
                    threshold *= root
                cost -= k*unit_price
                slope = logp-(-(-unit_price//(threshold-1-e)))
                if slope < 0:
                    if (root-1)*threshold*logp < unit_price:
                        raise ValueError("tail growth beyond the second breakpoint")
                    cost = min(cost,(threshold-1)*logp-(k+1)*unit_price)
                    slope = 0
                slopes[p] = min(slopes.get(p,logp),slope)
            j = add(cost,log_bounds(p,p-1)[1])
            entries.append((j,e,True))
            tail_exp[j] = (p,e)
            if first == 1:
                special.append((j,SCALE))

    first_tail = limit+1
    tail_log = log_bounds(first_tail)[0]
    tail_gain = log_bounds(first_tail, first_tail-1)[1]
    cheapest_tail = 2*tail_log
    if unit_price:
        if (root-1)*root*tail_log < unit_price:
            raise ValueError("tail valuation unit may be underpriced")
        cheapest_tail = min(cheapest_tail,(root-1)*tail_log-unit_price)
        if cheapest_tail < 0:
            raise ValueError("tail must have nonnegative price")
    tail = add(cheapest_tail*SCALE//tail_gain,SCALE)
    if mode == "any":
        j = add(tail_log,tail_gain)
        special.append((j,SCALE))

    rows = [(list(enumerate(-h for h in gains)),0), (special,SCALE)]
    for p, entries in by_prime.items():
        terms = [(j,SCALE) for j,_,_ in entries]
        rows.append((terms,SCALE))
        if branch == p:
            rows.append(([(j,-a) for j,a in terms],-SCALE))
    free = [(tail,costs[tail])]
    for q, factors in sources.items():
        # Individual implications and simultaneous required valuations.
        demand = []
        for p,e,k in factors:
            j = slots[p,e]
            eligible = [(i,-SCALE) for i,f,is_tail in by_prime[q]
                        if (is_tail or f >= k) and not (e%2 and f%2)]
            rows.append(([(j,SCALE),*eligible],0))
            demand.append((j,k*SCALE))
        y = add(slopes.get(q,log_bounds(q)[0]),0)
        free.append((y,costs[y]))
        rows.append((demand+[(i,-e*SCALE) for i,e,_ in by_prime[q]]+[(y,-SCALE)],0))
        # Bound a tail option's missing exponent by the size restriction.
        lo_e = 0
        hi_e = (BOUND.bit_length()-1)//(q.bit_length()-1)+1
        while hi_e-lo_e>1:
            mid=(lo_e+hi_e)//2
            if q**mid <= BOUND:
                lo_e=mid
            else:
                hi_e=mid
        cap = lo_e
        rows.append(([(y,SCALE)]+[(i,-max(0,cap-e)*SCALE)
                     for i,e,is_tail in by_prime[q] if is_tail],0))
    prices = {}
    if mode == "ordinary" and unit == 1:
        for q, entries in by_prime.items():
            by_source = {}
            for p,e,k in sources.get(q, ()):
                by_source[p] = max(by_source.get(p,0),k)
            incoming = sum(by_source.values())
            tail_min = next(e for _,e,is_tail in entries if is_tail)
            prices[q] = tail_min, max(tail_min,incoming)
    return costs, rows, free, ms, (first_tail, prices)


def gain_for_m(root,m):
    A = sigma(root,m-1)
    gain = log_bounds(root,root-1)[1]
    rem, j = A, 1
    while rem >= 2*m*j+1:
        rem //= 2*m*j+1
        gain += log_bounds(2*m*j+1,2*m*j)[1]
        j += 1
    return gain


def check_dual(costs, rows, free, weights):
    if len(weights)!=len(rows) or any(type(w) is not int or w<0 for w in weights):
        raise ValueError("invalid dual")
    reduced = [v*DYADIC for v in costs]
    constant = 0
    for w,(ts,b) in zip(weights,rows):
        constant -= w*b
        for j,a in ts:
            reduced[j]+=w*a
    unbounded = {j for j,_ in free}
    if any(reduced[j]<0 for j in unbounded):
        raise ValueError("invalid unbounded reduced cost")
    return constant+sum(min(v,0) for j,v in enumerate(reduced) if j not in unbounded)


def make_certificate(p,lo,hi,mode,archive,branch=0,source_gain=0,unit=1,cutoff=CUTOFF):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    costs, rows, free, ms, _ = model(p,lo,hi,mode,archive,branch,unit,cutoff)
    # Pick a representative demand. The verifier substitutes each exact m.
    gain = max(gain_for_m(p,m) for m in ms)+source_gain
    rows[0]=(rows[0][0],gain-log_bounds(2)[0])
    ri,ci,vs,bs=[],[],[],[]
    for i,(ts,b) in enumerate(rows):
        bs.append(b/SCALE)
        for j,a in ts:
            ri.append(i)
            ci.append(j)
            vs.append(a/SCALE)
    unbounded={i for i,_ in free}
    M=coo_matrix((vs,(ri,ci)),shape=(len(rows),len(costs))).tocsr()
    result=linprog([c/SCALE for c in costs], A_ub=M,b_ub=bs,
                   bounds=[(0,None if i in unbounded else 1) for i in range(len(costs))],
                   method="highs", options={"time_limit": 25})
    if not result.success:
        raise RuntimeError(result.message)
    weights=[max(0,round(-x*DYADIC)) for x in result.ineqlin.marginals]
    # A one-unit rounding error on an unbounded column must not produce a proof.
    uses={j: [] for j,_ in free}
    for i,(ts,_) in enumerate(rows):
        for col,a in ts:
            if col in uses:
                uses[col].append((i,a))
    for j,involved in uses.items():
        reduced=costs[j]*DYADIC+sum(a*weights[i] for i,a in involved)
        if reduced < 0:
            i,a=next((i,a) for i,a in involved if a<0)
            weights[i] -= (-reduced-a-1)//-a
    check_dual(costs,rows,free,weights)
    return dict(root=p,lo=lo,hi=hi,mode=mode,branch=branch,unit=unit,cutoff=cutoff,weights=weights)


def replay(cert,archive,source_gain=0,return_prices=False):
    p,lo,hi,mode,branch,weights=(cert[k] for k in ("root","lo","hi","mode","branch","weights"))
    unit = cert.get("unit",1)
    cutoff = cert.get("cutoff",CUTOFF)
    costs, rows, free, ms, prices = model(p,lo,hi,mode,archive,branch,unit,cutoff)
    bound = check_dual(costs,rows,free,weights)
    result = {m:bound+weights[0]*(log_bounds(2)[0]-gain_for_m(p,m)-source_gain) for m in ms}
    return (result,prices) if return_prices else result

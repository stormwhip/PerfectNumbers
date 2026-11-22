#!/usr/bin/env python3
"""Exact subset-DP screening of root orders by immediate sigma conflicts.

This is a combinatorial first-level proxy, NOT an empirical runtime guarantee.
Optionally use the exact one-second exponent-19 census as weights.
"""
import argparse
from functools import lru_cache
import math
import re
from pathlib import Path

ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
LOG_BOUND = 2400 * math.log(10)
ORIGINAL = tuple(ROOTS)
SHARD_RESULT = re.compile(r"SHARD_CENSUS_RESULT root=19 index=(\d+) exponent=(\d+) exact=(\d) status=(\w+)")

def prime_list(n):
    sieve = bytearray(b"\x01") * (n+1)
    sieve[:2] = b"\x00\x00"
    for p in range(2,math.isqrt(n)+1):
        if sieve[p]:
            sieve[p*p::p] = b"\x00" * (((n-p*p)//p)+1)
    return [i for i in range(2,n+1) if sieve[i]]

SMALL_PRIMES = prime_list(6000)

def root_options(p):
    opts=[]
    lp=math.log(p)
    if p%4==1 and lp<=LOG_BOUND:
        opts.append(1)
    if p==3:
        opts.extend(a for a in (2,4,8,14,24) if a*lp<=LOG_BOUND)
        start=7
    elif p==7:
        opts.extend(a for a in (2,8) if a*lp<=LOG_BOUND)
        start=5
    else:
        start=3
    for q in SMALL_PRIMES:
        if q<start: continue
        a=q-1
        if a*lp>LOG_BOUND: break
        opts.append(a)
    return tuple(opts)

def sigma_divisor(p,a,q):
    residue=p%q
    if residue==0:return False
    if residue==1:return (a+1)%q==0
    return pow(residue,a+1,q)==1

def census_weights(path):
    if not path: return {}
    records=SHARD_RESULT.findall(Path(path).read_text(encoding="utf-8"))
    if len(records)!=len(root_options(19)):
        raise RuntimeError(f"Incomplete empirical corpus: {len(records)} records, {len(root_options(19))} model options")
    weights={}
    for idx,a,exact,status in records:
        idx=int(idx)
        if root_options(19)[idx]!=int(a):
            raise RuntimeError("Empirical and generated exponent classes disagree")
        weights[int(a)]=30.0 if status=="TIMEOUT" else 0.1
    return weights

def solve(weight_mode,hard_weights):
    n=len(ROOTS); full=(1<<n)-1
    lookup={}
    for p in ROOTS:
        lookup[p]=[
            (a,sum(1<<j for j,q in enumerate(ROOTS)
                    if q!=p and sigma_divisor(p,a,q)))
            for a in root_options(p)
        ]
    option_count=sum(len(x) for x in lookup.values())
    @lru_cache(None)
    def cost(mask,i):
        p=ROOTS[i]
        result=0.0
        for a,conflicts in lookup[p]:
            if conflicts&mask: continue
            if weight_mode=="count": weight=1.0
            elif weight_mode=="sqrt": weight=1.0/math.sqrt(a+1)
            elif weight_mode=="inverse": weight=1.0/(a+1)
            elif weight_mode=="empirical":
                weight=hard_weights.get(a,0.1) if p==19 else 5.0/math.sqrt(a+1)
            else: raise ValueError(weight_mode)
            result+=weight
        return result
    @lru_cache(None)
    def dp(mask):
        if mask==full:return (0.0,())
        choices=[]
        for i,p in enumerate(ROOTS):
            if mask>>i&1: continue
            future,order=dp(mask|(1<<i))
            choices.append((cost(mask,i)+future,(p,)+order))
        return min(choices)
    original_cost=0.0
    mask=0
    for p in ORIGINAL:
        i=ROOTS.index(p)
        original_cost+=cost(mask,i)
        mask|=(1<<i)
    optimal_score,optimal_order=dp(0)
    print(f"DP_RESULT objective={weight_mode} options={option_count} "
          f"transitions={n*(1<<(n-1))} original={original_cost:.10f} "
          f"optimum={optimal_score:.10f} ratio={optimal_score/original_cost:.6f} "
          f"order={','.join(map(str,optimal_order))}",flush=True)
    return optimal_score,optimal_order

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--census",default=None)
    args=parser.parse_args()
    hard=census_weights(args.census)
    for mode in ("count","sqrt","inverse"):
        solve(mode,hard)
    if hard:solve("empirical",hard)

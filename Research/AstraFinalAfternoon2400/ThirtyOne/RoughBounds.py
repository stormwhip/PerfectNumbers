"""Exact low-divisor tests for six anonymous primitive cyclotomic blocks."""
import argparse,json,sys
from math import gcd,isqrt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import sigma, prime_small


def run(limit):
 for p,e,removed in [(31,456,3229),(31,466,3229),(31,268,3229),(3229,102,1),(3229,156,1),(3229,210,1)]:
  # Remove only when needed; 3229 is not a divisor in the first two rows.
  ell=e+1;assert prime_small(ell) and p%ell!=1
  A=sigma(p,e)
  if (p,e)==(31,268):assert A%removed==0;A//=removed
  assert A%(2*ell)==1
  # Every prime divisor q = 1 mod 2ell. Test the entire AP, including composites.
  # For q in [3,limit], a prime factor cannot be discarded except by residue.
  hits=[q for q in range(2*ell+1,limit+1,2*ell) if A%q==0]
  print(json.dumps(dict(p=p,e=e,tested=(limit-1)//(2*ell),limit=limit,hits=hits,
                       nonsquare=isqrt(A)**2!=A,composite_fermat=pow(2,A-1,A)!=1,bits=A.bit_length())))

if __name__=='__main__':
 assert __debug__;a=argparse.ArgumentParser();a.add_argument('--limit',type=int,default=10**8);run(a.parse_args().limit)

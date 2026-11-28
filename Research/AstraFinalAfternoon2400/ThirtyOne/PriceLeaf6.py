"""One exact first-72 residual with fixed Euler: weight-two target pricing."""
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from GenericPrice import T,Q,Z,W,domain,one
from Joint6 import run as verify_joint
from Replay import state, valuation

from functools import cache

A=((31,6),(T,72),(Q,2),(Z,4),(1360496847191,6),(W,16),(3,2),(13,2),(61,1))
J=((31,6),(T,72),(Q,16))

@cache
def allowed(row):
    assert __debug__ and row==A and state(row)[-1] and sum(h%2 for q,h in row)==1
    assert dict(row)[T]-valuation(state(row)[1],T)==71
    # L<=8000<T: no order-one length and no LTE length increment.
    assert T>8000
    assert min(domain(T))==3 and T not in domain(T)
    windows,n=one(row,T,Fraction(2))
    assert windows==[] and n==0
    return True

@cache
def joint(row):
    assert __debug__ and row==J and state(row)[-1] and all(h%2==0 for _,h in row)
    r=verify_joint(row,Fraction(3,2))
    assert r==dict(weight='3/2',loss_counts=[0,0,0],inside=[],outside=[]),r
    return True

if __name__=='__main__':
    print('exact fixed-Euler price terminal passed:',allowed(A),flush=True)
    print('exact separate joint price terminal passed:',joint(J),flush=True)

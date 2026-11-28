"""Under squarefreeness Phi_809(7) must have at least three distinct prime factors."""
from math import gcd
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyLattice import A, L, run
from VerifyFactorCount import allowances, X, B, E


def verify():
    assert __debug__
    assert A%809 and all(809%j for j in range(2,29)) and gcd(A,42)==1 and pow(2,A-1,A)!=1
    assert pow(A,3,7)==1 and pow(A,3,49)!=1
    run(227,1)
    allowances()
    U=579125
    # If A has at most two distinct factors, internal nonlinear/ordinary
    # supply <=5+230 even with an Euler inside A. Squarefree A gets fully paid
    # at least twice per prime, except in the separate linear-inside case.
    cap=235
    assert X*A*A*7**(2*(E-cap))>B*U
    for s in range(E+1):
        q=max(5,2*7**s-1)
        assert X*A*A*q*7**(2*max(0,E-cap-s))>B*U
    # Two independently valid N bounds, multiplied only to obtain N^2:
    # ordinary pricing on all ordinary atoms and mass+external pricing.
    left=X*7**(2*E)
    right=X*A*A*7**(2*(E-230))
    assert left*right>(B*U)**2
    print('PASS (7,808): if A is squarefree, at least three distinct primes are mandatory, all Euler cases')

if __name__=='__main__':verify()

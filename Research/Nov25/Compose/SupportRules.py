"""Portable support/exponent restrictions for root 13 and the index-11 seed."""
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Compose import sigma,valuation,permitted,euler,need,pc,ORDER

SEED=(13,10)
CORE=(23,419,859,18041)
PRIOR=ORDER[:ORDER.index(13)]


def min_abundancy(root,e,lower,absent=(),fixed=()):
    """Necessary lower bound: exact fixed and at least the given other powers."""
    need(root not in lower and root not in dict(fixed),'duplicate root support')
    need(not set(lower)&dict(fixed).keys(),'duplicate fixed/lower support')
    bad=PRIOR+tuple(absent)
    k=sum(f%2 for q,f in fixed)
    modes=[0]+([q for q in lower if euler(q,bad)] if not k else [])
    A=sigma(root,e)
    need(all(pc.prime64(q) for q in (*lower,*dict(fixed))),'nonprime payment')
    vals=[]
    for z in modes:
        fdict=dict(fixed)
        for q,l in lower.items():
            sp=(q==z);f=l+((1-l)%4 if sp else l%2)
            while not permitted(q,f,bad):f+=4 if sp else 2
            fdict[q]=f
        x=Fraction(A,root**e)
        for q,f in fdict.items():x*=Fraction(sigma(q,f),q**f)
        vals.append(x)
    return min(vals)


def rules(e=10):
    """The rules lift to all even E>=10 with 11|(E+1), not necessarily exact E=10."""
    p,seed=SEED
    need(type(e)==int and e>=seed and e%2==0 and (e+1)%11==0,'wrong index class')
    A=sigma(p,seed)
    need(A==23*419*859*18041 and all(pc.prime64(q) for q in CORE),'seed factors')
    h={q:valuation(A,q) for q in CORE}
    # Every exponent considered for another prime uses ordinary/Euler shape
    # and first-root exclusions. The actual root exponent E is used only
    # through H(13,E)>=H(13,10) and sigma(13^10)|sigma(13^E).
    all_three=min_abundancy(p,seed,{**h,3:1,5:1,17:1})
    five_ge2=min_abundancy(p,seed,{**h,3:1,5:2})
    three_ge3=min_abundancy(p,seed,{**h,3:3},fixed=((5,1),))
    need(min(all_three,five_ge2,three_ge3)>2,'support restriction fails')
    # If 3 and 5 both occur, v5=1 and v3=2. 5 is then Euler and 17 is absent.
    # Existing sigma from 5^1 pays one of the 3 units, and 3^2 pays one root 13 unit.
    return tuple(a.numerator*10**6//a.denominator for a in (all_three,five_ge2,three_ge3))


if __name__=='__main__':
    for e in map(int,sys.argv[1:] or (10,)):
        print('CONDITIONAL ONLY',(13,e),'abundancy ppm',rules(e),flush=True)

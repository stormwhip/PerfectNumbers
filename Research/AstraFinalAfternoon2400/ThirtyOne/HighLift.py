"""Coverage-complete loss table using all positive lifts; refuses over-budget scans."""
from functools import cache
from itertools import product
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import odd_lifts,roots,max_positive_base,prime_small


@cache
def high_labels(s, o, z, a, b, h, base_cap=None, max_count=1000000):
    """Verify every odd y≥3 with ord_s(y)=o, s^z|y^o−1, y^(bh)<s^(az)."""
    assert prime_small(s) and s%2 and o>1 and (s-1)%o==0
    assert z>=1 and a>=1 and b>=1 and h>=1 and max_count>=0
    modulus, rr=roots(s,o,z)[-1]
    assert modulus==s**z
    upper=max_positive_base(modulus**a,b*h)
    if base_cap is not None:
        assert type(base_cap) is int and base_cap>=0
        upper=min(upper,base_cap)
    aps=tuple(odd_lifts(r,modulus,upper) for r in rr)
    # Count with unbounded integers: len(range) can overflow on a large domain.
    n=sum(max(0,(x.stop-1-x.start)//x.step+1) for x in aps)
    if n>max_count:
        raise OverflowError(f'{n} admissible odd lifts exceed replay cap {max_count}; NO EXCLUSION')
    result=tuple(sorted(y for x in aps for y in x))
    assert len(result)==len(set(result))==n
    assert all(3<=y<=upper and y%2 and pow(y,o,modulus)==1 and y**(b*h)<modulus**a for y in result)
    return result


def regression():
    r=high_labels(19,3,1,6,1,2)
    direct=tuple(y for y in range(3,19**3,2) if pow(y,3,19)==1 and y%19!=1)
    assert r==direct and 83 in r and 11 in r
    for (s,o,z),(a,b,h) in product(((7,3,2),(19,9,2),(31,5,2)),((2,1,2),(3,2,2),(6,1,2),(6,1,4))):
        cap=5000;m=s**z
        expected=tuple(y for y in range(3,cap+1,2) if y**(b*h)<m**a and pow(y,o,m)==1 and all(pow(y,d,s)!=1 for d in range(1,o) if o%d==0))
        assert high_labels(s,o,z,a,b,h,cap)==expected
    try:
        high_labels(19,3,10,6,1,2,max_count=1000)
    except OverflowError:
        return dict(weight6_order3_depth1=len(r), greater_than_modulus=sum(y>19 for y in r),
                    r83=83, tiny_bruteforce_comparisons=12, overflow_rejected=True)
    raise AssertionError('overlarge input accepted')


if __name__=='__main__':
    assert __debug__
    print(json.dumps(regression(),sort_keys=True))

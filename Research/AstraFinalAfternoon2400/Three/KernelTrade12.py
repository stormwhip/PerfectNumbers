"""Independent strict root-twelve tradeoff using replayed finite square-kernel checks."""
from Prices import *
from CleanPrice import price2
from Explore import CASES
from Emitters import certificate
from pathlib import Path
from subprocess import run
from sys import argv


def proof(exe):
    assert __debug__
    r=run([str(Path(exe).resolve()),'398581','109','120000000000'],check=True,text=True,capture_output=True)
    assert r.stdout.strip()=='PASS 398581 109 120000000000 2'
    rows=CASES['12-1-108'];R,F0,odd,X,S,D,spec=certificate(rows);p=398581
    assert odd==1 and sig(3,12)==797161 and sig(797161,1)==2*p
    assert spec==[(p,109,D)] and D==sig(p,108) and F0[p]-vp(S,p)==107
    V,E=price2(rows,p);assert len(E)==1
    K=120000000001
    # If b supplies from D then the mass on D support (all ordinary) is
    # >=D·sf(D) >=D*K. The outside ordinary supplier bound is independent.
    assert V*D*K>B*p**4
    assert V*D*K<=B*p**6  # merely the limit of this specific inequality
    print('PASS fixed Euler 3^12·797161·398581^108: at least three internal Q-supply units',flush=True)
if __name__=='__main__':proof(argv[1])

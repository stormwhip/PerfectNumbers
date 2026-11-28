"""Pinned, standard-library-only high Euler supply supplement (all-signed and subgroup domains)."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from ThinGeneral import verify,require

PROFILE={
 '618s534':(618,534,5000,[(8,3,1,52360,2909,320,5),(10,5,9,52360,2380,224,5)]),
 '612s536':(612,536,120000,[(8,3,139,834829,46372,5421,67),(10,5,27,834829,37946,3647,36)]),
 '618s533':(618,533,120000,[(8,3,85,1723551,95749,11090,137),(10,5,139,1723551,78337,7377,85)]),
}

if __name__=='__main__':
    opts=sys.argv[1:] or ['618s534'];require(all(q in PROFILE for q in opts) and len(set(opts))==len(opts),'profile options')
    for key in opts:
        e,s,cap,ans=PROFILE[key];rows=[]
        require(verify(e,s,cap,rows) and rows==ans,('profile mismatch',key,rows))
        print('PASS pinned exact high Euler window',key,flush=True)

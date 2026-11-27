"""One canonical exact key, verifying old exact forest cover and all new complements."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R/'Night2400')];from VerifyFibers import verify
import Verify16
from Verify22 import check
from VerifyDeep import deep
assert __debug__;old=verify(R/'Night2400/Fibers31x16.json.gz');assert old['key']==[31,16] and int(old['pivot'])==751670559138758105956097 and old['open']==[16,22] and len(old['domain'])==16 and len(old['covered'])==14
assert check()=={2:[16,17,18,19,20]};assert not deep();print('FULL checked canonical exact 31^16: 14 historical + firsts 16 and 22. P31_I00005.',flush=True)

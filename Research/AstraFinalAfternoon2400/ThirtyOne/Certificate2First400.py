"""Strict one-first arithmetic certificate for v331=400 at canonical (31,2)."""
from hashlib import sha256
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import key, ledger
from PricedTwo import check

if __name__=='__main__':
    assert __debug__;ledger()
    t,domain,tail=key(2)
    assert t==331 and tail==952 and len(domain)==143 and ((31,2),(331,400)) in domain
    r=check(400)
    assert r==dict(first=400,loss_labels=1,U_digits=2,summary=[(1,0,1200),(5,0,1200)],residual=[]),r
    print(json.dumps(dict(key=[31,2],pivot=331,first_closed=[400],total_allocations=2400,
                         all_other_firsts='unchanged',residual_digest=sha256(b'[]').hexdigest())),flush=True)

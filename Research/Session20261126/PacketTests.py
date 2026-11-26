"""Negative checks on certificate scope. No discovery dependencies."""
import gzip, json, sys
from pathlib import Path
from tempfile import TemporaryDirectory
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import PivotCheck

def rejected(data,path):
    path.write_bytes(gzip.compress(json.dumps(data).encode()))
    try:PivotCheck.verify(path)
    except (AssertionError, ValueError, KeyError):return
    raise AssertionError('invalid certificate accepted')

if __name__=='__main__':
    if not __debug__:raise RuntimeError('assertions required')
    raw=(H/'Pivot11x408.json.gz').read_bytes()
    with TemporaryDirectory() as t:
        path=Path(t)/'Broken.json.gz'
        # Lose the very first required legal case, not an impossible exponent.
        d=json.loads(gzip.decompress(raw));del d['cases'][min(d['cases'],key=int)];rejected(d,path)
        # Forged pivot need not even divide the primary geometric sum.
        d=json.loads(gzip.decompress(raw));d['q']=121;rejected(d,path)
        # Replace one bound by a forest that pays no implicit labels.
        d=json.loads(gzip.decompress(raw));first=min(d['cases'],key=int);d['cases'][first]=dict(roots=[],owners=[],head=1);rejected(d,path)
    print('PASS: dropped branch, composite pivot, unsupported minimum')

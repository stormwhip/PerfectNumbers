"""Fail-closed replay jobs, worker-importable under Windows spawn."""
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent


def verify_job(name):
    sys.path.insert(0,str(HERE))
    if name=='five148':
        from Five.Verify148 import verify
        result=verify()
    elif name=='five520':
        from Five.Verify520 import verify
        result=verify()
    elif name.startswith('Seven/') and name.endswith('.pack.json.gz') and name.count('/')==1:
        from Seven.Verify import verify
        result=verify(HERE/name)
    elif name.endswith('.json.gz') and Path(name).name==name:
        from ForestPackets import verify
        result=verify(HERE/'Forests'/name)
    else:
        raise ValueError(f'unknown proof job {name}')
    return name,result

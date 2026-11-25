"""Fail-closed replay jobs, worker-importable under Windows spawn."""
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent


def verify_job(name):
    sys.path.insert(0,str(HERE))
    if name=='five148':
        from five.Verify148 import verify
        result=verify()
    elif name=='five520':
        from five.Verify520 import verify
        result=verify()
    elif name.endswith('.json.gz') and Path(name).name==name:
        from ForestPackets import verify
        result=verify(HERE/'Forests'/name)
    else:
        raise ValueError(f'unknown proof job {name}')
    return name,result

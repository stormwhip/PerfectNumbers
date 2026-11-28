"""Full f12 exact 2477-fiber; no prior f12 reductions needed."""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from VerifyNested import main
if __name__=='__main__':
    assert __debug__;pack=json.loads((P/'Nested12.json').read_bytes());assert set(pack['cases'])=={'12'};main(pack)

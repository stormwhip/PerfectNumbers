"""Stock Python exact f10 first-pivot closure."""
import sys,json
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from VerifyNested import main
if __name__=='__main__':
    assert __debug__;pack=json.loads((P/'SmallTen.json').read_bytes());assert set(pack['cases'])=={'10'};main(pack)

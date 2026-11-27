"""Replay complete f8 tree under exact 19^618."""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from VerifyNested import main
if __name__=='__main__':
    assert __debug__;D=json.loads((P/'Solved8.json').read_bytes());assert set(D['cases'])=={'8'};main(D)

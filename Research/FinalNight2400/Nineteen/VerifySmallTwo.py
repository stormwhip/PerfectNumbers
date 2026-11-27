"""Verify the final f=2 first-pivot fiber. Compact equivalent integer log routine."""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from FastKernel import Kernel;import VerifyNested as N
if __name__=='__main__':
    assert __debug__;sys.set_int_max_str_digits(0);D=json.loads((P/'Solved2.json').read_bytes());assert set(D['cases'])=={'2'};N.Kernel=Kernel;N.main(D)

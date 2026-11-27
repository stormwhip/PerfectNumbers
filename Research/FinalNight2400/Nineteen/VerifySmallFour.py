"""Optional strong lattice kernel for the complete f4 exact tree."""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import VerifyNested as N;from BestKernel import Kernel
if __name__=='__main__':
    assert __debug__;sys.set_int_max_str_digits(0);D=json.loads((P/'Solved4.json').read_bytes());assert set(D['cases'])=={'4'};N.Kernel=Kernel;N.main(D)
"""Both certified cofactor caps applied to the identical nested 618 leaf test."""
import sys
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import AnchorKernel as A,VerifyLattice as S,VerifySquareLattice as T
class Kernel(A.Kernel):
    def __init__(self):
        super().__init__();self.cut=S.run();A.C.U0=T.run()

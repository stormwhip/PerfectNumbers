"""Combine previously verified 7,906 square/linear cap and price for high Euler or s=0, no squarefreeness assumed."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Gain906 as V;import Repeated906 as C;C.run(160)
A=V.A;B=V.B;X=V.X;U=V.U;assert A**3%49!=1
# If omega(A)<=3, select one ordinary-or-Euler A prime with u<=5; zero-pad absent labels. Two other A-prime supplies are in [0,258].
# For a high label u>=164, there is no repeated r in A, and its ordinary (or high Euler) actual exponent >=2. Hence a whole additional r>10^7*7^(u-4) beyond A is a legitimate factor independent of off-A pricing.
C0=10**7;limits=[]
for h in range(3):
 # Worst mass occurs at largest possible u on each category: rise by one costs at most 7 in the extra-r bound and saves 49 in outside supply cost. Select h high (u=258), 2-h low (u=163).
 us=[258]*h+[163]*(2-h);N0=X*A*7**(2*(906-5-sum(us)))*C0**h*7**(254*h)
 assert N0>B*U;limits.append(len(str(N0//U))-1)
print('PASS high Euler or linear zero supply implies at least FOUR distinct factors of A independent of multiplicities. Worst floors, by 0/1/2 other high supplier labels:',limits)

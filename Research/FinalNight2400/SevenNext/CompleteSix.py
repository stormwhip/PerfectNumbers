"""Union and replay of all exact S valuations under T^6. No initial proof is assumed for these 14 cases."""
from pathlib import Path
import sys,runpy
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import VerifyTertiary as A, VerifyFour as F, VerifyNative as N
from math import prod

def main():
 assert __debug__;rows=[(7,12),(A.Q,12),(A.T,6)];s=A.C.State(rows);S=A.S6;c=A.C.valuation(s.D,S);assert c==1
 allj=[];j=c
 while s.base//S**c*S**j<=A.B:
  if s.possible(S,j,c):
   u=A.C.State(rows+[(S,j)])
   if not u.conflict and u.base<=A.B and prod(A.C.sigma(p,h) for p,h in u.rows.items())<=2*u.X:allj.append(j)
  j+=1
 assert j==42 and allj==[1,2,4,5,6,8,9,10,12,13,14,16,18,20]
 A.main();F.main();runpy.run_path(str(H/'Abundance.py'),run_name='__main__');N.run('Native.json.gz',[8,12]);N.run('FinalSix.json.gz',[2,6,10]);assert set(allj)==set(A.EXPECTED[6])|{4}|{k for k in allj if k%2}|{8,12}|{2,6,10}
 print('PASS FULL T^6: all 14 exact S powers and entire size tail excluded. No root-key closure.',flush=True)
if __name__=='__main__':main()

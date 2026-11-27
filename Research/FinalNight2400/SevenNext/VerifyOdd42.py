"""New complete remaining exact odd 173 assignments under 7^12 Q^42."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from Odd42 import *
@cache
def net_credit(r):
 h=2;z=r*r;ear=None
 while z<=B:
  S=(r*z-1)//(r-1);credit=Fraction(z,Q**(2*val(S,Q))*R**(38*val(S,R)));ear=credit if ear is None else min(ear,credit);z*=r*r;h+=2
 return ear
CRED={21:[3,23,29,43,1013,6392783],25:[3,29,43,79,157,70981],29:[3,11,13,29,31,43,109,131,9431,30103,95531,618041,2361617911],33:[3,29,43,443,1123,202777],37:[3,29,43,1597,4637,597551],41:[3,13,29,43,109,211,631,1051,25537,30103,3144079,8576317]}
def main():
 assert __debug__ and C.pc.prime64(Q) and C.pc.prime64(R) and C.sigma(7,12)==Q and R%4==1 and R-1==4*43 and Q>5100 and (Q-1)%R!=0
 for h,fs in CRED.items():
  z=C.State([(7,12),(Q,42),(R,h)]);assert h%4==1 and z.fixed_euler and not z.conflict
  assert len(set(fs))==len(fs) and all(C.pc.prime64(r) and r not in z.rows and z.D%r==0 for r in fs)
  j=h-val(z.S,R);c=42-val(z.S,Q);assert 0<=j<=41 and 0<c<=42;U=cost(Q,c,2,True)*cost(R,j,38,True);G=prod((net_credit(r) for r in fs),start=Fraction(1));N=z.X*G*Q**(2*c)*R**(38*j)/U;assert N>B;print('Q^42, 173^',h,'bits above B at least',N.numerator.bit_length()-N.denominator.bit_length()-B.bit_length()-1,flush=True)
if __name__=='__main__':main()

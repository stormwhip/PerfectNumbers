"""Revalidate only the historical 19,618 partition and its registered high-Euler repair."""
from pathlib import Path
import sys,runpy,hashlib
P=Path(__file__).resolve().parent;G=P.parents[1]/'GeminiFrontier'
def main():
    assert __debug__;src=G/'SubmittedVerify.py';assert hashlib.sha256(src.read_bytes()).hexdigest()=='39657ee6eafdd632f800597247b587a0f7d236fe8e8258723ca8cd0676c07469';V=runpy.run_path(str(src));t=2477;p=19;e=618;B=10**2400
    V['verify_prime'](t);V['verify_19_618_independent']();state,sig,odd,val=(V[k] for k in ('state_eval','sigma','odd','val'))
    for f in range(70,122,2):
        X,S,D=state({p:e,t:f},set());A=odd(sig(p,e))//t;C=odd(sig(t,f));C//=p**val(C,p);assert D==A*C;Q=2*t**(f-val(S,t))-1
        assert V['prove_q_not_dividing_block'](C,Q,2*(Q+1)) and X*C*Q**5>B
    X,S,D=state({p:e},set());live={f for f in range(1,243) if state({p:e,t:f},set()) is not None};assert live=={1,*range(2,121,2),*range(5,122,4)}
    assert X*(D//t)*t**242<=B<X*(D//t)*t**243
    covered={*range(5,122,4),*range(70,122,2)};assert len(live)==91 and len(covered)==56 and live-covered=={1,*range(2,69,2)}
    print('PASS historical 56/91 live excluded, canonical even 122..242 direct, size tail 243, residual 35',flush=True)
if __name__=='__main__':main()

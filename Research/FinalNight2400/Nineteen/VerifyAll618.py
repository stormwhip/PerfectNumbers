"""Standalone aggregate serial replay of the full (19,618) precision partition."""
from pathlib import Path
import sys,subprocess,time
P=Path(__file__).resolve().parent
# Each verifier checks the fixed exact values it covers internally (and fails on missing subtrees).
STAGES=[('VerifyHistory.py',{*range(5,122,4),*range(70,122,2)}),('Verify618.py',set(range(48,69,2))),('Verify618Square.py',set(range(36,47,2))),('Verify618Credit.py',{26,30,32,34}),('Verify618Factored.py',{22,24,28}),('VerifyOne.py',{1}),('VerifyAnchor.py',{18,20}),('VerifyAnchorMore.py',{16}),('VerifyNested.py',{14}),('VerifyTwelve.py',{12}),('VerifySmallTen.py',{10}),('VerifySmallEight.py',{8}),('VerifySmallSix.py',{6}),('VerifySmallFour.py',{4}),('VerifySmallTwo.py',{2})]
if __name__=='__main__':
    assert __debug__;covered=set();started=time.monotonic()
    for name,claims in STAGES:
        assert not covered&claims
        subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(P/name)],check=True);covered|=claims;print('STAGE',name,'ok; covered',len(covered),flush=True)
    assert covered=={1,*range(2,121,2),*range(5,122,4)} and len(covered)==91
    print('FULL KEY (19,618): all 91 live assignments excluded, direct checks and entire infinite size tail replayed. seconds',round(time.monotonic()-started,3),flush=True)

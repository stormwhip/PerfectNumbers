"""Full exact 19,282 key from both historical first-pivot reports and complete f10."""
from pathlib import Path
import json,subprocess,sys,time
P=Path(__file__).resolve().parent;N=P.parents[1]/'Night2400'
def replay(script,*args):
    subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(script),*map(str,args)],check=True)
if __name__=='__main__':
    assert __debug__;start=time.monotonic();sys.path.insert(0,str(N));import VerifyFibers as V
    H=[]
    for f in [N/'Fibers19x282.json.gz',N/'F4/Fibers19x282.json.gz']:
        d=V.verify(f);assert d['key']==[19,282] and d['pivot']=='1735317810514627' and d['first_out_of_size']==112 and d['domain']==list(range(2,55,2));H.append(set(d['covered']));print('Historical first-pivot covered',sorted(H[-1]),flush=True)
    assert not H[0]&H[1] and set.union(*H)==set(range(2,55,2))-{10}
    # Each group below consists of whole r-exponents; r28 requires three complementary packets.
    groups=[([20,32,34,38,44,46,48,50,54,56,62,64,68,74,76,80,84,86,90,92,94,96,98,100],['Verify282.py']),([28],['VerifyInner.py','VerifyInnerOne.py','VerifyInnerFour.py']),([82,88],['VerifyHigh.py']),([66,70,78],['VerifyHighThree.py']),([14,16],['VerifyLowPair.py']),([2,8,26],['VerifyAbundance.py']),([10,30,72],['VerifyMidThree.py']),([58],['VerifyMasked58.py']),([18,60],['VerifyMaskedMore.py']),([24],['VerifyMasked24.py']),([6,36,40,42,52],['VerifyFiveMore.py']),([4],['VerifyFourth.py']),([12],['VerifyTwelfth282.py']),([22],['VerifyR22Full.py'])]
    matched=set()
    for cases,scripts in groups:
        assert not matched&set(cases)
        for s in scripts:replay(P/s)
        matched|=set(cases);print('complete r-values',len(matched),'of 50',flush=True)
    assert matched==set(range(2,101,2));print('FULL KEY (19,282): all 27 first-pivot values and strict tail; all 50 second pivot values under first 10. seconds',round(time.monotonic()-start,3),flush=True)

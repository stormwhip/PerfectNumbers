"""Fixed closed-world admission adapter for the canonical (31,10); NO credit with any open leaf."""
from pathlib import Path
import hashlib,gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Transfer import check
sys.path.insert(0,str(H.parent/'Nov25/Compose'));from Replay import proof

def verify():
    # The remaining 3,5 both absent branch, with prior 7 absent, is exactly a subdomain of ThreeAvoid. Recheck its verifier, not the historical summary.
    import subprocess
    subprocess.run([sys.executable,'-I','-S','-B',str(H.parent/'NightUniform/ThreeHittingWitness.py'),str(H.parent/'NightUniform/ThreeAvoid.json')],check=True)
    q=150332843;check(31,[19,7,11],(23,397,617,q),[('absent',[13]),('absent',[17,29,37]),('exact1',[5])]);
    for name,A,yes,no in [('Both31',[[31,10],[5,1]],[3,5],[13,17,29,37]),('Full31',[[31,10]],[5],[3,13,17]),('Support513',[[31,10]],[5,13],[3]),('Support517',[[31,10]],[5,17],[3,13])]:
        u=json.loads(gzip.decompress((H/(name+'.json.gz')).read_bytes()));assert (u['assigned'],u['present'],u['absent'])==(A,yes,no);print('conditional',name,proof(u,conditional=True),flush=True)
    from RefinedOnly3 import SPLITS,data
    x=data(H/'Refined31.json.gz');assert x['exceptions']==[];bank=x['ecpp'];seen=0
    def convert(t,path):
        nonlocal seen
        z,cut,*_=SPLITS[path];assert (t['q'],t['cut'])==(z,cut);cells={}
        for k,a in t['cells'].items():
            k0=int(k);assert str(k0)==k;cells[k]=convert(a,path+(k0,)) if path+(k0,) in SPLITS else a
            if path+(k0,) not in SPLITS:assert a['kind'] in ('forest','direct');seen+=1
        assert t['tail']['kind']=='forest';seen+=1
        return dict(kind='exp',q=z,cut=cut,cells=cells,tail=t['tail'])
    u=dict(assigned=[[31,10]],present=[3],absent=[5],leaf=convert(x['tree'],()),ecpp=bank);print('remaining',proof(u,conditional=True));print('COMPLETE',31,10,'last subdomain',seen,'leaves')
if __name__=='__main__':
    if not __debug__:raise SystemExit('reject optimized mode')
    verify()

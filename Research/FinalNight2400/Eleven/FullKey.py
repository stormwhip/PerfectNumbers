"""Scoped complete-key replay for (11,462); no other ledger key is certified."""
import gzip,hashlib,json,sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[2];N=R/'Research'/'Night2400'
def run(path,*args):
    cmd=[sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(path),*map(str,args)]
    print('replay',path.name,*[Path(s).name for s in args],flush=True);subprocess.run(cmd,cwd=R,check=True)
if __name__=='__main__':
    assert __debug__
    packet=N/'Fibers11x462.json.gz';b=packet.read_bytes();assert hashlib.sha256(b).hexdigest()=='2e58bd6b8142157eb3b1972f600863ffe194264f5310f89b099e2919f6196c65'
    hist=json.loads(gzip.decompress(b));assert (hist['p'],hist['e'],hist['pivot'])==(11,462,879701)
    historical=set(map(int,hist['cases']));new={1,4,6,22,36,42,46,70,72};assert len(historical)==49 and not historical&new
    run(N/'FrontierTree.py',packet);run(N/'Receipts'/'FiberPartition.py',packet)
    # Rebuild full first domain plus strict raw tail. Only canonical absent 7,19.
    d=R/'Research'/'Session20261126';sys.path.insert(0,str(d));from PivotCheck import C,B
    p,t=11,879701;base=C.State([(p,462)]);v=C.valuation(base.D,t);assert v==1
    k=v;allfirst=set()
    while base.base//(t**v)*t**k<=B:
        if base.possible(t,k,v):
            child=C.State([(p,462),(t,k)])
            if not child.conflict and child.base<=B and C.sigma(p,462)*C.sigma(t,k)<=2*child.X:allfirst.add(k)
        k+=1
    assert k==243 and allfirst==historical|new
    run(H.parent/'Fifth'/'Verify.py','70','72');run(H/'One.py');run(H/'FortySix.py');run(H/'FortyTwo.py');run(H/'Six42.py');run(H/'ThirtySix.py');run(H/'ForceSix36.py');run(H/'Complete36.py');run(H/'ForestSeal.py','4','6','22');print('PASS complete (11,462) P11_I00088: all 58/58; first raw tail 243')

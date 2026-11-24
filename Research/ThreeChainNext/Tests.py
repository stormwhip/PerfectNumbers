"""Small regression and negative tests; run with python -I -S Tests.py."""
import importlib.util,sys,json
from pathlib import Path
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('replay_under_test',H/'Replay.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
def rejected(fn):
    try:fn()
    except (ValueError,KeyError):return True
    return False

def run():
    cases=V.load(H/'Certificates.json');cases={x['e']:x for x in cases}
    for n,expected in [(1,False),(2,True),(3,True),(4,False),(91,False),(341550071728321,False),(2**64-59,True),(2**64+13,False)]:V.require(V.mr(n)==expected,'MR test')
    V.require(V.legal(37,2)==False and V.legal(37,4)==all(V.sigma(37,4)%z for z in V.BANNED),'legal test')
    V.require(V.small_discount(27)==sum(V.discount(r,0,27) for r in range(5,11586,2) if r not in V.BANNED and V.mr(r)),'discount sieve tail')
    V.require(V.replay(cases[462])['nodes']>1,'no fold');V.require(rejected(lambda:V.replay(cases[462],cap=1)),'budget exhaustion accepted');V.require(rejected(lambda:V.replay({'e':6,'root':[],'edges':[]})),'OPEN accepted');V.require(rejected(lambda:V.replay({'e':462,'root':[25],'edges':[]})),'bad root accepted');V.require(rejected(lambda:V.replay({'e':462,'root':[],'edges':[['5',2,'43']]})),'invalid edge accepted')
    z=next(int(x) for x in cases[462]['root'] if int(x)>2**64);key=V.sha256(str(z).encode()).hexdigest()[:24];old=V.bundle()[key];V.bundle()[key]=[[z,0,0,1,[0,0]]];V.proven.cache_clear()
    V.require(rejected(lambda:V.proven(z)),'corrupt ECPP accepted');V.bundle()[key]=old;V.proven.cache_clear();V.require(V.proven(z),'restored certificate failed')
    cv=V.coverage(set(cases));V.require(len(cv['complete'])<=len(cases) and not V.coverage(set())['complete'],'representative projected twice')
    print('PASS MR, legal levels, exact price sieve, branch budget/open, divisibility, corrupted ECPP, and empty coverage')
if __name__=='__main__':run()

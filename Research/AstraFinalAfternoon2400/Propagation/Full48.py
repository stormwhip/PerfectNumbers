"""Cold complete canonical key (7,48); no projection to whole shards here."""
from pathlib import Path
import gzip,hashlib,json,subprocess,sys
H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(H.parent/'Seven')]
from VerifyForest import child_domain
import Verify48Price as V
import Full48Square,Full48Ten
import Full48Fourth,Full48Eight

HISTORY=R/'FinalNight2400/LowSeven/Seven48.json.gz'
SHA='8112caf03da5792950ba2d32beded8502c8a2f5e21ebb45d105be66b5e8f9c7e'

def historical():
    data=HISTORY.read_bytes();assert hashlib.sha256(data).hexdigest()==SHA
    sealed=json.loads(gzip.decompress(data));assert (sealed['p'],sealed['e'],sealed['pivot'])==(V.P,48,V.T)
    assert all(node['type']=='forest' for node in sealed['cases'].values())
    A=set(map(int,sealed['cases']));assert len(A)==27
    return A


def main(cold=True):
    assert __debug__
    assert V.prime64(V.P) and V.prime64(V.T) and V.val(V.sigma(V.P,48),V.T)==1
    child,tail=child_domain([(V.P,48)],(19,),V.T)
    A=set(map(int,child));old=historical()
    assert len(A)==31 and tail==125 and old<=A and A-old=={2,4,8,10}
    if cold:
        cmd=[sys.executable,'-I','-S','-B','-X','int_max_str_digits=0']
        subprocess.run(cmd+[str(R/'Night2400/VerifyFibers.py'),str(HISTORY)],check=True)
        Full48Square.main()
        Full48Fourth.main()
        Full48Eight.verify(H.parent/'Seven/Forest48Eight.json.gz')
        Full48Ten.main()
    else:
        Full48Square.main(False);Full48Ten.main(False)
    assert {2,4,8,10}.isdisjoint(old) and old|{2,4,8,10}==A
    print(('PASS full canonical key' if cold else 'Roster only for full canonical key'),
          '(7,48), 31 of 31 direct first assignments, strict raw tail 125. No shard projection asserted.',flush=True)
    return V.P,48

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--sets-only'])
    main(not sys.argv[1:])

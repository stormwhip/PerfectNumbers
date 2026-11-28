"""Full canonical (7,438) certificate composition, including all first/second domains."""
from pathlib import Path
import argparse,json,runpy,subprocess,sys
from hashlib import sha1,sha256
H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Night2400'),str(H.parent/'Propagation')]
from VerifyForest import child_domain,S438,C,B
from VerifyFibers import verify as historical_first
from Verify438Twelve import verify as new_twelve, square_external, PACKS
from VerifyReserved438 import rule
from VerifyReserved438x12 import replay as propagation, ACCEPTED_CORE
from Verify438x22 import replay_euler
NIGHT=R/'Night2400'; FINAL=R/'FinalNight2400'; GEMINI=R/'GeminiFrontier'; PROP=H.parent/'Propagation'
P=[(7,438)]; T=S438

def run(path,*args):
    subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(path),*args],check=True)

def first():
    F,tail=child_domain(P,(19,),T); domain=set(map(int,F))
    assert domain=={2,4,6,10,12,14,16,18,20,22,24,28} and tail==57
    covered=set()
    packs=[(NIGHT/'Fibers7x438.json.gz','112faa9f5618a97bdae40cad1eb6ada8df6b90a18ad68447ceb84383ca3d24a9'),(NIGHT/'G3/Seven438.json.gz','86801a494e509019196ec3a69a4c297bf64f3c33b4405dfe1c44dea27a3e506b')]
    for path,digest in packs:
        r=historical_first(path); assert r['key']==[7,438] and int(r['pivot'])==T and set(r['domain'])==domain and r['sha256']==digest
        c=set(r['covered']);assert covered.isdisjoint(c); covered|=c;print(r,flush=True)
    assert domain-covered=={10,12,18,22}
    f=GEMINI/'SubmittedVerify.py'; data=f.read_bytes().replace(b'\r\n',b'\n')
    assert sha256(data).hexdigest()=='39657ee6eafdd632f800597247b587a0f7d236fe8e8258723ca8cd0676c07469'
    v=runpy.run_path(str(f))
    for q in v['PRATT_CERTS']:v['verify_prime'](q)
    for p,n,d,L in ((7,19,10,[3]),(13,19,10,[3]),(19,99,50,[3,9])):
        assert n>d and (2*p+1)**(d*(p-1))>p**n
        for o in L:assert d*(o-1)>=n and 3**(d*o*(p-1))>=p**n
    v['verify_7_438_f22_f18'](); covered.update((18,22)); assert domain-covered=={10,12}

def twelve(historical=False):
    base=P+[(T,12)]; D,tail=child_domain(base,(19,),27431); known=set(range(28,111,2))
    domain=set(map(int,D));assert domain==set(range(2,111,2)) and tail==221
    assert known=={28}|set(range(30,73,2))|set(range(74,111,2))
    if historical:
        # Full438Ten --historical also replays the 74..110 and 30..72 proofs.
        run(FINAL/'SevenNext/Verify438Last28.py')
    rule(12); replay_euler()
    own=set(); other=set()
    for tag,hs in PACKS.items():
        assert not own.intersection(hs);own.update(hs)
        new_twelve(H/f'Forest438t12{tag}.json.gz',hs,square_external() if tag=='c' else ())
    for hs in (ACCEPTED_CORE,(10,),(26,)):
        path=PROP/('Reserved438x12-'+'-'.join(map(str,hs))+'.json.gz')
        got=propagation(path,hs); want={tuple(sorted(base+[(27431,h)])) for h in hs}
        assert got==want and not other.intersection(hs);other.update(hs)
    run(PROP/'Verify438x22.py'); assert 22 not in other; other.add(22)
    assert own=={2,4,6,8} and other=={10,12,14,16,18,20,22,24,26}
    assert not own&other and not (own|other)&known and own|other|known==domain
    print('PASS entire first fiber t^12: 55 direct, frozen 42, new 13; exclusive raw size tail 221',flush=True)

def incidence():
    def load(name,blob):
        d=(GEMINI/name).read_bytes().replace(b'\r\n',b'\n')
        assert sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==blob
        return json.loads(d)
    a=load('ShardToKeys.json','de821605b9bb0c124ff8ca4a576f85ced96afaa2'); b=load('KeyToShards.json','efad9522397f1b9a79aaf27c4ab90e65d58d1683')
    s='P7_I00084'; k=[7,438]; assert a[s]==[k] and [h for h,ks in a.items() if k in ks]==[s] and b['7,438']==[s]
    old=json.loads((FINAL/'OpenFrontier.json').read_bytes()); assert old['ShardRemainders'][s]==[k]
    print('PASS complete exact canonical key (7,438); singleton',s,flush=True)

if __name__=='__main__':
    assert __debug__
    parser=argparse.ArgumentParser(); parser.add_argument('--historical',action='store_true'); parser.add_argument('--twelve-only',action='store_true'); a=parser.parse_args()
    assert not(a.twelve_only and a.historical)
    if not a.twelve_only:
        first();run(H/'Full438Ten.py',*(['--historical'] if a.historical else []))
    twelve(a.historical)
    if not a.twelve_only:incidence()

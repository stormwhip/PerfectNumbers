"""Cold scoped replay plus exact, disjoint exhaustive coverage of 7^438,t^10."""
import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path.insert(0,str(H))
from VerifyForest import child_domain, S438, known_scope, verify
from VerifyReserved438 import PACKS, rule, verify as verify_reserved

# Frozen historical membership, checked against the stored source constants by
# cold replay below (the independently reviewed historical proof fixes q^1).
OLD={
 'base':set(range(228,293,2)),
 'further':{148,172,190,200,212,214,216,218,220,222,226,294,296,298,300},
 'mixed1':{192,194,196,198,202,204,206,208,210,224},
 'mixed2':{160,162,164,166,168,170,174,176,178,180,182,184,186,188},
}
NIGHT=R/'FinalNight2400'
SCRIPTS=(NIGHT/'Seven/Verify438.py',NIGHT/'SevenNext/Verify438New.py',NIGHT/'SevenNext/VerifyMixed67.py',NIGHT/'SevenNext/VerifyMixed67More.py')
PREF=[(7,438),(S438,10)]

def check_partition():
    cand,tail=child_domain(PREF,(19,),67); domain=set(map(int,cand)); assert domain==set(range(2,301,2))
    done=set(); new=set(); n=0
    for key,hs in OLD.items():
        assert hs<=domain and hs.isdisjoint(done); done|=hs
    assert len(done)==72 and domain-done==(set(range(2,159,2))-{148})
    for tag in 'abcdefgh':
        p=H/f'Forest438{tag}.json.gz'; d=json.loads(gzip.decompress(p.read_bytes())); hs=[]
        for rec in d['records']:
            row=list(map(tuple,rec['P'])); assert row[:-1]==PREF and row[-1][0]==67 and rec['bad']==[19] and not rec['unresolved']
            assert known_scope(row,(19,))=='438'; hs.append(row[-1][1])
        assert len(hs)==len(set(hs)) and set(hs)<=domain and set(hs).isdisjoint(done|new)
        if tag in PACKS:assert hs==PACKS[tag]
        n+=1;new.update(hs)
        print(tag,'covered',hs,'sha256',sha256(p.read_bytes()).hexdigest(),flush=True)
    assert len(new)==78 and done|new==domain
    print('7^438,t^10 full domain:',len(domain),'old',len(done),'new',len(new),'raw tail',tail,'packets',n,flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--historical',action='store_true',help='also cold replay the four frozen historical verifiers');a=p.parse_args()
    assert __debug__; check_partition()
    for tag in 'abc':verify(H/f'Forest438{tag}.json.gz')
    rule()
    for tag in PACKS:verify_reserved(tag)
    if a.historical:
        for path in SCRIPTS:
            subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(path)],check=True)
    print('PASS complete canonical first fiber v_t(N)=10;', 'historical arithmetic cold replay included' if a.historical else 'frozen historical coverage used as a dependency',flush=True)

if __name__=='__main__':main()

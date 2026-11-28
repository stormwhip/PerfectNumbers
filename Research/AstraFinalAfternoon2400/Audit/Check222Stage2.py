"""Independent exact coverage for the second-stage root-222 certificate union."""
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckForest222Domains import parts,live,T,U,R


def doc(p):return json.loads(gzip.decompress(p.read_bytes()))


def main():
    assert __debug__
    prev=doc(R/'Nineteen/Forest222.json.gz')['windows']
    fn=R/'Nineteen/Forest222Stage2.json.gz'; assert sha256(fn.read_bytes()).hexdigest()=='10688cbd5ecab9ca8fbd88ffc3c61a454f86febcdac43289359685a037f6dae0'
    stage=doc(fn)
    old=R.parent/'FinalNight2400/Root222'
    second=doc(old/'TwoForests.json.gz')['cases'];third=doc(old/'ThirdForests.json.gz')['cases']
    wanted={(1,2):{2,4},(2,2):{4,18},(2,46):{None},(18,2):{2,12}}
    group={}
    for w in stage['cases']:
        rows=[tuple(x) for x in w['prefix']];f,g=rows[1][1],rows[2][1]
        assert rows[:3]==[(19,222),(T,f),(U,g)] and parts(rows)
        assert f in live(rows[:1],T)[0] and g in live(rows[:2],U)[0] and str(g) not in second[str(f)]
        key=f'{f}:{g}'
        if len(rows)==3:
            assert key not in third and key not in prev
            j=None
        else:
            q,j=rows[3]; frozen=third[key]; assert frozen['q']==q
            a,tail=live(rows[:3],q); earlier={int(i) for i in frozen['children']}; residual=set(frozen['left'])
            assert earlier|residual==a and not earlier&residual
            assert (f,g) in {(1,2),(2,2),(18,2)} # no Gemini/earlier inert cut in these domains
            assert residual-set(prev[key]['closed'])==set(stage['windows'][key]['before'])
            assert j in residual and j not in prev[key]['closed'] and tail==stage['windows'][key]['raw_tail']
        assert j in wanted[(f,g)] and j not in group.setdefault((f,g),set());group[(f,g)].add(j)
        mass=parts(rows); roots,edges,head=w['forest']; V=set(roots)|{t for t,_ in edges}; assert len(V)==len(roots)+len(edges)
        assert all(mass%p==0 for p in roots) and all(mass%p for p,_ in edges) and not set(dict(rows))&V
        assert all(parent in V for _,parent in edges) and 0<head<=1024
    assert group==wanted and stage['windows']['2:2']['after']==[] and stage['windows']['2:46']['after']==[]
    print('PASS independent raw domains, frozen/first-stage exclusions subtraction, 7 strict-forest scopes, two fully covered secondary prefixes')

if __name__=='__main__':main()

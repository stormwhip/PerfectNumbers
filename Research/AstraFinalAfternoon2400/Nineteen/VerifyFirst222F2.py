"""Compose the exact first exponent-two union at canonical (19,222)."""
from pathlib import Path
import subprocess,sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import B,C,HERE,RESEARCH,need,readz,domain,T,R


def main():
    need(__debug__,'assertions required')
    f=2; root=((19,222),); P=root+((T,f),)
    a=RESEARCH/'FinalNight2400/Root222'
    first,ft=domain(root,T);second,st=domain(P,R)
    need(len(first)==53 and ft==144 and f in first,'first scope')
    orig=readz(a/'TwoForests.json.gz')['cases']['2'];left=set(second)-set(map(int,orig))
    need(left=={2,16,22,46},'frozen exact second complement')
    cases=readz(a/'ThirdForests.json.gz')['cases'];needed={}
    for g in (2,16,22):
        row=cases[f'2:{g}'];q=row['q'];d,tail=domain(P+((R,g),),q)
        old=set(map(int,row['children']));new=set(row['left']);need(set(d)==old|new and not old&new,'third initial partition')
        needed[g]=new
    need(needed=={2:{2,4,18,28},16:{1,2,4,18,28},22:{1,2,4,18,28}} and '2:46' not in cases,'initial exact live windows')
    P1=readz(HERE/'Forest222.json.gz')['windows'];P2=readz(HERE/'Forest222Stage2.json.gz')['windows'];P3=readz(HERE/'Forest222Stage3.json.gz')['windows'];m=readz(HERE/'Mask222J4.json.gz');p=readz(HERE/'Plain222J2.json.gz');e=readz(HERE/'Root222J18.json.gz');w=readz(HERE/'Root222J28.json.gz')
    for k,g in [('Plain222J2.json.gz',2),('Mask222J4.json.gz',4),('Root222J18.json.gz',18),('Root222J28.json.gz',28)]:
        d=readz(HERE/k);need(tuple(map(tuple,d['prefix']))==P+((R,22),(2032322226061,g)),'exact leaf binding')
    need(P1['2:2']['closed']==[2,28] and P2['2:2']['closed']==[4,18] and P2['2:46']['closed']==[None] and P3['2:16']['closed']==[2,4,18,28],'distinct accepted overlays')
    need(e['remaining']==[2],'j18 upper remainder must be exactly exponent two')
    lo=readz(HERE/'Root222J18Low.json.gz')
    need(tuple(map(tuple,lo['prefix']))==tuple(map(tuple,e['prefix']))+((e['pivot'],2),) and not lo['remaining'],'j18 low branch incomplete')
    results={2:{2,4,18,28},16:{1,2,4,18,28},22:{1,2,4,18,28}}
    need(needed==results,'some existing second condition not covered')
    scripts=['Inert222','VerifyForest222','VerifyForest222Stage2','VerifyForest222Stage3','VerifyMask222J4','VerifyPlain222J2','VerifyRoot222J18','VerifyRoot222J28','VerifyRoot222J18Low']
    for name in scripts:subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(HERE/(name+'.py'))],check=True)
    print('COMPLETE (19,222) canonical exact first exponent 2, raw first tail',ft,'second tail',st,'remaining f=[1,18]')

if __name__=='__main__':main()

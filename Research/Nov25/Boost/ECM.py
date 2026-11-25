"""Capped GMP-ECM on current minimizing cyclotomic residuals (hints only)."""
from collections import defaultdict
import argparse,math,re,subprocess,time
from pathlib import Path
from BoostScore import arithmetic,scorer,load,valuation,nonsupport,H
from Search import divisors,phi,hints,prime,CACHE
import json

E='/mnt/e/PerfectNumbers/NightCache/ecm/pkg/usr'

def ecm(n,b1,curves,seconds,log):
    cmd=['wsl','-d','Ubuntu','--','timeout',f'{seconds}s','env',f'LD_LIBRARY_PATH={E}/lib/x86_64-linux-gnu',f'{E}/bin/ecm','-maxmem','64','-q','-one','-c',str(curves),str(b1)]
    with log.open('wb') as outf:
        sc=subprocess.run(cmd,input=f'{n}\n'.encode(),stdout=outf,stderr=subprocess.STDOUT,timeout=seconds+12,cwd=H)
    vals={int(x) for x in re.findall(rb'\b[0-9]{2,1000}\b',log.read_bytes().replace(b'\0',b''))}
    return sorted(x for x in vals if 1<x<n and n%x==0),sc.returncode

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('path',type=Path);ap.add_argument('--seconds',type=int,default=180);ap.add_argument('--b1',type=int,default=15000);ap.add_argument('--curves',type=int,default=800);ap.add_argument('--label',default='ecm1');a=ap.parse_args()
    row=load(a.path);p,e=row['p'],row['e'];W={q:u/row['den'] for q,u in row.get('rho',[])};vs,t=scorer(row,W); states=t(min(vs,key=vs.get)); t.clear()
    dl=time.monotonic()+a.seconds; targets=[]
    owned=math.prod(dict(row['owners']))
    for z,(_,f,_,w) in states.items():
        if w is False:continue
        for d in divisors(f+1)-{1}:
            n=nonsupport(phi(z,d),math.gcd(phi(z,d),owned)*2*math.prod(hints(z,f)))
            if 72<=n.bit_length()<=4000 and not prime(n):targets.append((n.bit_length(),z,d,n))
    targets.sort(); out={}
    for j,(bits,z,d,n) in enumerate(targets):
        sec=int(dl-time.monotonic())
        if sec<=1:break
        sec=min(sec,max(30,a.seconds//2)); print(p,e,'ECM cell',z,d,bits,sec,flush=True)
        try:qs,ret=ecm(n,a.b1,a.curves,sec,H/f'{p}x{e}-{a.label}-{j}.log')
        except subprocess.TimeoutExpired:continue
        ps=set(q for x in qs for q in (x,n//x) if prime(q)); print(p,e,'ECM result',ret,sorted(ps),flush=True)
        if ps:
            out[z,d]=sorted(ps)
            (H/f'{p}x{e}-{a.label}.json').write_text(json.dumps([(a,b,c) for (a,b),c in out.items()])+'\n',encoding='utf8')

if __name__=='__main__':main()

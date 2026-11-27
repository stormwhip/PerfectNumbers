"""Bounded ECM discovery on selected cyclotomic residuals. Hints are untrusted."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess
import sys

from Verify130 import H,R,PIVOT
sys.path.insert(0,str(R/'Session20261126'))
from Discover import Finder, Bank, phi, ds, fmpz


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--index',type=Path,required=True);ap.add_argument('--prefix',required=True)
    ap.add_argument('--seconds',type=int,default=90);ap.add_argument('--b1',type=int,default=60000);ap.add_argument('--curves',type=int,default=400)
    ap.add_argument('--workers',type=int,default=4);ap.add_argument('--label',required=True);ap.add_argument('--hint');ap.add_argument('input',nargs='+',help='base:exponent or q:exponent');a=ap.parse_args()
    F=Finder(Bank(a.index),0); current=json.loads((H/a.hint).read_bytes()) if a.hint else {}
    def run(task):
        z,e,d,u=task
        for q in sorted(set(F.factors(z,e))|set(current.get(f'{z}:{e}',[]))):
            while u%q==0:u//=q
        if u==1 or fmpz(u).is_probable_prime():return z,e,[u] if u>2 else []
        if u.bit_length()<=90:return z,e,[int(q) for q,_ in fmpz(u).factor() if q>2]
        cmd=['wsl','-d','Ubuntu','--','timeout','--kill-after=4',str(a.seconds),'env',
             f'LD_LIBRARY_PATH={a.prefix}/lib/x86_64-linux-gnu',f'{a.prefix}/bin/ecm','-maxmem','64','-q','-one','-c',str(a.curves),str(a.b1)]
        try:
            r=subprocess.run(cmd,input=f'{u}\n'.encode(),capture_output=True,timeout=a.seconds+12)
            vals={int(x) for x in re.findall(rb'\b[0-9]{2,1300}\b',r.stdout.replace(b'\0',b''))}; out=[]
            for q in vals:
                if 1<q<u and u%q==0:
                    out += [k for k in (q,u//q) if k>2 and fmpz(k).is_probable_prime()]
            print(z.bit_length(),e,d,u.bit_length(),r.returncode,sorted(set(out)),flush=True)
            return z,e,out
        except subprocess.TimeoutExpired:
            return z,e,[]
    tasks=[]
    for word in a.input:
        z,e=word.split(':'); z=PIVOT if z=='q' else int(z);e=int(e)
        tasks.extend((z,e,d,phi(z,d)) for d in ds(e+1)[1:])
    with ThreadPoolExecutor(a.workers) as pool:
        for z,e,out in pool.map(run,tasks):
            key=f'{z}:{e}';current[key]=sorted(set(current.get(key,[]))|set(out))
            (H/a.label).write_text(json.dumps(current,separators=(',',':')),encoding='utf8')


if __name__=='__main__':main()

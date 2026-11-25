"""Certify the three alternative four-prime hitting sets by exact support composition."""
import sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from AuditLarge import check

def main():
 if not __debug__:raise SystemExit('Do not use -O')
 a=sys.argv[1:];assert a in ([],['--baseline'],['--only-new'])
 if a!=['--only-new']:subprocess.run([sys.executable,'-I','-S','-B',str(H/'ReleasePairs.py'),*a],check=True)
 Q=(17,19,23)
 for q,expect in zip(Q,(2436,2408,2409)):
  d,b=check(f'Pack-New-Big{q}.json.gz');assert d['extra']==[3,5,11,q] and d['x']==[] and d['lower']==[[p,1] for p in (7,13,*[k for k in Q if k!=q])] and b==expect
  print('PROVED hitting set',d['extra'],flush=True)
 print('Reason: prior sets imply absent 3,5,11 forces 7,13 and at least two of 17,19,23. If q is absent, the other two are forced, exactly the checked cell. Hence all three and 7,13 are present. No complete canonical exponent or shard is credited.',flush=True)
if __name__=='__main__':main()

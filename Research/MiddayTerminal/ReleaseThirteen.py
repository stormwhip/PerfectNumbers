"""A second new three-element theorem: 3,5,13. The final floor is exactly 2400;
strict dyadic comparison, not this displayed floor, is essential."""
from pathlib import Path
import subprocess,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from AuditLarge import check

def main():
 if not __debug__:raise SystemExit('Do not use -O')
 a=sys.argv[1:];assert a in ([],['--baseline'],['--only-new'])
 if a!=['--only-new']:subprocess.run([sys.executable,'-I','-S','-B',str(H/'ReleaseTriple.py'),*a],check=True)
 for file,bad,pos,score in [('PackNewBigNo11.json.gz',[3,5,13,17],[7,11],2500),('PackNewTriple3513.json.gz',[3,5,13],[7,11,17],2400)]:
  d,f=check(file);assert d['x']==[] and d['extra']==bad and d['lower']==[[q,1] for q in pos] and f==score
 print('If 3,5 are absent then {3,5,7} and {3,5,11} force both 7 and 11. With 13 also absent, the first packet forces 17 and the second packet excludes that last support class. PROVED {3,5,13}; absent 3,5 implies 7,11,13 all divide N. This alone adds 0 complete canonical exponents/shards.',flush=True)
if __name__=='__main__':main()

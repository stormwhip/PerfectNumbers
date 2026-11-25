"""Independent validation of 31 positive-cell exact trees (including multi-level exponent tails)."""
from pathlib import Path
import json,gzip,sys,argparse,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Independent31 import replay,sig,req,valuation,prime64

def audit(label):
 y,n,d,sec,cut={'513':([5,13],[3],'Support513',13,65),'517':([5,17],[3,13],'Support517',17,65),'3':([3],[5],'Support3',3,90)}[label];pkt=json.loads(gzip.decompress((H/(d+'.json.gz')).read_bytes()));A=[[31,10]];q=150332843;req(pkt['assigned']==A and pkt['present']==y and pkt['absent']==n,'root');bad=math.prod([19,7,11,*n]);scores=[]
 def walk(A,t,low=None,depth=0):
  low=low or {};kind=t['kind']
  if kind=='forest':
   names=set(t['roots'])|dict(t['owners']).keys();cs={str(w):pkt['ecpp'][str(w)] for w in names if w>=2**64};scores.append(replay(dict(assigned=A,present=y,absent=n,leaf=t,ecpp=cs),low));return
  req(kind=='exp' and depth<2,'split depth');r=t['q'];s=t['cut'];req((r,s)==((q,100) if depth==0 else (sec,cut)) and prime64(r),'scope');D=math.prod(sig(z,f)//(2 if f%2 else 1) for z,f in A);req(r not in dict(A) and (not D%r or r in y),'compelled');a=valuation(D,r);locked=any(f%2 for z,f in A)
  cells=[f for f in range(1,s+1) if f>=a and (not f%2 or not locked and r%4==f%4==1) and math.gcd(sig(r,f),bad)==1];req(set(t['cells'])==set(map(str,cells)),'cell completeness');
  for f in cells:walk(A+[[r,f]],t['cells'][str(f)],low,depth+1)
  walk(A,t['tail'],{**low,r:s+1},depth+1)
 walk(A,pkt['leaf']);print('INDEPENDENT',label,len(scores),min(scores),flush=True)
if __name__=='__main__':audit(sys.argv[1])

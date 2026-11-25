"""Build or replay exact exception tree. Scope and missing branches are independently reconstructed."""
from pathlib import Path
import gzip,json,sys,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Independent31 import replay,sig,valuation,prime64,level,req
q0=150332843; bign=32848452483811177815421
# Each row keys previous actual exponents of compulsory components. An optional deeper split may only be attached by explicit registration.
SPLITS={(): (q0,100,'31only3',110,12),(40,):(5659,100,'31only3x40w5659',95,7),(52,):(107,130,'31only3x52w107',90,6),(40,2):(967,95,'C40w2',100,10),(40,6):(bign,42,'C40w6',110,13),(52,4):(627091,70,'C52w4',90,9)}

def data(f):return json.loads(gzip.decompress(f.read_bytes()))
def walk(mode,path,A,bank,t,scores,holes,src=None):
 q,cut,where,head,rounds=SPLITS[path];D=math.prod(sig(z,f)//(2 if f%2 else 1) for z,f in A);req(D%q==0 and q not in dict(A),'pivot scope');bad=19*7*11*5;vc=valuation(D,q);locked=any(f%2 for z,f in A);K=[f for f in range(1,cut+1) if f>=vc and (not f%2 or not locked and q%4==f%4==1) and math.gcd(sig(q,f),bad)==1];
 if mode=='build':t=dict(q=q,cut=cut,cells={})
 else:req(q==t['q'] and cut==t['cut'] and set(t['cells'])=={str(f) for f in K},'coverage')
 for k in [*K,0]:
  ax=A if not k else A+[[q,k]];key=str(k) if k else 'tail';inode=t['cells'] if k else t
  if path+(k,) in SPLITS:
   inode[key]=walk(mode,path+(k,),ax,bank,inode.get(key),scores,holes,src);continue
  if mode=='build':
   if k:
    fs=list((H/where).glob(f'*-{q}x{k}.json.gz'))
    if not fs:inode[key]={'kind':'exception'};holes.append(path+(k,));continue
    assert len(fs)==1;u=data(fs[0]);req(u['assigned']==ax and u['present']==[3] and u['absent']==[5],'leaf assignment');bank.update(u['ecpp']);leaf=u['leaf']
   else:
    from Compose import State,B
    s=State(ax,[3],[5],{q:cut+1});b,r,_=src.bound(s,head,rounds);print('tail',path,q,len(str(b))-1,flush=True);assert b>B
    leaf=dict(kind='forest',**r)
    for z in set(r['roots'])|dict(r['owners']).keys():
     if z>=2**64:bank[str(z)]=src.cert[str(z)]
   inode[key]=leaf
  else:
   leaf=inode[key]
   if leaf=={'kind':'exception'}:holes.append(path+(k,));continue
   names=set(leaf.get('roots',[]))|dict(leaf.get('owners',[])).keys()|set(dict(ax));cs={str(z):bank[str(z)] for z in names if z>=2**64};scores.append(replay(dict(assigned=ax,present=[3],absent=[5],leaf=leaf,ecpp=cs),{q:cut+1} if not k else {}));
 return t

def main():
 F=H/'Refined31.json.gz';mode=sys.argv[1];holes=[];scores=[];assert mode in ('build','check')
 if mode=='build':
  sys.path.insert(0,str(H.parent/'Nov25/Compose'));from Scout import Sources
  src=Sources(31,10,True,True);bank={};t=walk(mode,(),[[31,10]],bank,None,scores,holes,src);F.write_bytes(gzip.compress(json.dumps(dict(tree=t,exceptions=holes,ecpp=bank),separators=(',',':')).encode(),mtime=0))
 else:
  X=data(F);bank=X['ecpp'];ar=bank[str(bign)];a=bign
  for row in ar:req(row[0]==a,'chain');a=level(*row)
  req(prime64(a) and all(prime64(z) for z in [q0,107,5659,627091,967]),'pivots');walk(mode,(),[[31,10]],bank,X['tree'],scores,holes);req([list(z) for z in holes]==X['exceptions'],'exception list')
 print(mode,'leaves',len(scores),'minimum',min([z for z in scores if z is not None],default=None),'exceptions',holes,flush=True)
if __name__=='__main__':main()

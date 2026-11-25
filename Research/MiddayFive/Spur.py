"""Exact child exponents with all authentic prime labels. One independently
checkable output packet per disjoint (e, primary exponent) branch."""
from Joint import *
import argparse

def extend(e):
 if not (H/f'Extra{e}.json.gz').is_file():return
 extra=json.loads(gzip.decompress((H/f'Extra{e}.json.gz').read_bytes()));row=data()['rows'][str(e)];parent=dict(row['owners']);q=max(row['roots']);data()['ecpp'].update(extra)
 for zstr,proof in extra.items():
  z=int(zstr);assert prime(z)
  if z not in set(parent)|set(row['roots']):parent[z]=q
 row['owners']=[[z,p] for z,p in parent.items()]

def scan(e,f,L=5001,cut=32,cap=48):
 extend(e);row=data()['rows'][str(e)];q=max(row['roots']);x=[[q,f]];m=model(e,x,L,cut,cap);b,w=solve(m);out=dict(e=e,f=f,L=L,cut=cut,cap=cap,initial=b,basew=w if b>=2400 else [],z=None,leaves=[],open=[]);file=H/f'Spur{e}x{f}.json.gz'
 def save():file.write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0))
 print(e,f,'unconditional cell floor after charges',b,flush=True);save()
 if b>=2400:return
 y=sigma(q,f);z=max([p for p in set(dict(row['owners']))|set(row['roots']) if p!=q and y%p==0],default=0)
 if not z:return
 r=y;v=0
 while r%z==0:v+=1;r//=z
 out['z']=z
 # Pure-power bound suffices past this limit, even ignoring output expenses.
 budget=B//(5**e*q**f);capf=0;power=1
 while power*z<=budget:power*=z;capf+=1
 # For smaller z keep gap-free tail after first ten legal exact exponents.
 fs=[i for i in range(v,capf+1) if (not i%2 or i%4==z%4==1) and allowed(z,i,BAD)];lim=fs[10] if len(fs)>10 else capf+1;out['limit']=lim
 for h in [i for i in fs if i<lim]+([lim] if lim<=capf else []):
  xx=x+([[z,h]] if h<lim else []);lo=[[z,h]] if h==lim else [];m=model(e,xx,L,cut,cap,lo);b,w=solve(m);print('child',e,f,h,b,flush=True)
  if weighted(m,w)>2400*W*lg(10)[1]:out['leaves'].append(dict(h=h,w=w))
  else:out['open'].append(h)
  save()
if __name__=='__main__':
 for val in sys.argv[1:]:scan(*map(int,val.split(':')))

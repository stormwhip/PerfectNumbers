"""Cold replay of both disjoint cover parts of 11^358 in the canonical class."""
from pathlib import Path
import gzip,json,sys,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path.insert(0,str(N))
spec=importlib.util.spec_from_file_location('g_eleven',N/'G/Verify.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
sys.path.insert(0,str(H))
from ElevenPrice import verify as price
from VerifyFibers import verify
if __name__=='__main__':
 assert __debug__
 p=N/'G/Eleven358.json.gz';old.verify(p);a=set(json.loads(gzip.decompress(p.read_bytes()))['full_fibers']);v=verify(H/'Eleven358Five.json.gz');assert v['key']==[11,358] and v['pivot']==str(old.Q) and len(a)==9 and len(v['covered'])==5 and len(v['domain'])==16
 price(28);price(30);assert not set(v['covered']) & {28,30};v['covered'] += [28,30]
 b=set(v['covered']);assert not a&b and a|b==set(v['domain']);print('FULL canonical exact key (11,358), 16/16; P11_I00070.',flush=True)

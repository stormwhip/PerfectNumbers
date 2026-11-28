"""One complete canonical pair, not a projection: immutable G7 + all verified complements."""
from pathlib import Path
import sys,runpy,importlib.util
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from FinalFibers import verify,ROOT,Q,R
from Verify import run

def load(name,file):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 assert __debug__;gdir=R/'Night2400/G7';g=load('g7_frozen',gdir/'MaskedVerify.py');assert (g.P,g.E,g.Q)==(*ROOT,Q);M=g.verify(gdir/'Seven882.json.gz');assert set(M)==set(range(2,256,4));assert {f for row in M.values() for f in row}=={1,2,4,8,12,72}
 for f in (2,8):assert {m for m,r in M.items() if f in r}=={50,54,58,178,186}
 runpy.run_path(str(H.parent/'Audit/SevenEight/Verify.py'),run_name='__main__');m=load('root7_joint72',H.parent/'Root7Joint/Verify.py');m.check()
 assert not run(12)
 for f in (1,4,8,2):verify(f)
 print('FULL canonical (7,882), P7_I00152: 70 first exponents; all 64 support masks.',flush=True)
if __name__=='__main__':main()

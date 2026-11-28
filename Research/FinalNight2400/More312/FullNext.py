from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path.insert(0,str(N));from VerifyFibers import verify
sp=importlib.util.spec_from_file_location('g4_root19',N/'G4/Verify.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
if __name__=='__main__':
 assert __debug__
 a=old.verify(N/'G4/Nineteen372.json.gz');b=verify(H/'Nineteen372Five.json.gz');assert old.P==19 and old.E==372 and str(old.Q)==b['pivot'] and b['key']==[19,372] and a['root_domain']==b['domain'];u=set(a['covered']);v=set(b['covered']);assert len(u)==10 and len(v)==5 and not u&v and u|v==set(b['domain']);print('FULL canonical (19,372) all 15 firsts; singleton P19_I00072.',flush=True)

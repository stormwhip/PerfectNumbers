"""Scoped exact forest sets plus independent root-domain scan. No full key."""
import sys,subprocess,json,gzip,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'Night2400'));from VerifyFibers import verify
for n,e,k,dom,expected in [('Seven16',16,44,91,'4af54b1088f307019fbfe2a5b74e7faa5e6834488ae4445fee864fd56b917145'),('Low18',18,30,44,'b68b20069c0c73143109afefcd4e54e999fbe24933d26e5f0963587cfdaeb7e0'),('Seven48',48,27,31,'8112caf03da5792950ba2d32beded8502c8a2f5e21ebb45d105be66b5e8f9c7e')]:
 p=H/(n+'.json.gz');assert __debug__ and hashlib.sha256(p.read_bytes()).hexdigest()==expected;v=verify(p);assert v['key']==[7,e] and len(v['domain'])==dom and len(v['covered'])==k
 subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(H/'TreeAudit.py'),str(p)],check=True)

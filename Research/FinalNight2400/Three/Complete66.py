"""Bind the frozen old packet to the exact hole filled by the new proof. Optional old cold replay."""
from pathlib import Path
import json,gzip,sys,hashlib,importlib.util
H=Path(__file__).resolve().parent;R=H.parents[1];D=R/'Night2400/B';sys.path.insert(0,str(H));import Partial66 as W
BIND={D/'Fiber66.json.gz':'caa7837039a620cd4451dc9344f1455d6c9956550e55c014a9aa7321dcae186c',H/'WholeR.json.gz':'e7a078323af59eb79f0ff1c82b10de2aad62e7e2c3340e50d7d8bd735ad65beb'}

def main():
 assert __debug__ and sys.argv[1:] in ([],['--replay-old']);old,new=BIND
 for path,h in BIND.items():assert hashlib.sha256(path.read_bytes()).hexdigest()==h
 spec=importlib.util.spec_from_file_location('old66',D/'Verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 O=json.loads(gzip.decompress(old.read_bytes()));assert O['f']==66 and O['tree']['q']==5897
 rows,tail=v.domain([(3,12),(797161,66)],5897);k=set(O['tree']['cases']);assert tail==430 and len(rows)==97 and set(rows)-k=={'6'} and k<=rows.keys() and rows['6']==list(W.K.F[:3]);print('old 96/97 exact, raw tail 430, sole hole 6',flush=True)
 if len(sys.argv)>1:
  rr=v.verify(old);assert rr['unresolved']==[6] and rr['covered']==96
 W.audit('WholeR.json.gz');print('PASS completed first-pivot v797161=66 under canonical v3=12. Not the whole key.',flush=True)
if __name__=='__main__':main()

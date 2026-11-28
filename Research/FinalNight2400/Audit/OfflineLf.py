"""Recreate LF transport in a private temporary directory; never mutate checkout.
Run from any directory: python -B OfflineLf.py. Default historical prerequisites enabled.
"""
from pathlib import Path
import subprocess, tempfile, shutil, time, os, sys, json, hashlib
A=Path(__file__).resolve().parent
R=A.parents[2]
flags=['-I','-S','-B','-X','int_max_str_digits=0']
with tempfile.TemporaryDirectory(prefix='Lf',dir=A) as tmp:
    root=Path(tmp); research=R/'Research'; files=set()
    for path in (research,R/'Sources'):
        for f in path.rglob('*.py'):
            if not f.is_relative_to(research/'FinalNight2400'): files.add(f)
    for folder in ('GeminiFrontier','Night2400/G8','Night2400/C10'):
        files.update(f for f in (research/folder).glob('*') if f.is_file())
    files.add(research/'Night2400/ShardToKeys.json')
    for f in sorted(files):
        out=root/f.relative_to(R);out.parent.mkdir(parents=True,exist_ok=True)
        if f.suffix in ('.py','.md','.json'):
            out.write_bytes(f.read_bytes().replace(bytes((13,10)),bytes((10,))))
        else: shutil.copyfile(f,out)
    for key,script in [('Ten','VerifyT10.py'),('Gemini','Verify.py')]:
        cmd=[sys.executable,*flags,'Research/GeminiFrontier/'+script];t=time.perf_counter()
        with (A/(key+'Lf.log')).open('wb') as fp:
            proc=subprocess.run(cmd,cwd=root,stdout=fp,stderr=subprocess.STDOUT,env=dict(os.environ,TMP=tmp,TEMP=tmp,TMPDIR=tmp))
        result=dict(exit=proc.returncode,seconds=round(time.perf_counter()-t,3),cmd=cmd)
        (A/(key+'LfTiming.json')).write_text(json.dumps(result,indent=2)+chr(10));print(key,result,flush=True)

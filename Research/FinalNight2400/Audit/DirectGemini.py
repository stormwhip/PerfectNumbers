"""Repeat exact frozen commands after canonical LF restoration; optional psutil monitors RSS."""
from pathlib import Path
import os,sys,subprocess,tempfile,json,time
try:import psutil
except ImportError:psutil=None
H=Path(__file__).resolve().parent;root=H.parents[2]
for script,label in [('Verify.py','Gemini'),('VerifyT10.py','Ten')]:
    cmd=[sys.executable,'-I','-S','-B','-X','int_max_str_digits=0','Research/GeminiFrontier/'+script];t=time.perf_counter();peak=0
    with tempfile.TemporaryDirectory(dir=H,prefix='Temp') as tmp,(H/(label+'Direct.log')).open('wb') as out:
        pp=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,cwd=root,env=dict(os.environ,TMP=tmp,TEMP=tmp,TMPDIR=tmp))
        if psutil is None:pp.wait()
        else:
            parent=psutil.Process(pp.pid)
            while pp.poll() is None:
                try:procs=[parent,*parent.children(recursive=True)]
                except psutil.NoSuchProcess:break
                rss=0
                for proc in procs:
                    try:rss+=proc.memory_info().rss
                    except (psutil.NoSuchProcess,psutil.AccessDenied):pass
                peak=max(peak,rss)
                try:pp.wait(timeout=.5)
                except subprocess.TimeoutExpired:pass
        code=pp.wait()
    data=dict(command=cmd,exit=code,seconds=round(time.perf_counter()-t,3),sampled_tree_rss_bytes=peak or None,poll_seconds=.5)
    (H/(label+'DirectTiming.json')).write_text(json.dumps(data,indent=2)+chr(10));print(label,data,flush=True)

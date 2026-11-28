"""Run the five baseline checks; preserve outputs, process status and elapsed times."""
from datetime import datetime,timezone
import json,os,subprocess,sys,tempfile,time
from pathlib import Path
here=Path(__file__).resolve().parent
root=here.parents[2]
flags=['-I','-S','-B','-X','int_max_str_digits=0']
checks={'Structure':['Sources/Python/RepositoryStructureChecks.py'],'Ledger':['-I','-S','-B','Sources/Python/FinalSprintLedgerChecks.py'],'Replay':flags+['Research/Night2400/Replay.py'],'Gemini':flags+['Research/GeminiFrontier/Verify.py'],'Ten':flags+['Research/GeminiFrontier/VerifyT10.py']}
if __name__=='__main__':
 for key in sys.argv[1:]:
    cmd=[sys.executable,*checks[key]]
    start=datetime.now(timezone.utc).isoformat(); t=time.perf_counter()
    with tempfile.TemporaryDirectory(dir=here,prefix='Temp') as tmp, (here/(key+'.log')).open('wb') as out:
        r=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,cwd=root,env=dict(os.environ,TMP=tmp,TEMP=tmp,TMPDIR=tmp,PYTHONDONTWRITEBYTECODE='1'))
    data=dict(command=cmd,start=start,seconds=round(time.perf_counter()-t,3),exit=r.returncode)
    (here/(key+'Timing.json')).write_text(json.dumps(data,indent=2)+'\n', encoding='utf-8');print(key,data,flush=True)

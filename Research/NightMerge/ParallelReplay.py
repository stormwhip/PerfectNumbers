"""Resource-bounded final replay. Partitions only by whole proofs, never by a shortened tree.
Persists positive receipts keyed by all tracked source/data blobs on the proof branch.
A changed release invalidates the cache; use --fresh to ignore it completely.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,json,sys,hashlib,time,argparse,os
from tempfile import TemporaryDirectory
from Checkpoint import R,H,read,merge

def run(cmd,cwd,log):
    start=time.perf_counter()
    with log.open('wb') as f:proc=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    if proc.returncode:raise RuntimeError(f'Incomplete replay ({proc.returncode}); see {log}')
    return round(time.perf_counter()-start,3)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=8);ap.add_argument('--receipts',type=Path,required=True,help='external checkpoint folder; not proof inputs');ap.add_argument('--fresh',action='store_true');args=ap.parse_args();assert 1<=args.workers<=24 and __debug__;D=R.parent;args.receipts.mkdir(exist_ok=True,parents=True);reg=read(H/'Batches.json');jobs=[]
    def add(label,*params):jobs.append((label,[sys.executable,'-B',*map(str,params)]))
    add('pilot',R/'EveningTree/IndependentTree.py','--allow-overlap','--valuation','--input',H/'Pilot.json')
    for n in reg['order']:add('order-'+n,R/'NightOrder/Replay.py','--input',n)
    for n in reg['three']:add('three-'+n,R/'NightThree/Verify.py',n)
    for n in reg['five']:add('five-'+n,R/'NightFive/Verify.py',n)
    if reg['five_more']:add('five-more',R/'NightFive/VerifyMore.py')
    for n,script in reg['five_extra']+reg.get('five_chain',[]):add('five-'+n,R/'NightFive'/script)
    for script,params,records in reg.get('uniform',[]):add('uniform-'+script+'-'+str(records[0][1]),R/'NightUniformReview'/script,*[str(R/'NightUniformReview'/v) if v.endswith('.gz') and script=='Verify31.py' else v for v in params])
    for n in reg.get('source_nodes',[]):add('source-nodes-'+n,R/'NightUniform/ReleaseNode.py',R/'NightUniform'/n)
    for n in reg.get('extra',[]):add('extra-'+n,H/'ExtraVerify.py',n)
    # Bind receipts to actual bytes of tracked inputs, not merely a Git label. Never cache untracked dependencies.
    # Final check must run in a clean detached worktree containing only released inputs.
    if subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=D).strip():raise RuntimeError('Dirty files. Use a clean publication checkout.')
    if subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=D).strip():raise RuntimeError('Unexpected files in proof checkout; use a clean worktree.')
    files=subprocess.check_output(['git','ls-files','-z','Research'],cwd=D).decode().split('\0');digest=hashlib.sha256()
    for fn in sorted(filter(None,files)):
        digest.update(fn.encode()+b'\0'+hashlib.sha256((D/fn).read_bytes()).digest())
    key=digest.hexdigest();print('input SHA256',key,'jobs',len(jobs),flush=True);start=time.time()
    def job(item):
        name,cmd=item;safe_name=name.replace('/','_').replace('\\','_');rec=args.receipts/(safe_name+'.json');log=args.receipts/(safe_name+'.log');prev=read(rec) if rec.exists() else {}; old=prev.get('sha256')==key and prev.get('passed') is True
        if old and not args.fresh:return name,'cached',prev['seconds']
        sec=run(cmd,D,log);temp=rec.with_suffix('.tmp');temp.write_text(json.dumps(dict(name=name,sha256=key,passed=True,seconds=sec,log=log.name))+'\n');temp.replace(rec);return name,'replayed',sec
    # Schedule known long tails first. Only scheduling order changes: every proof still runs, and aggregation waits for every result.
    slow={'five-Batch18.json':100000,'five-Batch16.json':90000,'five-Batch19.json':60000,'five-Batch14.json':40000,'five-Batch17.json':35000,'five-Batch15.json':30000,'order-Batch08.json':25000}
    jobs.sort(key=lambda item: -slow.get(item[0],10000 if item[0].startswith('order-') else 0))
    with ThreadPoolExecutor(args.workers) as pool:
        for result in as_completed([pool.submit(job,item) for item in jobs]):print(*result.result(),flush=True)
    # A second isolated process checks that the exact proven union reproduces the release ledger.
    subprocess.run([sys.executable,'-B',str(H/'Checkpoint.py'),'--manifest-only'],cwd=D,check=True);print('all packets passed',len(jobs),'wall seconds',round(time.time()-start,1))
if __name__=='__main__':main()

"""Run all 13x568 states, including six exact anonymous guards. Requires python-flint==0.9.0, mathematical arithmetic only. No discovery cache is read."""
from pathlib import Path,PurePosixPath
import hashlib,sys,os,json,subprocess,tempfile,zipfile
H=Path(__file__).resolve().parent;RESEARCH=H.parents[1];PIN='053bce309ab468980e839ace2e73ee33c77a1a3e63bfedc7c6e4e57f4b3df20e'

def verify():
    if not __debug__:raise ValueError('assertions required')
    m=json.loads((H/'Manifest.json').read_bytes());arc=H/'Proof.zip';assert hashlib.sha256(arc.read_bytes()).hexdigest()==PIN==m['archive_sha256']
    with tempfile.TemporaryDirectory() as temp:
        top=Path(temp)
        with zipfile.ZipFile(arc) as z:
            assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(m['files'])
            for n,dig in m['files'].items():
                assert not PurePosixPath(n).is_absolute() and not {'..','.'}.intersection(PurePosixPath(n).parts) and '\\' not in n and ':' not in n
                f=top/n;b=z.read(n);assert hashlib.sha256(b).hexdigest()==dig;f.parent.mkdir(exist_ok=True,parents=True);f.write_bytes(b)
        vv=os.environ.get('PERFECTNUMBERS_FLINT_PATH');extra=[str(Path(vv).resolve())] if vv else [];prog=top/'Recursive/Domain.py';packet=top/'Recursive/Recursive13x568.json.gz'
        # -I ignores user site and PYTHONPATH. An explicit vendor dir is optional; otherwise use this interpreter's ordinary system site installation.
        cmd="import sys,runpy; sp=sys.argv[1:]; sys.path[:0]=sp[3:]; sys.argv=sp[:3]; runpy.run_path(sp[0],run_name='__main__')";p=subprocess.Popen([sys.executable,'-I','-B','-X','int_max_str_digits=0','-c',cmd,str(prog),str(RESEARCH),str(packet),*extra],stdout=subprocess.PIPE,text=True);end=''
        for line in p.stdout:end=line.strip();print(line,end='',flush=True)
        assert p.wait()==0;v=json.loads(end);assert (v['p'],v['e'])==(13,568) and v['rules']['anonymous-square']==6
    return dict(packet='Anon568/Proof.zip',sha256=PIN,seed=[13,568],actuals=[568],receipt=v)
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))

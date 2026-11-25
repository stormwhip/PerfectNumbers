"""Reproduce the historical candidate output; mathematical acceptance is in Progress.md."""
import runpy
import sys
from pathlib import Path
folder=Path(__file__).resolve().parent/'Candidate'
sys.path.insert(0,str(folder))
import Check
sys.modules['check']=Check
sys.argv=[str(folder/'VerifyP31162.py'),str(folder/'P3E1162Complete.json')]
runpy.run_path(sys.argv[0],run_name='__main__')

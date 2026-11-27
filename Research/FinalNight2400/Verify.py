"""Replay the independently accepted overlay; not the historical baseline."""
import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
for name in ('Root7Joint/Verify.py','Audit/CheckSeven.py','Dual/Verify.py','Seven/DualSweep.py','Fifth/Verify.py','Project.py'):
    subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(here/name)],check=True)

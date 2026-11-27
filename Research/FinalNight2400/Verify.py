"""Replay the independently accepted overlay; not the historical baseline."""
import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
for name in ('Root7Joint/Verify.py','Audit/CheckSeven.py','Dual/Verify.py','Seven/DualSweep.py','Fifth/Verify.py','Dual/Explore.py','Others/Audit18.py','Eleven/One.py','Nineteen/Verify282.py','VerifyOtherForests.py','Ten/VerifyFull.py','Audit/CheckTen.py','Audit/CheckPrices.py','Others/Full31.py','Seven/Verify12.py','Seven/LowOne.py','Seven/Verify42.py','Seven/Verify438.py','Disjoint/Verify.py','Eleven/FortySix.py','Others/AuditEleven46.py','Audit/SevenEight/Verify.py','Three/Abundance.py','Support/Verify.py','Project.py'):
    subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(here/name)],check=True)

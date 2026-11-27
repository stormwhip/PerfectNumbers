"""Offline research overlay with full targeted dependencies. This is not the entire project history."""
import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
CHECKS='''
Root7Joint/Verify.py
Audit/CheckSeven.py
Dual/Verify.py
Seven/DualSweep.py
Fifth/Verify.py
Dual/Explore.py
Others/Audit18.py
Eleven/One.py
Nineteen/Verify282.py
VerifyOtherForests.py
Ten/VerifyFull.py
Audit/CheckTen.py
Audit/CheckPrices.py
Others/Full31.py
Seven/Verify12.py
Seven/LowOne.py
Seven/Verify42.py
Seven/Verify438.py
Disjoint/Verify.py
Eleven/FortySix.py
Others/AuditEleven46.py
Audit/SevenEight/Verify.py
Three/Abundance.py
Support/Verify.py
Others/Full13.py
Audit/CheckThirteen.py
Nineteen/Verify618.py
Nineteen/Verify618Square.py
Nineteen/Verify618Credit.py
SevenNext/Audit618.py
Others/FullNext.py
Audit/CheckNext.py
Batch/Verify.py
Eleven/FortyTwo.py
Eleven/Six42.py
Nineteen/Verify618Factored.py
Nineteen/VerifyOne.py
Sieve/OneAudit.py
Nineteen/VerifyAnchor.py
SevenNext/Audit618.py --credit
SevenNext/Audit618.py --anchor
Three/Hard66.py
Three/Six.py
Three/VerifyForests.py
Three/Full.py 16 18 22
SevenNext/VerifyTertiary.py
SevenNext/VerifyFour.py
SevenNext/Abundance.py
Others/FullMore.py
Audit/CheckMore.py
Triple/Verify.py
ThirtyOne/Verify16.py
Audit/CheckSixteen.py
Project.py
'''.splitlines()
if __name__=='__main__':
    for item in filter(None,CHECKS):
        script,*args=item.split()
        subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(here/script),*args],check=True)

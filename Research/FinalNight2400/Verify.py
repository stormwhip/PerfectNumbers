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
Three/Full.py 16 18 22 96 126
SevenNext/VerifyTertiary.py
SevenNext/VerifyFour.py
SevenNext/Abundance.py
Others/FullMore.py
Audit/CheckMore.py
Triple/Verify.py
ThirtyOne/Verify16.py
Audit/CheckSixteen.py
Nineteen/VerifyAnchorMore.py
Nineteen/VerifyNested.py
Nineteen/VerifyTwelve.py
Nineteen/VerifySmallTen.py
Nineteen/VerifyInner.py
AuditNext/Inner282.py
SevenNext/CompleteSix.py
Audit/CheckSecondary.py
Eleven/ThirtySix.py
Eleven/ForceSix36.py
Eleven/Complete36.py
TenNext/Verify46.py
TenNext/VerifyAlternate.py
TenNext/VerifyDOne.py
Audit/CheckDOne.py
ThirtyOne/Full31x16.py
AuditNext/Check31Partitions.py
Triple/Discrete.py
Nineteen/VerifySmallEight.py
AuditNext/CheckSmall.py Solved8.json
SevenNext/VerifyTwo.py
Others/FullEleven.py
AuditNext/CheckEleven358.py
Eleven/FullKey.py
AuditNext/Check462.py
Three/Complete66.py --replay-old
AuditNext/Check66.py
Batch/Low.py
Nineteen/VerifySmallSix.py
AuditNext/Lattice.py
AuditNext/CheckSmall.py Solved6.json
Others/FullLast.py
AuditNext/Check388.py
Batch/TwoTrees.py
Nineteen/VerifySmallFour.py
AuditNext/CheckSmall.py Solved4.json
More312/Full.py
Seven430/Full430.py
AuditNext/Check430.py
Project.py
'''.splitlines()
if __name__=='__main__':
    for item in filter(None,CHECKS):
        script,*args=item.split()
        subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(here/script),*args],check=True)

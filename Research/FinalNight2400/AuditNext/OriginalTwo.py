"""Independent final f2 replay using original unoptimized exact kernel. No FastBounds or FastKernel imports."""
from pathlib import Path
import json,sys,time
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
H=Path(__file__).resolve().parents[1]/'Nineteen';sys.path.insert(0,str(H));import VerifyNested,BestKernel
P=json.loads((H/'Solved2.json').read_bytes());assert set(P['cases'])=={'2'};VerifyNested.Kernel=BestKernel.Kernel;s=time.perf_counter();VerifyNested.main(P);assert 'FastKernel' not in sys.modules;print('PASS unoptimized original f2 arithmetic',round(time.perf_counter()-s,3),'s')

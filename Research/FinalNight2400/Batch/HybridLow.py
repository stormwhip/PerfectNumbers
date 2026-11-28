from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from Hybrid import verify
if __name__=='__main__':
 verify('HybridSmall.json.gz',[4,6,12,24]);verify('HybridTwentySix.json.gz',[26])

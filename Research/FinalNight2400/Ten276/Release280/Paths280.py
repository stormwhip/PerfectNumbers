from pathlib import Path
p=19;s=353998162545967;t=5967366623139106062930976717;y=16208389663;r=4465757330217695897641;z=167887043133006663319040440782979;k=132001981879
pre=[(p,280),(s,2)]; paths=[pre+[(t,4),(r,2),(z,a)] for a in [2,4]]+[pre+[(t,4),(r,a)] for a in [8,10]]+[pre+[(t,6),(y,12),(k,22)]]+[pre+[(t,6),(y,a)] for a in [18,22,28,30,36,40,42]]+[pre+[(t,10),(y,a)] for a in [22,28,36]]+ [[(p,280),(s,e)] for e in [16,18]]+[pre+[(t,4),(r,1)]]
# Direct children of the first-squared pivot; index is 18+position in Tdomain.
Tdomain=[1,2,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26,28,29,30]
paths += [pre+[(t,e)] for e in Tdomain]
# High first s valuations, then mandatory y; IDs 41..70 (s^16), 71..99 (s^18).
paths += [[(p,280),(s,e),(y,f)] for e,count in [(16,30),(18,29)] for f in range(2,2*count+1,2)]

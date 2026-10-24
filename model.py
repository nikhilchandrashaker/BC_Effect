import openpyxl, re, math, json, random
import numpy as np
wb=openpyxl.load_workbook('/mnt/user-data/uploads/Bullet_Club_Impact_Database_EXHAUSTIVE_PUBLIC_RESEARCH.xlsx',data_only=True)
def rows(n):
    return [list(map(lambda c:'' if c is None else str(c),r)) for r in list(wb[n].iter_rows(values_only=True))[3:] if r[0] and r[1]]
M=rows('Members');T=rows('Impact Timeline');MER=rows('Merchandise');A=rows('Audience & Events')
yr=lambda s:int(s[:4]) if s[:4].isdigit() else None
Y=list(range(2013,2027))
roster=[sum(1 for m in M if yr(m[2]) and yr(m[2])<=y<=(yr(m[3]) or 2026)) for y in Y]
ms=[sum(1 for t in T if yr(t[0])==y) for y in Y]
def num(x):
    try:return float(x)
    except:return None
mu=[]
for y in Y:
    s=0
    for r in MER:
        if re.fullmatch(r'\d{4}(-\d\d)?',r[2]) and yr(r[2])==y and r[5]=='shirts' and num(r[4]): s+=num(r[4])
    mu.append(math.sqrt(s))
au=[]
for y in Y:
    v=[num(r[4]) for r in A if yr(r[2])==y and num(r[4])]
    au.append(math.log10(max(v)) if v else 0)
nm=lambda a:np.array(a)/max(a)
C=np.array([nm(roster),nm(ms),nm(mu),nm(au)])
S=lambda w:100*(np.array(w)@C)/sum(w)
base=S([1,1,1,1]);print(dict(zip(Y,base.round(0))))
print('roster',roster,'ms',ms)
rng=np.random.default_rng(1);peaks=[]
for _ in range(10000):
    w=rng.dirichlet([1,1,1,1]);peaks.append(Y[int(np.argmax(S(w)))])
from collections import Counter;print(Counter(peaks))
# scenarios
sc={'Equal':[1,1,1,1],'Roster-heavy':[4,1,1,1],'Commercial-heavy':[1,1,4,1],'Audience-heavy':[1,1,1,4],'No merch':[1,1,0,1]}
for k,w in sc.items():print(k,Y[int(np.argmax(S(w)))])
np.save('C.npy',C);json.dump(dict(Y=Y,roster=roster,ms=ms),open('m.json','w'))

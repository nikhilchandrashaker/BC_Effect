import openpyxl, json
wb=openpyxl.load_workbook('/mnt/user-data/uploads/Bullet_Club_Impact_Database_EXHAUSTIVE_PUBLIC_RESEARCH.xlsx',data_only=True)
def rows(n,hdr=3):
    ws=wb[n]; out=[]
    for r in list(ws.iter_rows(values_only=True))[hdr:]:
        if r[0] is None or r[1] is None: continue
        out.append([('' if c is None else str(c)) for c in r])
    return out
D={k:rows(n) for k,n in dict(m='Members',t='Impact Timeline',p='Promotion Impact',s='Subgroups',c='Championships & Awards',r='Related & Inspired',mer='Merchandise',a='Audience & Events',g='Data Gaps').items()}
html=open('t.html').read().replace('__DATA__',json.dumps(D,ensure_ascii=False,separators=(',',':')))
open('bullet_club_dashboard.html','w').write(html)
print(len(html), {k:len(v) for k,v in D.items()})

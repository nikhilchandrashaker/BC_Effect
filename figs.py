import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from collections import Counter
exec(open('model.py').read().split("# scenarios")[0].replace("print(","(lambda *a,**k:None)("))
G='#b8941f';K='#111111';GR='#8c8c8c';LG='#d9d9d9'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
def save(n):plt.tight_layout();plt.savefig(n,dpi=200);plt.close()
# F1 roster + eras
fig,ax=plt.subplots(figsize=(6.5,3.0))
eras=[('Devitt',2013.35,2014.27),('Styles',2014.27,2016.01),('Omega',2016.01,2018.83),('White',2018.83,2023.18),('Finlay',2023.18,2026.01)]
for i,(n,a,b) in enumerate(eras):
    ax.axvspan(a,b,color=LG if i%2==0 else '#efefef',zorder=0);ax.text((a+b)/2,36,n,ha='center',fontsize=8,color=GR)
ax.bar(Y,roster,color=K,width=.7,zorder=2)
for y,r in zip(Y,roster):ax.text(y,r+.6,r,ha='center',fontsize=8)
ax.set_ylim(0,40);ax.set_xticks(Y);ax.set_xticklabels([str(y)[2:] for y in Y]);ax.set_ylabel('Members active');ax.set_xlabel("Year ('13 to '26)")
save('f1.png')
# F2 index stacked contributions
w=np.array([1,1,1,1]);contrib=(C*25).T  # each comp share of 100 under equal weights
labs=['Roster','Milestones','Merch units','Audience peak'];cols=[K,GR,G,'#d8c27a']
fig,ax=plt.subplots(figsize=(6.5,3.0));bot=np.zeros(14)
for k in range(4):ax.bar(Y,contrib[:,k],bottom=bot,color=cols[k],label=labs[k],width=.7);bot+=contrib[:,k]
for y,v in zip(Y,bot):ax.text(y,v+1,f'{v:.0f}',ha='center',fontsize=8)
ax.set_xticks(Y);ax.set_xticklabels([str(y)[2:] for y in Y]);ax.set_ylabel('Index (0-100)');ax.set_ylim(0,88);ax.legend(ncol=4,frameon=False,fontsize=8,loc='upper left')
save('f2.png')
# F3 sensitivity
rng=np.random.default_rng(1);pk=Counter()
for _ in range(10000):
    ww=rng.dirichlet([1,1,1,1]);pk[Y[int(np.argmax(S(ww)))]]+=1
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.5,2.7),gridspec_kw={'width_ratios':[1,1.3]})
ks=[2017,2023,2025];a1.bar([str(k) for k in ks],[pk[k]/100 for k in ks],color=[G,K,GR]);a1.set_ylabel('% of 10,000 weightings');a1.set_title('Peak year, random weights',fontsize=9)
for i,k in enumerate(ks):a1.text(i,pk[k]/100+1,f'{pk[k]/100:.1f}%',ha='center',fontsize=8)
sc={'Equal weights':[1,1,1,1],'Roster-heavy':[4,1,1,1],'Merch-heavy':[1,1,4,1],'Audience-heavy':[1,1,1,4],'No audience':[1,1,1,0],'No merch':[1,1,0,1]}
for i,(n,ww) in enumerate(sc.items()):
    s=S(ww);a2.plot(Y,s/ s.max()*100,marker='o',ms=2.5,lw=1,color=[K,GR,G,'#d8c27a','#5a5a5a','#c9c9c9'][i],label=n)
a2.set_xticks(Y[::2]);a2.set_ylabel('Index, scaled to own peak');a2.set_ylim(0,135);a2.legend(fontsize=6.5,frameon=False,ncol=3,loc='upper center');a2.set_title('Index shape under six weightings',fontsize=9)
save('f3.png')
print({n:Y[int(np.argmax(S(ww)))] for n,ww in sc.items()},{k:v for k,v in pk.items()})
# F4 hot topic
fig,ax=plt.subplots(figsize=(6.5,2.8))
items=['Bullet Club','Kenny Omega','Young Bucks'];ini=[7000,1900,2700];re_=[25000,18000,22000];x=np.arange(3)
ax.bar(x-.18,ini,.36,color=GR,label='Initial order');ax.bar(x+.18,re_,.36,color=K,label='Reorder (about 3 months)')
for i in range(3):ax.text(x[i]+.18,re_[i]+500,f'{re_[i]/ini[i]:.1f}x',ha='center',fontsize=8)
ax.set_xticks(x);ax.set_xticklabels(items);ax.set_ylabel('Shirts');ax.legend(frameon=False,fontsize=8)
save('f4.png')
# F5 diffusion gantt
P=[('NJPW (Japan)',2013,2026),('CMLL (Mexico)',2013,2019),('ROH (US)',2014,2019),('WWE (alumni, not a BC branch)',2016,2026),('NJPW Strong (US)',2020,2024),('Impact/TNA (US)',2021,2024),('AEW (US)',2021,2026),('NJPW Tamashii (AUS/NZ)',2022,2025)]
fig,ax=plt.subplots(figsize=(6.5,3.0))
for i,(n,a,b) in enumerate(P):ax.barh(i,b-a,left=a,color=GR if 'WWE' in n else K if i==0 else G,height=.55)
ax.set_yticks(range(len(P)));ax.set_yticklabels([p[0] for p in P],fontsize=8);ax.invert_yaxis();ax.set_xlim(2013,2027);ax.set_xticks(range(2013,2027,2))
save('f5.png')
# F6 causal chain
def box(ax,x,y,t,fc='white',ec=K,w=2.3,h=.9,ls='-'):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.03',fc=fc,ec=ec,lw=1.2,ls=ls));ax.text(x,y,t,ha='center',va='center',fontsize=7.5)
def arr(ax,x1,y1,x2,y2,ls='-',c=K):ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=10,lw=1.2,ls=ls,color=c))
fig,ax=plt.subplots(figsize=(6.5,3.4));ax.set_xlim(0,13.4);ax.set_ylim(0,6.2);ax.axis('off')
box(ax,1.7,5,'Bullet Club\n(NJPW, 2013)');box(ax,5,5,'Elite sub-group\nand brand');box(ax,8.3,5,'Hot Topic and PWT\nmerch, 2017-18');box(ax,11.3,5,'Elite members leave\nBC, Oct 2018')
box(ax,1.7,2.6,'All In, Sep 2018\n11,263 attended\n~50,000 buys',w=2.5,h=1.1);box(ax,5.6,2.6,'Demonstrated non-WWE\nlarge-event demand',ls='--',w=2.9);box(ax,9.7,2.6,'AEW begins, 2019\nElite central',w=2.5)
for a,b in [(2.9,3.8),(6.2,7.1),(9.5,10.2)]:arr(ax,a,5,b,5)
arr(ax,8.3,4.5,2.8,3.2,'--',GR);arr(ax,3.0,2.6,4.1,2.6,'--',GR);arr(ax,7.1,2.6,8.4,2.6,'--',GR);arr(ax,11.3,4.5,10.8,3.2)
ax.plot([0.6,1.4],[0.7,0.7],color=K,lw=1.2);ax.text(1.6,.7,'Documented in workbook',fontsize=7.5,va='center')
ax.plot([5.2,6],[0.7,0.7],color=GR,lw=1.2,ls='--');ax.text(6.2,.7,'Interpretation, not proven',fontsize=7.5,va='center')
save('f6.png')
# F7 lineage network
fig,ax=plt.subplots(figsize=(6.5,4.0));ax.set_xlim(0,13.5);ax.set_ylim(0,8);ax.axis('off')
N={'bc':(2,4,'Bullet Club\n2013-2026',K,'white'),'aj':(5.2,6.8,'AJ Styles,\nGallows, Anderson','white',K),'club':(8.6,6.8,'The Club / O.C.\n(WWE)','#e8e8e8',K),
'god':(5.2,5.0,'G.O.D.\nTonga / Loa','white',K),'bl':(8.6,5.0,'Bloodline / MFT\nlineage (WWE)','#e8e8e8',K),
'el':(5.2,3.0,'The Elite','white',K),'allin':(8.6,3.0,'All In\n2018','white',K),'aew':(11.7,3.0,'AEW\nElite, 2019 on','#f3e7b8',K),
'jw':(5.2,1.1,'Jay White,\nBC Gold','white',K),'bbg':(8.6,1.1,'Bang Bang Gang\n(AEW)','#f3e7b8',K),'wd':(2,1.4,'Finlay, War Dogs\n(final NJPW era)','white',K)}
for k,(x,y,t,fc,tc) in N.items():
    ax.add_patch(FancyBboxPatch((x-1.35,y-.55),2.7,1.1,boxstyle='round,pad=0.03',fc=fc,ec=K,lw=1.1));ax.text(x,y,t,ha='center',va='center',fontsize=7.3,color='white' if fc==K else 'black')
E=[('bc','aj'),('bc','god'),('bc','el'),('bc','jw'),('aj','club'),('god','bl'),('el','allin'),('jw','bbg'),('x','y'),('x','y')]
for a,b in E[:-2]:
    xa,ya=N[a][:2];xb,yb=N[b][:2];arr(ax,xa+1.4 if a!='bc' else xa+1.35,ya if a!='bc' else ya,xb-1.4,yb)
arr(ax,N['allin'][0]+1.4,3.0,N['aew'][0]-1.4,3.0,'--',GR);arr(ax,2,3.4,2,1.97)
ax.text(.2,7.6,'Grey fill: WWE (talent lineage, not an official BC branch). Gold fill: AEW. Dashed: inferred link.',fontsize=7)
save('f7.png')

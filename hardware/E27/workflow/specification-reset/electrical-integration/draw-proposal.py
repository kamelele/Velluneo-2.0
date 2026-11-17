from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
D=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(11,6));ax.set_xlim(-1,10);ax.set_ylim(-1,6);ax.axis('off')
ax.text(-.6,5.7,'ECO-01 | Proposed discharge networks',fontsize=18,weight='bold')
ax.text(-.6,5.25,'UNAPPROVED • independent circuit proposal • existing KiCad unchanged',fontsize=10,color='#a23c22')
def line(x,y):ax.plot(x,y,c='#294a65',lw=2)
def resistor(x,y,name,value):
 line([x,x],[y+.5,y+.2]);ax.add_patch(Rectangle((x-.16,y-.2),.32,.4,fill=False,lw=2,edgecolor='#294a65'));line([x,x],[y-.2,y-.5]);ax.text(x+.3,y+.02,name+'  '+value,va='center',fontsize=11)
line([0,3.5],[4.5,4.5]);line([0,3.5],[.5,.5]);ax.text(-.5,4.8,'BULK_POS',fontsize=10);ax.text(-.5,.1,'PRIMARY_GND',fontsize=10)
for x,refs in [(0,['R2','R3']),(3.5,['R14','R15'])]:
 line([x,x],[4.5,3.8]);resistor(x,3.3,refs[0],'499 kΩ');line([x,x],[2.8,2.2]);resistor(x,1.7,refs[1],'499 kΩ');line([x,x],[1.2,.5])
ax.text(.35,2.5,'BLEED_MID',fontsize=8);ax.text(3.85,2.5,'BLEED_MID_B',fontsize=8)
ax.text(-.1,-.45,'All four: 2512 / candidate CRCW2512499KFKEG\nSeparate series branches; common rails remain shared.',fontsize=10)
x=7.5;line([x,x],[4.5,3.]);resistor(x,2.5,'R13','1 MΩ');line([x,x],[2.,.5]);ax.text(x-.4,4.8,'VDD',fontsize=10);ax.text(x-1,.1,'PRIMARY_GND',fontsize=10)
ax.text(6.3,-.45,'0603 / candidate CRCW06031M00FKEA\nBias discharge only; adds bias load.',fontsize=10)
fig.text(.07,.02,'Not a PCB, KiCad capture, complete power circuit, safety approval or measured service waiting time.',fontsize=9,color='#8c2b21')
fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(D/'ECO-01.png',dpi=150);fig.savefig(D/'ECO-01.svg');plt.close(fig)

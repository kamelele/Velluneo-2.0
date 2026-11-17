#!/usr/bin/env python3
"""Mechanical space illustration, explicitly not a PCB placement or safety design."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyBboxPatch
P=Path(__file__).resolve().parent
v=json.loads((P/'space-proposal.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
fig=plt.figure(figsize=(15,8),facecolor='#f5f7fa')
ax=fig.add_axes([.055,.27,.68,.55]);ax.set_aspect('equal');ax.set_xlim(-9,85);ax.set_ylim(-9,51);ax.axis('off')
fig.text(.055,.93,'Velluneo | driver board space study',fontsize=23,fontweight='bold',color='#182c3a')
fig.text(.055,.875,'CONCEPT ONLY — not a KiCad PCB or a manufacturing layout',fontsize=13,fontweight='bold',color='#aa4c14')
ax.add_patch(FancyBboxPatch((0,0),75,40,boxstyle='round,pad=0,rounding_size=1.2',edgecolor='#2f6556',facecolor='#e4f0e9',linewidth=2))
for item in v['items']:
 ref=item['ref'];x=item['x'];y=item['y'];w=item['w'];h=item['h']
 if ref=='CBULK':
  ax.add_patch(Circle((x,y),w/2,facecolor='#394b59',edgecolor='#172733',linewidth=1.5));ax.text(x,y,'CBULK\n450 V',ha='center',va='center',color='white',fontsize=9)
 elif ref=='T1':
  ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor='#fff4d9',edgecolor='#a87723',hatch='///',linewidth=1.2,alpha=.8))
  ax.add_patch(Rectangle((x-25.2/2,y-26/2),25.2,26,facecolor='#485363',edgecolor='#172733',linewidth=1.5))
  ax.text(x,y+2,'T1\nEFD25 bobbin',ha='center',va='center',fontsize=11,color='white',fontweight='bold')
  ax.text(x,y-7,'25.2 × 26 mm\nbody projection',ha='center',va='center',fontsize=8,color='white')
 else:
  color={'F1':'#c4a87a','RIN':'#bdb4a4','COUT':'#b7c4cc','DOUT':'#677c8e'}[ref]
  ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor=color,edgecolor='#364956',linewidth=1.3))
  ax.text(x,y,ref,ha='center',va='center',rotation=90 if h>w*1.3 else 0,fontsize=10,color='white' if ref=='DOUT' else '#1e2b33',fontweight='bold')
ax.annotate('E27\nwires',xy=(0,10),xytext=(-8,10),ha='center',va='center',fontsize=9,color='#36596b',arrowprops={'arrowstyle':'->','color':'#36596b'})
ax.annotate('LED\nwires',xy=(75,20),xytext=(83,20),ha='center',va='center',fontsize=9,color='#36596b',arrowprops={'arrowstyle':'->','color':'#36596b'})
ax.annotate('',xy=(0,-5),xytext=(75,-5),arrowprops={'arrowstyle':'<->','color':'#345362'})
ax.text(37.5,-7,'75 mm — proposed, not approved',ha='center',fontsize=10,color='#345362')
ax.annotate('',xy=(78,0),xytext=(78,40),arrowprops={'arrowstyle':'<->','color':'#345362'})
ax.text(80,36,'40 mm',rotation=90,fontsize=10,color='#345362')
ax.text(0,44,'BODY ENVELOPES / RESERVED SPACE ONLY',fontsize=10,color='#3e5e6a',fontweight='bold')
notes=fig.add_axes([.765,.27,.21,.55]);notes.axis('off')
notes.text(0,.97,'What this shows',fontsize=14,fontweight='bold',color='#182c3a')
notes.text(0,.85,'6 dominant components\nof the 28-item schematic',fontsize=11,linespacing=1.6,color='#405664')
notes.text(0,.62,'Transformer reserve: 30 × 30 mm\nComplete winding/core/yoke\nenvelope still to be qualified.',fontsize=10,linespacing=1.6,color='#405664')
notes.text(0,.34,'Not demonstrated:\n• room for the other 22 items\n• copper, pads or drill positions\n• electrical safety distances\n• thermal or enclosure fit',fontsize=10,linespacing=1.7,color='#7a482b')
fig.text(.055,.17,'The EFD25 transformer and the 450 V capacitor dominate the mechanical space.',fontsize=13,color='#263f4d',fontweight='bold')
fig.text(.055,.12,'Green outline = a proposed space budget. Coloured bodies are not qualified footprints.\nThis is a planning illustration; no native .kicad_pcb, routed board or fabrication output is generated.',fontsize=10.5,color='#566c79',linespacing=1.7)
fig.savefig(P/'driver-space-concept.png',dpi=160,facecolor=fig.get_facecolor())
fig.savefig(P/'driver-space-concept.svg',facecolor=fig.get_facecolor())

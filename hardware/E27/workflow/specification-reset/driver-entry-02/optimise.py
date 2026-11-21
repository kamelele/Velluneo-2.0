"""Reproducible pre-CAD connection-length study; never a router or PCB approval."""
from pathlib import Path
import json, math, random, hashlib
import numpy as np
D=Path(__file__).resolve().parent; P=D.parent
inv=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'))
parts={p['ref']:p for p in inv['parts']}; refs=list(parts); idx={r:i for i,r in enumerate(refs)}
source=json.loads((P/'assembly-fit-01/packing-diagnostic.json').read_text(encoding='utf-8'))
electrical={p['ref']:p for p in json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'))}
fixed={'T1','C1','C4','R1','F1','J1','J2'}; semis={'U1','Q1','BR1','D1','D2','D3','TVS1'}
W,L=32.,60.
# Weights are search priorities only, not datasheet numerical requirements.
links=[('U1.1','C2.1',6),('U1.4','C2.2',6),('U1.1','C3.1',3),('U1.4','C3.2',3),
 ('U1.2','R4.2',8),('U1.2','R5.1',8),('R5.2','U1.4',4),('T1.4','R4.1',1),
 ('U1.5','R6.2',8),('R6.1','R9.1',5),('Q1.3','R9.1',6),('R9.2','C1.2',3),
 ('U1.4','R9.2',2),('U1.6','R7.1',5),('R7.2','Q1.1',6),('R8.1','Q1.1',2),('R8.2','Q1.3',2),
 ('T1.5','Q1.2',5),('T1.5','D1.2',5),('D1.1','TVS1.1',5),('TVS1.2','T1.1',5),('C1.1','T1.1',3),
 ('Q1.3','R6.1',2),('T1.4','D2.2',2),('D2.1','R10.1',2),('R10.2','C2.1',2),
 ('U1.3','RT1.1',2),('RT1.2','U1.4',2),('R13.1','C2.1',1),('R13.2','C2.2',1),
 ('T1.10','D3.2',5),('D3.1','C4.1',5),('C4.2','T1.6',5),('C4.1','J2.1',2),('C4.2','J2.2',2),
 ('C1.1','BR1.1',1),('C1.2','BR1.3',1),('BR1.4','R1.2',1),('F1.2','R1.1',1),('J1.1','F1.1',1),('J1.2','BR1.2',1),
 ('R2.2','R3.1',1),('R14.2','R15.1',1),('R2.1','C1.1',.3),('R3.2','C1.2',.3),('R14.1','C1.1',.3),('R15.2','C1.2',.3)]
for a,b,w in links:
 ar,ap=a.split('.');br,bp=b.split('.')
 assert electrical[ar]['pins'][ap]==electrical[br]['pins'][bp] and electrical[ar]['pins'][ap] is not None,(a,b)
def trans(x,y,c):
 a,b,ang,side=c
 if side=='B':y=-y
 if ang==90:x,y=y,-x
 return x+a,y+b
def box(b,c):
 xy=[trans(x,y,c)for x in(b[0],b[2])for y in(b[1],b[3])]
 return np.array([min(x for x,y in xy),min(y for x,y in xy),max(x for x,y in xy),max(y for x,y in xy)])
def geometry(r,c):
 p=parts[r];court=box(p['courtyard_bbox_mm'],c)
 if r=='T1':court=np.array([c[0]-15,c[1]-15,c[0]+15,c[1]+15])
 pads={};padboxes=[];domains=[]
 for pp in p['pads']:
  x,y=trans(*pp['xy_mm'],c);w,h=pp['size_mm']
  if c[2]==90:w,h=h,w
  pads[r+'.'+pp['pin']]=np.array([x,y]);padboxes.append([x-w/2,y-h/2,x+w/2,y+h/2])
  domains.append((r=='T1' and pp['pin']in('6','7','8','9','10')) or r in{'C4','D3','R11','R12','J2'})
 return court,pads,np.array(padboxes),np.array(domains),np.array([pp['tht']for pp in p['pads']])
def overlap(a,b,g=0):return a[0]<b[2]+g and b[0]<a[2]+g and a[1]<b[3]+g and b[1]<a[3]+g
initial={r:tuple(source['positions'][r][k]for k in('x_mm','y_mm','angle_deg','side'))for r in refs}
pos=dict(initial)
# Independent read-only topology implementer supplied a constructive seed with no
# semiconductor courtyard under T1. Root checks the stronger joint/metal constraints.
seed_moves={'U1':(-11.5,11,0,'F'),'Q1':(4,12.5,0,'F'),'BR1':(12,12.5,0,'F'),'D1':(-11.5,15.75,0,'F'),'TVS1':(-1.2,20.1,0,'B'),'D3':(-10.5,-24,0,'B')}
pos.update(seed_moves);geo={r:geometry(r,c)for r,c in pos.items()}
def valid(r,c,g):
 court,_,pb,dom,tht=g
 if court[0]<-16 or court[2]>16 or court[1]<-30 or court[3]>30:return False
 if np.any(pb[:,:2]<[-15.5,-29.5]) or np.any(pb[:,2:]>[15.5,29.5]):return False
 for rr,gg in geo.items():
  if rr==r:continue
  cc,_,qb,qd,qt=gg
  if c[3]==pos[rr][3] and overlap(court,cc,.1):return False
  if c[3]!=pos[rr][3]:
   if any(overlap(court,q+[-.4,-.4,.4,.4])for q in qb[qt]):return False
   if any(overlap(cc,q+[-.4,-.4,.4,.4])for q in pb[tht]):return False
  # Conservative projected metal check, including all NC row terminals.
  dx=np.maximum(np.maximum(pb[:,None,0]-qb[None,:,2],qb[None,:,0]-pb[:,None,2]),0)
  dy=np.maximum(np.maximum(pb[:,None,1]-qb[None,:,3],qb[None,:,1]-pb[:,None,3]),0)
  if np.any((dx*dx+dy*dy<9.35**2-1e-10)&(dom[:,None]!=qd[None,:])):return False
 return True
bad=[r for r,c in pos.items()if not valid(r,c,geo[r])]
assert not bad,('Seed not feasible under declared study constraints',bad)
padloc={k:v for g in geo.values()for k,v in g[1].items()}
def score():
 distances=[float(np.linalg.norm(padloc[a]-padloc[b]))for a,b,w in links]
 # Strongly discourage semiconductor body/courtyard projection under the finished magnetics allocation.
 under=[r for r in semis if overlap(geo[r][0],geo['T1'][0])]
 return sum(d*w for d,(_,_,w)in zip(distances,links))+400*len(under)
bestscore=score();best=dict(pos);baseline=bestscore;rng=random.Random(20261118)
movable=[r for r in refs if r not in fixed];accepted=0
for step in range(24000):
 r=rng.choice(movable);old=pos[r];oldg=geo[r];oldscore=score()
 side=('F'if old[3]=='B'else'B')if rng.random()<.12 else old[3]
 if rng.random()<.15:c=(rng.randrange(-30,31)*.5,rng.randrange(-58,59)*.5,rng.choice((0,90)),side)
 else:c=(old[0]+rng.choice((-2,-1,-.5,.5,1,2)),old[1]+rng.choice((-2,-1,-.5,.5,1,2)),rng.choice((0,90))if rng.random()<.15 else old[2],side)
 if r in semis and overlap(geometry(r,c)[0],geo['T1'][0]):continue
 g=geometry(r,c)
 if not valid(r,c,g):continue
 pos[r]=c;geo[r]=g;padloc.update(g[1]);newscore=score();temp=max(.2,16*(1-step/24000))
 if newscore<oldscore or rng.random()<math.exp(min(0,(oldscore-newscore)/temp)):
  accepted+=1
  if newscore<bestscore:bestscore=newscore;best=dict(pos)
 else:pos[r]=old;geo[r]=oldg;padloc.update(oldg[1])
pos=dict(best)
# Final bounded constructive correction from the separate topology implementer.
# This overrides aggregate-score selection to give U1 an actually adjacent bypass.
local_bias_moves={'U1':(-12,12,90,'F'),'C2':(-12,13.5,0,'B'),'C1':(-2.7,12.2,90,'B'),'Q1':(4.5,12.5,0,'F'),'BR1':(12.2,12.5,0,'F'),'D1':(-2,23.9,0,'B'),'R3':(10,-5,0,'B'),'R9':(-5.5,12.5,90,'F')}
pos.update(local_bias_moves);geo={r:geometry(r,c)for r,c in pos.items()};padloc={k:v for g in geo.values()for k,v in g[1].items()}
assert all(valid(r,c,geo[r])for r,c in pos.items()),'Final local-bypass correction violates study constraints'
def metrics(pp):
 gg={r:geometry(r,c)for r,c in pp.items()};pl={k:v for g in gg.values()for k,v in g[1].items()}
 return {'weighted_search_score':sum(float(np.linalg.norm(pl[a]-pl[b]))*w for a,b,w in links)+400*sum(overlap(gg[r][0],gg['T1'][0])for r in semis),
 'semiconductors_projected_under_T1':sorted(r for r in semis if overlap(gg[r][0],gg['T1'][0])),
 'links':[{'a':a,'b':b,'net':electrical[a.split('.')[0]]['pins'][a.split('.')[1]],'pad_centres_distance_mm':float(np.linalg.norm(pl[a]-pl[b])),'search_weight':w}for a,b,w in links]}
report={'scope':'Unapplied analytical pre-CAD study, no routed conductor/copper or adopted spatial intent. Pad-centre distances are geometric lower bounds, not trace lengths or qualified loops. Weights/9.35mm projected domain reserve/0.5mm edge/0.4mm joint are planning allocations, not supplier or IEC acceptance.',
 'base':'f0216041fc47fef993e24939c6f31727fe409a14','inputs':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest()for p in(P/'assembly-fit-01/packing-diagnostic.json',P/'compact-60/mechanics/native-inventory.json',P/'electrical-integration/proposed-parts.json')},
 'board_study_rectangle_mm':[W,L],'placed_count':31,'total_count':31,'selected_product_PCB':False,'PCB_entry_ready':False,'fixed_during_search_refs':sorted(fixed),'final_local_bias_moves':{rr:list(cc)for rr,cc in local_bias_moves.items()},'final_manual_override_of_search_anchor':['C1'],'iterations':24000,'seed':20261118,'accepted_moves':accepted,
 'baseline':metrics(initial),'candidate':metrics(pos),
 'positions':{r:{'x_mm':c[0],'y_mm':c[1],'angle_deg':c[2],'side':c[3],'courtyard_bbox_mm':geo[r][0].tolist(),'pads':geo[r][2].tolist()}for r,c in pos.items()}}
(D/'layout-proposal.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:report[k]for k in('iterations','accepted_moves','PCB_entry_ready')}));print(json.dumps({'baseline_score':report['baseline']['weighted_search_score'],'candidate_score':report['candidate']['weighted_search_score'],'semiconductors_under_T1':report['candidate']['semiconductors_projected_under_T1']}))

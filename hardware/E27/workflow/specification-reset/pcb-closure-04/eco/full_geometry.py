"""Independent proposed33-part geometry, including changed THT joints and pin map."""
from pathlib import Path
import json,math,itertools
D=Path(__file__).resolve().parent
parts={p['ref']:p for p in json.loads((D/'proposed-parts.json').read_text(encoding='utf-8'))};inv={p['ref']:p for p in json.loads((D/'native-inventory.json').read_text(encoding='utf-8'))['parts']};proposal=json.loads((D/'full-placement-proposal.json').read_text(encoding='utf-8'));pos=proposal['positions'];HW,HH=[x/2 for x in proposal['board_outline_mm']]
assert set(parts)==set(inv)==set(pos)and len(pos)==33
assert all(c['side']in{'F','B'}and c['angle_deg']in{0,90,180,270}for c in pos.values())
def xy(x,y,c):
 if c['side']=='B':y=-y
 a=math.radians(c['angle_deg']);return c['x_mm']+x*math.cos(a)+y*math.sin(a),c['y_mm']+y*math.cos(a)-x*math.sin(a)
def box(b,c):
 pp=[xy(x,y,c)for x in(b[0],b[2])for y in(b[1],b[3])];return[min(x for x,y in pp),min(y for x,y in pp),max(x for x,y in pp),max(y for x,y in pp)]
def overlap(a,b,gap=0):return a[0]<b[2]+gap-1e-9 and b[0]<a[2]+gap-1e-9 and a[1]<b[3]+gap-1e-9 and b[1]<a[3]+gap-1e-9
def distance(a,b):return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
courts={};pads={};centres={}
for ref,c in pos.items():
 courts[ref]=box(inv[ref]['courtyard_bbox_mm'],c)
 if ref=='T1':courts[ref]=[c['x_mm']-15,c['y_mm']-15,c['x_mm']+15,c['y_mm']+15]
 for p in inv[ref]['pads']:
  pin=ref+'.'+p['pin'];x,y=xy(*p['xy_mm'],c);w,h=p['size_mm']
  if c['angle_deg']%180==90:w,h=h,w
  dom='S'if(ref=='T1'and p['pin']in('6','7','8','9','10'))or ref in{'C4','D3','J2','R11','R12'}else'P'
  centres[pin]=(x,y);pads[pin]=dict(ref=ref,number=p['pin'],box=[x-w/2,y-h/2,x+w/2,y+h/2],domain=dom,tht=p['tht'],circle=p.get('circle',False),centre=(x,y),radius=w/2,net=parts[ref]['pins'][p['pin']])
assert len(pads)==81
overruns=[r for r,b in courts.items()if b[0]<-HW-1e-9 or b[2]>HW+1e-9 or b[1]<-HH-1e-9 or b[3]>HH+1e-9]
courtconf=[[a,b]for a,b in itertools.combinations(pos,2)if pos[a]['side']==pos[b]['side']and overlap(courts[a],courts[b],.1)]
joints=[]
for pin,p in pads.items():
 if p['tht']:
  b=p['box'];bb=[b[0]-.4,b[1]-.4,b[2]+.4,b[3]+.4]
  for r,c in pos.items():
   if r!=p['ref']and c['side']!=pos[p['ref']]['side']and overlap(bb,courts[r]):joints.append([pin,r])
semis=[r for r in('U1','Q1','BR1','D1','D2','D3','TVS1')if overlap(courts[r],courts['T1'])]
hv={'AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','BULK_POS','DRAIN','CLAMP','STARTUP_MID'};quiet={'VDD','VS','NTC','CS','DRV','GATE','SENSE','PRIMARY_GND','AUX_RAW','AUX_RECT'};clearance=[];cross=[]
def copper_gap(a,b):
 if a['circle']and b['circle']:return max(0,math.dist(a['centre'],b['centre'])-a['radius']-b['radius'])
 if a['circle']or b['circle']:
  c,r=(a,b)if a['circle']else(b,a);x,y=c['centre'];bb=r['box'];return max(0,math.hypot(max(bb[0]-x,x-bb[2],0),max(bb[1]-y,y-bb[3],0))-c['radius'])
 return distance(a['box'],b['box'])
for (i,a),(j,b)in itertools.combinations(pads.items(),2):
 if a['net']==b['net']and a['net']is not None:continue
 common=a['tht']or b['tht']or pos[a['ref']]['side']==pos[b['ref']]['side'];gap=distance(a['box'],b['box'])if a['domain']!=b['domain']else copper_gap(a,b);limit=10 if a['domain']!=b['domain']else 3 if(a['net']in hv and b['net']in quiet)or(b['net']in hv and a['net']in quiet)else .25
 if common and gap<limit-1e-9:clearance.append(dict(a=i,b=j,gap_mm=gap,limit_mm=limit))
 if not common and limit==3 and gap<3:cross.append(dict(a=i,b=j,gap_mm=gap))
ps=min((distance(a['box'],b['box']),i,j)for i,a in pads.items()for j,b in pads.items()if a['domain']!=b['domain'])
edge=min((min(p['box'][0]+HW,p['box'][1]+HH,HW-p['box'][2],HH-p['box'][3]),pin)for pin,p in pads.items())
assert not(overruns or courtconf or joints or semis or clearance),(overruns,courtconf,joints,semis,clearance)
assert ps[0]>=10-1e-9 and edge[0]>=.5-1e-9,(ps,edge)
links=[('bypassVDD','U1.2','C2.1'),('bypassGND','U1.5','C2.2'),('CS','U1.4','R6.2'),('DRV','U1.3','R7.1'),('gate','R7.2','Q1.1'),('VSupper','U1.6','R4.2'),('VSlower','U1.6','R5.1'),('power_shunt','Q1.3','R9.1'),('sense_shunt','R6.1','R9.1'),('shunt_return','R9.2','C1.2'),('Q1_D1','Q1.2','D1.2'),('D1_TVS1','D1.1','TVS1.1'),('TVS1_C1','TVS1.2','C1.1'),('T1_D1','T1.5','D1.2'),('TVS1_T1','TVS1.2','T1.1')]
metrics={n:math.dist(centres[a],centres[b])for n,a,b in links}
out=dict(parts=33,pads=81,board_outline_mm=[2*HW,2*HH],courtyard_conflicts=courtconf,opposite_THT_joint_conflicts=joints,semis_under_T1=semis,outline_overruns=overruns,all_common_copper_clearance_failures=clearance,crossface_HVquiet_projected_gaps_below3mm=cross,min_PS_mm=ps[0],PS_pair=list(ps[1:]),min_pad_edge_mm=edge[0],edge_pin=edge[1],endpoint_distances_mm=metrics,Q1_clamp_C1_endpoint_chain_mm=sum(metrics[n]for n in('Q1_D1','D1_TVS1','TVS1_C1')),T1_clamp_three_legs_mm=sum(metrics[n]for n in('T1_D1','D1_TVS1','TVS1_T1')),scope='Proposed33-part physical planning model; changed pin map/all new THT joints included. Functional gap is shape-aware for circles and rectangle-conservative for other lands; P/S remains all-layer bounding-box reserve. Native DRC authoritative. No finished forming/insulation, routed-loop, operational/thermal or stage acceptance.')
if __name__=='__main__':print(json.dumps(out,indent=2))

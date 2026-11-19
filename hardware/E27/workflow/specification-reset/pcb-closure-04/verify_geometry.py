"""Independent scalar source geometry and saved-proposal constraints; no native writer."""
from pathlib import Path
import json,math,itertools
D=Path(__file__).resolve().parent;P=D.parent
proposal=json.loads((D/'placement-proposal.json').read_text(encoding='utf-8'));pos=proposal['positions'];HALF_W,HALF_H=[v/2 for v in proposal.get('board_outline_mm',[32,60])]
parts={p['ref']:p for p in json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'))['parts']}
electrical={p['ref']:p for p in json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'))}
baseline=json.loads((P/'pcb-clamp-03/placement-proposal.json').read_text(encoding='utf-8'))['positions']
assert set(pos)==set(parts)==set(electrical)and len(pos)==31
def xy(x,y,c):
 if c['side']=='B':y=-y
 a=math.radians(c['angle_deg']);return(x*math.cos(a)+y*math.sin(a)+c['x_mm'],y*math.cos(a)-x*math.sin(a)+c['y_mm'])
def box(bb,c):
 ps=[xy(x,y,c)for x in(bb[0],bb[2])for y in(bb[1],bb[3])];return[min(x for x,y in ps),min(y for x,y in ps),max(x for x,y in ps),max(y for x,y in ps)]
def rect_overlap(a,b,gap=0):return a[0]<b[2]+gap-1e-9 and b[0]<a[2]+gap-1e-9 and a[1]<b[3]+gap-1e-9 and b[1]<a[3]+gap-1e-9
def distance(a,b):return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
def extract(pp):
 courts={};pads={};centres={}
 for ref,c in pp.items():
  p=parts[ref];courts[ref]=box(p['courtyard_bbox_mm'],c)
  if ref=='T1':courts[ref]=[c['x_mm']-15,c['y_mm']-15,c['x_mm']+15,c['y_mm']+15]
  for pad in p['pads']:
   x,y=xy(*pad['xy_mm'],c);w,h=pad['size_mm']
   if c['angle_deg']%180==90:w,h=h,w
   pin=ref+'.'+pad['pin'];dom='S'if(ref=='T1'and pad['pin']in('6','7','8','9','10'))or ref in{'C4','D3','J2','R11','R12'}else'P'
   pads[pin]={'ref':ref,'pin':pad['pin'],'box':[x-w/2,y-h/2,x+w/2,y+h/2],'tht':pad['tht'],'domain':dom,'net':electrical[ref]['pins'][pad['pin']]};centres[pin]=(x,y)
 return courts,pads,centres
courts,pads,centres=extract(pos);_,oldpads,oldcentres=extract(baseline)
assert len(pads)==79
overruns=[r for r,b in courts.items()if b[0]<-HALF_W-1e-9 or b[1]<-HALF_H-1e-9 or b[2]>HALF_W+1e-9 or b[3]>HALF_H+1e-9]
conflicts=[[a,b]for a,b in itertools.combinations(pos,2)if pos[a]['side']==pos[b]['side']and rect_overlap(courts[a],courts[b],.1)]
joint=[]
for pin,p in pads.items():
 if not p['tht']:continue
 b=p['box'];bb=[b[0]-.4,b[1]-.4,b[2]+.4,b[3]+.4]
 for r,c in pos.items():
  if r!=p['ref']and c['side']!=pos[p['ref']]['side']and rect_overlap(bb,courts[r]):joint.append([pin,r])
semis=[r for r in('U1','BR1','Q1','D1','D2','D3','TVS1')if rect_overlap(courts[r],courts['T1'])]
ps=min((distance(a['box'],b['box']),i,j)for i,a in pads.items()for j,b in pads.items()if a['domain']!=b['domain'])
edge=min((min(p['box'][0]+HALF_W,p['box'][1]+HALF_H,HALF_W-p['box'][2],HALF_H-p['box'][3]),pin)for pin,p in pads.items())
hv={'AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','BULK_POS','DRAIN','CLAMP'};quiet={'VDD','VS','NTC','CS','DRV','GATE','SENSE','PRIMARY_GND','AUX_RAW','AUX_RECT'}
inter=[];fixed=[];opposite=[]
for (i,a),(j,b)in itertools.combinations(pads.items(),2):
 if not((a['net']in hv and b['net']in quiet)or(b['net']in hv and a['net']in quiet)):continue
 dd=distance(a['box'],b['box'])
 if dd<3-1e-9:
  item={'a':i,'b':j,'distance_mm':dd}
  common_copper=a['tht']or b['tht']or pos[a['ref']]['side']==pos[b['ref']]['side']
  if not common_copper:opposite.append(item)
  else:(fixed if a['ref']==b['ref']else inter).append(item)
assert not(overruns or conflicts or joint or semis or inter),(overruns,conflicts,joint,semis,inter)
assert ps[0]>=10-1e-9 and edge[0]>=.5-1e-9
links=[('bypass_VDD','U1.1','C2.1'),('bypass_GND','U1.4','C2.2'),('VS_upper','U1.2','R4.2'),('VS_lower','U1.2','R5.1'),('CS','U1.5','R6.2'),('sense_shunt','R6.1','R9.1'),('DRV','U1.6','R7.1'),('gate','R7.2','Q1.1'),('power_shunt','Q1.3','R9.1'),('shunt_return','R9.2','C1.2'),('drain','T1.5','Q1.2'),('clamp_leg1','T1.5','D1.2'),('clamp_leg2','D1.1','TVS1.1'),('clamp_leg3','TVS1.2','T1.1'),('Q1_clamp_feed','Q1.2','D1.2'),('clamp_bulk_return','TVS1.2','C1.1')]
metrics=[{'name':n,'a':a,'b':b,'baseline_pad_centre_distance_mm':math.dist(oldcentres[a],oldcentres[b]),'candidate_pad_centre_distance_mm':math.dist(centres[a],centres[b])}for n,a,b in links]
clamp_names={'clamp_leg1','clamp_leg2','clamp_leg3'}
clampold=sum(v['baseline_pad_centre_distance_mm']for v in metrics if v['name']in clamp_names);clampnew=sum(v['candidate_pad_centre_distance_mm']for v in metrics if v['name']in clamp_names)
out={'assigned':31,'physical_pads':79,'same_face_courtyard_plus_0p1mm_conflicts':conflicts,'opposite_face_THT_plus_0p4mm_conflicts':joint,'courtyard_or_T1_allocation_overruns':overruns,'semiconductor_courtyards_under_T1':semis,'min_PS_bbox_mm':ps[0],'PS_pair':list(ps[1:]),'min_pad_edge_mm':edge[0],'edge_pin':edge[1],'intercomponent_same_copper_3mm_conflicts':inter,'opposite_face_HV_quiet_projected_gaps_below3mm_not_DRC_air_clearance':opposite,'fixed_package_unique_3mm_pairs':fixed,'pad_centre_links':metrics,'clamp_external_legs':{'baseline_mm':clampold,'candidate_mm':clampnew,'increase_percent':100*(clampnew/clampold-1),'accepted_as_routing':False},'scope':'Independent scalar planning model. Native DRC is authoritative.3mmnative clearances compare common copper layers; opposite-face SMD projections require separate solid-dielectric/capacitive-coupling review and are not qualified by this check. P/S all-layer projection includes NC. No routed loop, qualified tolerance/process, thermal/NTC coupling, waveform or lighting-insulation pass.','rules_relaxed':False,'stage_approved':False}
print(json.dumps(out,indent=2))

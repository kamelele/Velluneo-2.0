"""Independent scalar geometry/net checks on the saved preparation proposal."""
from pathlib import Path
import json,math,itertools,hashlib
D=Path(__file__).resolve().parent;P=D.parent
r=json.loads((D/'layout-proposal.json').read_text(encoding='utf-8'));pos=r['positions']
inv=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'));parts={p['ref']:p for p in inv['parts']}
ep={p['ref']:p for p in json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'))}
assert set(pos)==set(parts)==set(ep) and len(pos)==31
def transformed(x,y,c):
 if c['side']=='B':y=-y
 angle=math.radians(c['angle_deg']);return(x*math.cos(angle)+y*math.sin(angle)+c['x_mm'],-x*math.sin(angle)+y*math.cos(angle)+c['y_mm'])
def overlap(a,b):return a[0]<b[2]-1e-10 and b[0]<a[2]-1e-10 and a[1]<b[3]-1e-10 and b[1]<a[3]-1e-10
def dist(a,b):return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
pads={};loc={};courts={};mismatch=[]
for ref,c in pos.items():
 p=parts[ref];bb=p['courtyard_bbox_mm'];xy=[transformed(x,y,c)for x in(bb[0],bb[2])for y in(bb[1],bb[3])]
 court=[min(a for a,b in xy),min(b for a,b in xy),max(a for a,b in xy),max(b for a,b in xy)]
 if ref=='T1':court=[c['x_mm']-15,c['y_mm']-15,c['x_mm']+15,c['y_mm']+15]
 assert max(abs(a-b)for a,b in zip(court,c['courtyard_bbox_mm']))<1e-6
 courts[ref]=court
 for pp,saved in zip(p['pads'],c['pads']):
  x,y=transformed(*pp['xy_mm'],c);w,h=pp['size_mm']
  if c['angle_deg']in(90,270):w,h=h,w
  b=[x-w/2,y-h/2,x+w/2,y+h/2];key=ref+'.'+pp['pin'];loc[key]=(x,y)
  assert max(abs(a-bb)for a,bb in zip(b,saved))<1e-6
  domain='S'if(ref=='T1'and pp['pin']in('6','7','8','9','10'))or ref in{'D3','C4','J2','R11','R12'}else'P'
  pads[key]={'box':b,'domain':domain,'tht':pp['tht'],'ref':ref}
assert len(pads)==79
collisions=[[a,b]for a,b in itertools.combinations(pos,2)if pos[a]['side']==pos[b]['side']and overlap(courts[a],courts[b])]
joint=[]
for pin,p in pads.items():
 if not p['tht']:continue
 b=p['box'];expanded=[b[0]-.4,b[1]-.4,b[2]+.4,b[3]+.4]
 for ref,c in pos.items():
  if ref!=p['ref']and c['side']!=pos[p['ref']]['side']and overlap(expanded,courts[ref]):joint.append([pin,ref])
minPS=min((dist(a['box'],b['box']),i,j)for i,a in pads.items()for j,b in pads.items()if a['domain']!=b['domain'])
edge=min((min(p['box'][0]+16,p['box'][1]+30,16-p['box'][2],30-p['box'][3]),pin)for pin,p in pads.items())
overruns=[ref for ref,b in courts.items()if b[0]<-16 or b[2]>16 or b[1]<-30 or b[3]>30]
under=[ref for ref in('U1','Q1','BR1','D1','D2','D3','TVS1')if overlap(courts[ref],courts['T1'])]
assert not(collisions or joint or overruns or under)
assert minPS[0]>=9.35-1e-9 and edge[0]>=.5
for e in r['candidate']['links']:
 a,ap=e['a'].split('.');b,bp=e['b'].split('.');assert ep[a]['pins'][ap]==ep[b]['pins'][bp]==e['net']
 assert abs(math.dist(loc[e['a']],loc[e['b']])-e['pad_centres_distance_mm'])<1e-9
out={'checked_components':31,'checked_pads':79,'critical_same_net_edges':len(r['candidate']['links']),'same_face_courtyard_conflicts':collisions,'opposite_face_THT_pad_plus_0p4mm_conflicts':joint,'outline_overruns':overruns,'semiconductor_courts_under_T1':under,'min_projected_PS_bbox_mm':minPS[0],'PS_pair':list(minPS[1:]),'min_pad_edge_mm':edge[0],'edge_pad':edge[1],
 'scope':'Independent geometric checks of the saved proposal only. No actual traces, via holes, solder-process qualification, functional clearance under high-voltage parts, normative isolation or finished transformer proof.',
 'remaining_topology':{'bypass_distance_not_qualified':True,'VS_CS_routing_not_qualified':True,'quiet_ground_Kelvin_not_routed':True,'RT1_thermal_attachment_not_qualified':True},'PCB_entry_ready':False}
print(json.dumps(out,indent=2))

"""Independent saved-board/intent parity and native geometry checks; never release approval."""
from pathlib import Path
import pcbnew,json,math,hashlib,xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;P=D.parent;B='Velluneo_specification_reset'
board=pcbnew.LoadBoard(str(D/(B+'.kicad_pcb')));assert board
parts={p['ref']:p for p in json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'))};layout=json.loads((P/'driver-entry-02/layout-proposal.json').read_text(encoding='utf-8'))
inventory={p['ref']:p for p in json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'))['parts']}
comps={x.attrib['ref']:x for x in ET.parse(D/'checks/current-netlist.xml').getroot().findall('./components/comp')}
footprints={f.GetReference():f for f in board.GetFootprints()};assert set(footprints)==set(parts)==set(comps)and len(footprints)==31
expected={n:{(r,p)for r,c in parts.items()for p,nn in c['pins'].items()if nn==n}for n in{n for c in parts.values()for n in c['pins'].values()if n is not None}}
actual={};observedpads=[];maximum=0;NC=[]
for ref,f in footprints.items():
 assert f.GetValue()==comps[ref].findtext('value')
 assert f.GetFieldText('MPN')==parts[ref]['mpn']
 assert f.GetFPID().GetLibNickname().c_str()=='Velluneo_Driver'
 c=layout['positions'][ref];assert bool(f.IsFlipped())==(c['side']=='B')
 assert {p.GetNumber()for p in f.Pads()}==set(parts[ref]['pins'])
 expectedboxes={pp['pin']:bb for pp,bb in zip(inventory[ref]['pads'],c['pads'])}
 for pad in f.Pads():
  pin=pad.GetNumber();name=pad.GetNetname();actual.setdefault(name,set()).add((ref,pin))
  expectednet=parts[ref]['pins'][pin]
  if expectednet is None:NC.append((ref,pin,name))
  x=pcbnew.ToMM(pad.GetPosition().x)-100;y=pcbnew.ToMM(pad.GetPosition().y)-100
  w,h=pcbnew.ToMM(pad.GetSize().x),pcbnew.ToMM(pad.GetSize().y)
  if abs(pad.GetOrientation().AsDegrees()%180-90)<1e-6:w,h=h,w
  bbox=[x-w/2,y-h/2,x+w/2,y+h/2];delta=max(abs(a-b)for a,b in zip(bbox,expectedboxes[pin]));maximum=max(maximum,delta);assert delta<2e-6,(ref,pin,delta)
  domain='S'if(ref=='T1'and pin in('6','7','8','9','10'))or ref in{'C4','D3','J2','R11','R12'}else'P'
  observedpads.append((ref,pin,domain,bbox))
 for model in f.Models():assert model.m_Filename.startswith('${KIPRJMOD}/')and(D/model.m_Filename.removeprefix('${KIPRJMOD}/')).exists()
aliases={}
for name,pins in expected.items():
 matched=[n for n,ps in actual.items()if ps==pins];assert len(matched)==1,(name,matched);aliases[name]=matched[0]
assert len(NC)==4 and all(len(actual[n])==1 and n.startswith('unconnected-(T1-')for r,p,n in NC)
assert sum(map(len,actual.values()))==79 and len(actual)==26
edges=[s for s in board.GetDrawings()if s.GetLayer()==pcbnew.Edge_Cuts];assert len(edges)==4
xy=[(pcbnew.ToMM(p.x),pcbnew.ToMM(p.y))for s in edges for p in(s.GetStart(),s.GetEnd())]
dimensions=[max(x for x,y in xy)-min(x for x,y in xy),max(y for x,y in xy)-min(y for x,y in xy)];assert dimensions==[32,60]
def distance(a,b):return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
minimum=min((distance(a[3],b[3]),a[0]+'.'+a[1],b[0]+'.'+b[1])for a in observedpads for b in observedpads if a[2]!=b[2])
assert minimum[0]>=10
assert len(list(board.GetTracks()))==0
zones=list(board.Zones());assert len(zones)==1 and zones[0].GetIsRuleArea()and zones[0].GetDoNotAllowPads()and zones[0].GetDoNotAllowTracks()and zones[0].GetDoNotAllowVias()and zones[0].GetDoNotAllowZoneFills()
report={'native_pcbnew':pcbnew.Version(),'saved_board_reloaded':True,'components':31,'physical_pads':79,'functional_nets':22,'native_single_pad_NC_nets':4,'logical_to_native_netnames':aliases,'complete_physical_membership_matches_independent_parts':True,'source_MPN_values_present':True,'all_model_paths_resolve':True,'maximum_saved_pad_bbox_delta_mm':maximum,'board_outline_mm':dimensions,'native_copper_layers':board.GetCopperLayerCount(),'tracks_and_vias':len(list(board.GetTracks())),'rule_area_count':len(zones),'min_projected_domain_pad_bbox_mm':minimum[0],'pair':list(minimum[1:]),'finished_metal_budget_with_0p35mm_each':minimum[0]-.7,'scope':'Actual saved board parity and geometry, including NC terminals. No routed connection, finished transformer, manufactured process, functional HV spacing, lighting-standard compliance or stage acceptance is established.','stage_approved':False,'ready_to_manufacture':False}
print(json.dumps(report,indent=2))

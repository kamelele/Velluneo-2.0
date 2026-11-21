"""Independent saved native ECO board/netlist/proposal parity, not physical qualification."""
from pathlib import Path
import json,math,hashlib,xml.etree.ElementTree as ET,pcbnew
import full_geometry as geom
D=Path(__file__).resolve().parent;B='Velluneo_specification_reset';board=pcbnew.LoadBoard(str(D/(B+'.kicad_pcb')));assert board
parts=geom.parts;pos=geom.pos;inv=geom.inv;fps={f.GetReference():f for f in board.GetFootprints()};assert set(fps)==set(parts)and len(fps)==33
intent=json.loads((D/'proposed-intent.json').read_text(encoding='utf-8'));assert intent['approval']is None
selection=json.loads((D.parent/'owner-decision.json').read_text(encoding='utf-8'));assert selection['approved_intent_digest']==intent['proposal_digest']and selection['decision']=='approved_as_basis_for_further_work'
assert hashlib.sha256(json.dumps({k:v for k,v in intent.items()if k!='proposal_digest'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()==intent['proposal_digest']
assert {p['ref']:{k:p[k]for k in('ref','mpn','pins')}for p in intent['components']}=={r:{k:p[k]for k in('ref','mpn','pins')}for r,p in parts.items()}
comps={c.attrib['ref']:c for c in ET.parse(D/'checks/proposed-netlist.xml').getroot().findall('./components/comp')};expected={n:{(r,k)for r,p in parts.items()for k,nn in p['pins'].items()if nn==n}for n in{n for p in parts.values()for n in p['pins'].values()if n is not None}};actual={};nc=[];maxdelta=0
for ref,f in fps.items():
 lib,name=inv[ref]['footprint'].split(':');libpath=D/('Velluneo_ECO04.pretty'if lib=='Velluneo_ECO04'else'libraries/Velluneo_Driver.pretty');assert hashlib.sha256((libpath/(name+'.kicad_mod')).read_bytes()).hexdigest()==inv[ref]['source_sha256']
 assert f.GetValue()==comps[ref].findtext('value')and f.GetFieldText('MPN')==parts[ref]['mpn'];assert f.Reference().IsVisible();assert bool(f.IsFlipped())==(pos[ref]['side']=='B');assert {p.GetNumber()for p in f.Pads()}==set(parts[ref]['pins'])
 assert f.GetFPID().GetLibNickname().c_str()+':'+f.GetFPID().GetLibItemName().c_str()==comps[ref].findtext('footprint'),ref
 for pad in f.Pads():
  pin=pad.GetNumber();name=pad.GetNetname();actual.setdefault(name,set()).add((ref,pin));p=geom.pads[ref+'.'+pin];x=pcbnew.ToMM(pad.GetPosition().x)-100;y=pcbnew.ToMM(pad.GetPosition().y)-100;maxdelta=max(maxdelta,abs(x-p['centre'][0]),abs(y-p['centre'][1]));assert maxdelta<2e-6,(ref,pin,maxdelta)
  source=next(q for q in inv[ref]['pads']if q['pin']==pin);assert abs(pcbnew.ToMM(pad.GetSize().x)-source['size_mm'][0])<2e-6 and abs(pcbnew.ToMM(pad.GetSize().y)-source['size_mm'][1])<2e-6
  assert int(pad.GetAttribute())==source['attribute']and int(pad.GetShape())==source['shape']and int(pad.GetDrillShape())==source['drill_shape']
  assert max(abs(a-b)for a,b in zip([pcbnew.ToMM(pad.GetDrillSize().x),pcbnew.ToMM(pad.GetDrillSize().y)],source['drill_xy_mm']))<2e-6
  expectedlayers=set(source['local_layers'])
  if pos[ref]['side']=='B':
   opposite={int(pcbnew.F_Cu):int(pcbnew.B_Cu),int(pcbnew.B_Cu):int(pcbnew.F_Cu),int(pcbnew.F_Paste):int(pcbnew.B_Paste),int(pcbnew.B_Paste):int(pcbnew.F_Paste),int(pcbnew.F_Mask):int(pcbnew.B_Mask),int(pcbnew.B_Mask):int(pcbnew.F_Mask)};expectedlayers={opposite.get(n,n)for n in expectedlayers}
  assert set(int(n)for n in pad.GetLayerSet().Seq())==expectedlayers,(ref,pin,'layers')
  if parts[ref]['pins'][pin]is None:nc.append((ref,pin,name))
 for model in f.Models():assert model.m_Filename.startswith('${KIPRJMOD}/')and(D/model.m_Filename.removeprefix('${KIPRJMOD}/')).exists()
for n,pins in expected.items():assert sum(p==pins for p in actual.values())==1,n
assert {n['name']:{(p['ref'],p['pin'])for p in n['pins']}for n in intent['nets']}==expected
assert {(p['ref'],p['pin'])for p in intent['no_connect']}=={(r,k)for r,k,n in nc}
assert len(actual)==27 and sum(map(len,actual.values()))==81 and len(nc)==4 and all(len(actual[n])==1 for r,k,n in nc)
edges=[e for e in board.GetDrawings()if e.GetLayer()==pcbnew.Edge_Cuts];assert len(edges)==4;coords=[(pcbnew.ToMM(p.x),pcbnew.ToMM(p.y))for e in edges for p in(e.GetStart(),e.GetEnd())];dims=[max(x for x,y in coords)-min(x for x,y in coords),max(y for x,y in coords)-min(y for x,y in coords)];assert dims==[2*geom.HW,2*geom.HH]
assert len(list(board.GetTracks()))==0;zones=list(board.Zones());assert len(zones)==1 and zones[0].GetIsRuleArea()and zones[0].GetDoNotAllowPads()and zones[0].GetDoNotAllowTracks()and zones[0].GetDoNotAllowVias()and zones[0].GetDoNotAllowZoneFills()
intent=json.loads((D/'proposed-intent.json').read_text(encoding='utf-8'));assert intent['approval']is None
selection=json.loads((D.parent/'owner-decision.json').read_text(encoding='utf-8'));assert selection['approved_intent_digest']==intent['proposal_digest']and selection['decision']=='approved_as_basis_for_further_work'
print(json.dumps(dict(native_pcbnew=pcbnew.Version(),saved_reloaded=True,components=33,physical_pads=81,functional_nets=23,NC_singletons=4,all_native_memberships_match_proposed_intent=True,all_MPN_values_footprint_assignments_match=True,all_model_paths_resolve=True,all_references_visible=True,max_saved_pad_centre_delta_mm=maxdelta,board_outline_mm=dims,tracks_vias=0,keepout_count=1,proposed_intent_digest=intent['proposal_digest'],basis_owner_selected=True,technical_intent_stage_approved=False,process_qualified=False,routing_accepted=False,scope='Saved complete proposedECOgeometry/membership consistency only; not operating/insulation/process or human approval.'),indent=2))

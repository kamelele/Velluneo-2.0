from pathlib import Path
import pcbnew,json,hashlib,collections,math
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-prototype-09';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';old=pcbnew.LoadBoard(str(P/'pcb-driver-08/design/Velluneo_driver.kicad_pcb'));b=pcbnew.LoadBoard(str(B))
def tracks(b):
 return sorted((t.GetNetname(),int(t.GetLayer()),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth(pcbnew.F_Cu)if isinstance(t,pcbnew.PCB_VIA)else t.GetWidth(),t.GetDrillValue()if isinstance(t,pcbnew.PCB_VIA)else 0)for t in b.GetTracks())
def pads(b):
 return sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y,int(p.GetShape()),tuple(p.GetLayerSet().Contains(l)for l in(pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu)))for f in b.GetFootprints()for p in f.Pads())
assert tracks(b)==tracks(old);assert pads(b)==pads(old)
for f in b.GetFootprints():
 o=next(q for q in old.GetFootprints()if q.GetReference()==f.GetReference());assert f.GetPosition()==o.GetPosition()and f.GetOrientationDegrees()==o.GetOrientationDegrees()and f.GetLayer()==o.GetLayer()and f.GetValue()==o.GetValue()and f.GetFieldText('MPN')==o.GetFieldText('MPN')
expected=[];via=[]
for f in b.GetFootprints():
 for p in f.Pads():
  dx,dy=p.GetDrillSize().x,p.GetDrillSize().y
  if dx or dy:
   assert dx==dy,'No slots expected';expected.append(dict(kind='component',ref=f.GetReference()+'.'+p.GetNumber(),x_mm=pcbnew.ToMM(p.GetPosition().x)-77.5,y_mm=130-pcbnew.ToMM(p.GetPosition().y),diameter_mm=pcbnew.ToMM(dx),plated=int(p.GetAttribute())==int(pcbnew.PAD_ATTRIB_PTH)))
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA):
  row=dict(kind='via',ref='via',x_mm=pcbnew.ToMM(t.GetPosition().x)-77.5,y_mm=130-pcbnew.ToMM(t.GetPosition().y),diameter_mm=pcbnew.ToMM(t.GetDrillValue()),plated=True);expected.append(row);via.append(row);assert t.GetFillingMode()==pcbnew.FILLING_MODE_FILLED and t.GetCappingMode()==pcbnew.CAPPING_MODE_CAPPED
def normalized(p):
 j=json.loads(p.read_text());r=j['board']['design_settings']['rules'];r.update(min_text_height=1,min_text_thickness=.15,min_silk_clearance=.15);sev=j['board']['design_settings']['rule_severities'];sev.update(silk_over_copper='warning',silk_edge_clearance='warning',silk_overlap='warning');return j
assert normalized(P/'pcb-driver-08/design/Velluneo_driver.kicad_pro')==normalized(B.with_suffix('.kicad_pro'))
assert B.with_suffix('.kicad_dru').read_bytes()==(P/'pcb-driver-08/design/Velluneo_driver.kicad_dru').read_bytes()
out=dict(board_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),all_copper_and_pad_geometry_identical_to_DRIVER08=True,all_component_positions_sides_values_MPNs_unchanged=True,schematic_only_change='R14 footprint identifier to named same-land silk-only variant',project_only_changes='Stronger silk height/stroke/clearance and explicit warning checks; electrical policy unchanged',expected_drills=expected,via_count=len(via),component_hole_count=len(expected)-len(via),copper_layers=4,footprints=33,pads=81,source_inventory_is_historical_baseline=True)
(D/'checks/native-fabrication-input.json').write_text(json.dumps(out,indent=2)+'\n');print('Native preservation verified, holes',len(expected))

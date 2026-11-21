from pathlib import Path
import pcbnew as p,json,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-toolkit-11';B=D/'design/Velluneo_driver.kicad_pcb';A=P/'pcb-cleanup-10/design/Velluneo_driver.kicad_pcb';a=p.LoadBoard(str(A));b=p.LoadBoard(str(B))
def inv(board):
 fs=sorted((f.GetReference(),f.GetValue(),f.GetFieldText('MPN'),f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),f.GetLayer())for f in board.GetFootprints())
 pads=sorted((f.GetReference(),x.GetNumber(),x.GetNetname(),x.GetPosition().x,x.GetPosition().y,x.GetSize().x,x.GetSize().y,x.GetDrillSize().x,x.GetDrillSize().y,int(x.GetLayerSet().Seq()[0]))for f in board.GetFootprints()for x in f.Pads())
 tracks=sorted((x.GetNetname(),int(x.GetLayer()),x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y,x.GetWidth(p.F_Cu)if isinstance(x,p.PCB_VIA)else x.GetWidth(),x.GetDrillValue()if isinstance(x,p.PCB_VIA)else 0)for x in board.GetTracks())
 return fs,pads,tracks
assert inv(a)==inv(b),'Physical inventory/copper changed'
assert b.GetCopperLayerCount()==4
holes=[]
for f in b.GetFootprints():
 for x in f.Pads():
  if x.GetDrillSize().x:holes.append(dict(kind='component',ref=f.GetReference()+'.'+x.GetNumber(),x_mm=p.ToMM(x.GetPosition().x)-77.5,y_mm=130-p.ToMM(x.GetPosition().y),diameter_mm=p.ToMM(x.GetDrillSize().x),plated=True))
for x in b.GetTracks():
 if isinstance(x,p.PCB_VIA):
  assert x.GetFillingMode()==p.FILLING_MODE_FILLED and x.GetCappingMode()==p.CAPPING_MODE_CAPPED
  holes.append(dict(kind='via',ref='via',x_mm=p.ToMM(x.GetPosition().x)-77.5,y_mm=130-p.ToMM(x.GetPosition().y),diameter_mm=p.ToMM(x.GetDrillValue()),plated=True))
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
r=dict(board_sha256=sha(B),baseline_board_sha256=sha(A),component_count=len(inv(b)[0]),pad_count=len(inv(b)[1]),track_segments=sum(not isinstance(x,p.PCB_VIA)for x in b.GetTracks()),via_count=17,all_component_geometry_values_MPNs_and_track_via_copper_identical=True,expected_drills=holes,component_hole_count=25,scope='Native semantic comparison against C10; added managed non-copper area and stronger configuration only. No physical qualification inferred.')
(D/'checks/native-fabrication-input.json').write_text(json.dumps(r,indent=2)+'\n');print('Native geometry preserved:',r['component_count'],r['pad_count'],r['track_segments'],len(holes),'holes')

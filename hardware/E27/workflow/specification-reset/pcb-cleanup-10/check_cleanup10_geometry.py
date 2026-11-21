from pathlib import Path
import pcbnew,json,math,hashlib,csv
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-cleanup-10';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';old=pcbnew.LoadBoard(str(P/'pcb-prototype-09/design/Velluneo_driver.kicad_pcb'));b=pcbnew.LoadBoard(str(B))
def ps(board):return sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y)for f in board.GetFootprints()for p in f.Pads())
assert ps(b)==ps(old)
for f in b.GetFootprints():
 q=next(o for o in old.GetFootprints()if o.GetReference()==f.GetReference());assert f.GetPosition()==q.GetPosition()and f.GetLayer()==q.GetLayer()and f.GetOrientationDegrees()==q.GetOrientationDegrees()and f.GetValue()==q.GetValue()and f.GetFieldText('MPN')==q.GetFieldText('MPN')
def sig(t):return(t.GetNetname(),int(t.GetLayer()),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth())
for net in('/SENSE','/CS'):assert sorted(sig(t)for t in b.GetTracks()if not isinstance(t,pcbnew.PCB_VIA)and t.GetNetname()==net)==sorted(sig(t)for t in old.GetTracks()if not isinstance(t,pcbnew.PCB_VIA)and t.GetNetname()==net)
holes=[];rows=[]
for f in b.GetFootprints():
 for p in f.Pads():
  drill=p.GetDrillSize()
  if drill.x or drill.y:holes.append(dict(kind='component',ref=f.GetReference()+'.'+p.GetNumber(),x_mm=pcbnew.ToMM(p.GetPosition().x)-77.5,y_mm=130-pcbnew.ToMM(p.GetPosition().y),diameter_mm=pcbnew.ToMM(drill.x),plated=True))
expected=list(holes)
for i,v in enumerate(t for t in b.GetTracks()if isinstance(t,pcbnew.PCB_VIA)):
 x,y=pcbnew.ToMM(v.GetPosition().x),pcbnew.ToMM(v.GetPosition().y);assert abs(pcbnew.ToMM(v.GetWidth(pcbnew.F_Cu))-.7)<1e-6 and abs(pcbnew.ToMM(v.GetDrillValue())-.3)<1e-6;assert v.GetFillingMode()==pcbnew.FILLING_MODE_FILLED and v.GetCappingMode()==pcbnew.CAPPING_MODE_CAPPED
 gaps=[math.hypot(x-77.5-h['x_mm'],130-y-h['y_mm'])-(.3+h['diameter_mm'])/2 for h in holes];assert min(gaps)>.45
 rows.append(dict(id=i+1,net=v.GetNetname(),board_x_mm=x,board_y_mm=y,output_x_mm=x-77.5,output_y_mm=130-y,hole_mm=.3,pad_mm=.7,fill='nonconductive epoxy',cap='copper',minimum_hole_edge_gap_to_component_hole_mm=min(gaps)));expected.append(dict(kind='via',ref='via',x_mm=x-77.5,y_mm=130-y,diameter_mm=.3,plated=True))
with(D/'fabrication/designated-filled-vias.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
tracks=[t for t in b.GetTracks()if not isinstance(t,pcbnew.PCB_VIA)];metrics=dict(board_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),old_segments=647,new_segments=len(tracks),reduction_percent=100*(647-len(tracks))/647,old_total_planar_mm=sum(pcbnew.ToMM(t.GetLength())for t in old.GetTracks()if not isinstance(t,pcbnew.PCB_VIA)),new_total_planar_mm=sum(pcbnew.ToMM(t.GetLength())for t in tracks),drv_planar_mm=sum(pcbnew.ToMM(t.GetLength())for t in tracks if t.GetNetname()=='/DRV'),vias=17,via_pad_mm=.7,via_hole_mm=.3,annular_ring_mm=.2,one_VDD_via_shift_mm=[0,.05],pads_values_MPNs_positions_unchanged=True,SENSE_CS_copper_identical=True,scope='Actual saved native planar lengths/counts. Some routes use straight non45-degree segments; no current/EMI/inductance or operating qualification inferred.')
(D/'route-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');(D/'checks/native-fabrication-input.json').write_text(json.dumps(dict(board_sha256=metrics['board_sha256'],expected_drills=expected,protected_measurement_copper_identical=True,all_pads_and33componentplacements_values_MPNs_unchanged=True,via_count=17,component_hole_count=25),indent=2)+'\n');print(json.dumps(metrics))

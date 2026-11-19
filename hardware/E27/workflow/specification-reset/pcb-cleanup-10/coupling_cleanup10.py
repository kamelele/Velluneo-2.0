from pathlib import Path
import pcbnew,math,json,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-cleanup-10';B=D/'design/Velluneo_driver.kicad_pcb';b=pcbnew.LoadBoard(str(B));seed=pcbnew.LoadBoard(str(P/'pcb-route-07/studies/sense/routing-seed.kicad_pcb'))
def xy(p):return(pcbnew.ToMM(p.x),pcbnew.ToMM(p.y))
def pointseg(p,a,z):
 dx,dy=z[0]-a[0],z[1]-a[1];u=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy or 1)));return math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy)
hv={'Net-(F1-Pad1)','Net-(BR1-AC-Pad2)','Net-(F1-Pad2)','Net-(BR1-AC-Pad4)','/BULK_POS','/DRAIN','Net-(D1-K)','/STARTUP_MID'};rows=[]
for net,count in(('/SENSE',6),('/CS',1)):
 measure=[t for t in seed.GetTracks()if t.GetNetname()==net];assert len(measure)==count;gaps=[]
 for s in measure:
  a,z=xy(s.GetStart()),xy(s.GetEnd());sw=pcbnew.ToMM(s.GetWidth());n=max(1,math.ceil(math.dist(a,z)/.005))
  for t in b.GetTracks():
   if t.GetNetname()not in hv:continue
   if isinstance(t,pcbnew.PCB_VIA):gaps.append(pointseg(xy(t.GetPosition()),a,z)-(sw+pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)))/2);continue
   if t.GetLayer()==s.GetLayer():continue
   ta,tz=xy(t.GetStart()),xy(t.GetEnd());gaps.append(min(pointseg((a[0]+(z[0]-a[0])*k/n,a[1]+(z[1]-a[1])*k/n),ta,tz)for k in range(n+1))-(sw+pcbnew.ToMM(t.GetWidth()))/2)
 minimum=min(gaps);assert minimum>=3,(net,minimum);rows.append(dict(net=net,original_segments=count,original_length_mm=sum(pcbnew.ToMM(t.GetLength())for t in measure),minimum_projected_HV_track_or_via_edge_gap_mm=minimum))
(D/'checks/measurement-coupling.json').write_text(json.dumps(dict(board_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),screens=rows,sampling_mm=.005,scope='Dedicated unchanged original measurement conductors versus different-layer HV tracks and all HV vias. Geometric sampling only; not EMI/error/insulation qualification.'),indent=2)+'\n');print(rows)

"""Native negative fixtures and read-only study export; product board untouched."""
from pathlib import Path
import pcbnew,json,shutil,hashlib,math
D=Path(__file__).resolve().parent;E=D/'design';S=D/'studies/sense';B='Velluneo_sense_exploration';N=D/'studies/.work/sense-negative';N.mkdir(parents=True,exist_ok=True)
b=pcbnew.LoadBoard(str(S/(B+'.kicad_pcb')));positive=[]
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA):continue
 positive.append(dict(net=t.GetNetname(),layer='F'if t.GetLayer()==pcbnew.F_Cu else'B',width_mm=pcbnew.ToMM(t.GetWidth()),points_mm=[[pcbnew.ToMM(p.x)-100,pcbnew.ToMM(p.y)-100]for p in(t.GetStart(),t.GetEnd())]))
fps={f.GetReference():f for f in b.GetFootprints()};drain=next(p for p in fps['Q1'].Pads()if p.GetNumber()=='2');target=drain.GetPosition();source=next(p for p in fps['R9'].Pads()if p.GetNumber()=='1');t=pcbnew.PCB_TRACK(b);t.SetStart(source.GetPosition());t.SetEnd(target);t.SetWidth(pcbnew.FromMM(.4));t.SetLayer(pcbnew.F_Cu);t.SetNet(source.GetNet());b.Add(t)
assert pcbnew.SaveBoard(str(N/(B+'.kicad_pcb')),b)
for ext in('.kicad_pro','.kicad_dru'):shutil.copyfile(S/(B+ext),N/(B+ext))
(N/'fp-lib-table').write_text((E/'fp-lib-table').read_text().replace('${KIPRJMOD}',E.as_posix()),encoding='utf-8',newline='\n')
# Separate oval-land negative control: wider lands violate retained3mm screen.
T=D/'studies/t1-oval';TB='T1_oval_process_study';TN=D/'studies/.work/t1-negative';TN.mkdir(parents=True,exist_ok=True);tb=pcbnew.LoadBoard(str(T/(TB+'.kicad_pcb')))
for f in tb.GetFootprints():
 for p in f.Pads():p.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(2.1),pcbnew.FromMM(2.15)))
assert pcbnew.SaveBoard(str(TN/(TB+'.kicad_pcb')),tb)
for ext in('.kicad_pro','.kicad_dru'):shutil.copyfile(T/(TB+ext),TN/(TB+ext))
(TN/'fp-lib-table').write_text((T/'fp-lib-table').read_text().replace('${KIPRJMOD}',T.as_posix()),encoding='utf-8',newline='\n')
import importlib.util
spec=importlib.util.spec_from_file_location('g',E/'full_geometry.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);cross=[]
for i,row in enumerate(positive):
 if row['net']!='/SENSE':continue
 a,z=row['points_mm'];count=max(1,math.ceil(math.dist(a,z)/.02))
 for key,p in g.pads.items():
  if p['tht']or g.pos[p['ref']]['side']==row['layer']or p['net']not in g.hv:continue
  bb=p['box'];minimum=min(math.hypot(max(bb[0]-(a[0]+(z[0]-a[0])*n/count),(a[0]+(z[0]-a[0])*n/count)-bb[2],0),max(bb[1]-(a[1]+(z[1]-a[1])*n/count),(a[1]+(z[1]-a[1])*n/count)-bb[3],0))for n in range(count+1))-row['width_mm']/2
  if minimum<3:cross.append(dict(track_index=i,opposite_HV_pad=key,conservative_sampled_projected_gap_mm=minimum,not_solid_dielectric_or_coupling_qualification=True))
out=dict(tracks=positive,crossface_HV_SENSE_track_projections_below3_mm=cross,positive_study_board_sha256=hashlib.sha256((S/(B+'.kicad_pcb')).read_bytes()).hexdigest(),negative_fixture='One SENSE segment deliberately crosses Q1DRAIN; retainedrules must reportshort/clearance. Productunchanged.',negative_board_sha256=hashlib.sha256((N/(B+'.kicad_pcb')).read_bytes()).hexdigest())
(S/'native-track-export.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(dict(tracks=len(positive),crossface_track_pairs=len(cross))))

from pathlib import Path
import json,hashlib,csv,math,sys
import pcbnew as k
ROOT=Path(__file__).resolve().parents[2]; S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'; P=ROOT/'work/Velluneo-2.0/hardware/E27/workflow/integrated-shade/compact-09/prototype-package'
sys.path.insert(0,str(ROOT/'work/compact09/checker'));import checker
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=S/'SC09_compact.kicad_pcb'; before=sha(src);b=checker.q.load_native(src)
def filled(board):
 return [{'name':z.GetZoneName(),'layer':board.GetLayerName(z.GetLayer()),'net':z.GetNetname(),'filled_area_mm2':z.GetFilledPolysList(z.GetLayer()).Area()/1e12,'polygons':[[[p.x,p.y] for p in z.GetFilledPolysList(z.GetLayer()).COutline(i).CPoints()] for i in range(z.GetFilledPolysList(z.GetLayer()).OutlineCount())]} for z in board.Zones() if not z.GetIsRuleArea()]
original=filled(b); b.BuildConnectivity(); assert k.ZONE_FILLER(b).Fill(b.Zones()); tmp=S/'.work/final-refill.kicad_pcb';assert k.SaveBoard(str(tmp),b,True)
b=checker.q.load_native(tmp);b.BuildConnectivity();assert k.ZONE_FILLER(b).Fill(b.Zones());assert k.SaveBoard(str(tmp),b,True)
new=filled(b);save(P/'checks/refill.json',{'source_sha256':before,'original_saved_fill':original,'two_pass_fresh_fill':new,'exact_polygon_equality':original==new,'original_source_unchanged':sha(src)==before,'refilled_copy_sha256':sha(tmp),'unconnected':b.GetConnectivity().GetUnconnectedCount(False),'limitations':'Actual saved polygon comparison; not physical thermal validation.'})
assert original==new,'Saved fills are stale'
assert sha(src)==before
footprints=[];pads=[]
for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
 p=f.GetPosition();row={'ref':f.GetReference(),'value':f.GetValue(),'footprint':str(f.GetFPID().GetLibItemName()),'side':b.GetLayerName(f.GetLayer()),'x_mm_from_left':round(k.ToMM(p.x)-100,5),'y_mm_from_top':round(k.ToMM(p.y)-100,5),'kicad_native_angle_deg':f.GetOrientationDegrees(),'models':len(f.Models()),'dnp':bool(f.IsDNP())};footprints.append(row)
 for pad in f.Pads():
  p=pad.GetPosition();pads.append({'ref':f.GetReference(),'pin':pad.GetNumber(),'net':pad.GetNetname(),'x_mm_from_left':round(k.ToMM(p.x)-100,5),'y_mm_from_top':round(k.ToMM(p.y)-100,5),'drill_x_mm':k.ToMM(pad.GetDrillSize().x),'drill_y_mm':k.ToMM(pad.GetDrillSize().y)})
with (P/'SC09_positions_manual_reference.csv').open('w',newline='',encoding='utf-8') as o:
 writer=csv.DictWriter(o,fieldnames=list(footprints[0]));writer.writeheader();writer.writerows(footprints)
with (P/'SC09_pin_connections.csv').open('w',newline='',encoding='utf-8') as o:
 writer=csv.DictWriter(o,fieldnames=list(pads[0]));writer.writeheader();writer.writerows(pads)
tracks=list(b.GetTracks());save(P/'checks/native-inventory.json',{'board_sha256':before,'kicad':k.GetBuildVersion(),'board_thickness_mm':k.ToMM(b.GetDesignSettings().GetBoardThickness()),'footprints':footprints,'physical_pads':len(pads),'copper_track_segments':sum(not isinstance(t,k.PCB_VIA) for t in tracks),'through_vias':sum(isinstance(t,k.PCB_VIA) for t in tracks),'track_widths_mm':sorted(set(k.ToMM(t.GetWidth()) for t in tracks if not isinstance(t,k.PCB_VIA))),'vias_mm':sorted(set((k.ToMM(t.GetWidth(k.F_Cu)),k.ToMM(t.GetDrill())) for t in tracks if isinstance(t,k.PCB_VIA))),'connected_thermal_zones':[{a:v for a,v in z.items() if a!='polygons'} for z in original],'model_coverage':sum(f['models'] for f in footprints),'DNP_refs':[f['ref'] for f in footprints if f['dnp']]})
print('Native inventory and exact two-pass fill comparison PASS',before)

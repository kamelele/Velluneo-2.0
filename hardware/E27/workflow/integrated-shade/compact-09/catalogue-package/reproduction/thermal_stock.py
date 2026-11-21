"""Native pour keepouts implement unchanged HV2mm / local.3mm matrix.
Rectangular copper-zone outlines avoid native complex-outline refill artifacts.
Guards affect pours only, never remove or waive DRC checks.
"""
from pathlib import Path
import sys,os,json,hashlib,pcbnew as k
root=Path(__file__).resolve().parent;S=root/'project';sys.path.insert(0,str(root/'checker'));import checker as c
src=S/'SC09_compact.kicad_pcb';b=c.q.load_native(src);contract=c.Contract(S,root/'spacing-matrix.CAT01.json',root/'package-assessment.CAT01.json');collector=c.Checker(b,contract);collector.collect();objects=list(collector.objects)
for z in list(b.Zones()):
 if z.GetZoneName().startswith('SOURCE_THERMAL'):b.Remove(z)
guard_records=[];bounds=c.q.rectangle([114.8,100.75,149.25,112])
for face,layer in [('F.Cu',k.F_Cu),('B.Cu',k.B_Cu)]:
 unions={}
 for o in objects:
  if o.layer!=face or o.net=='SW_SOURCE' or contract.gap('SW_SOURCE',o.net)<=.3:continue
  p=k.SHAPE_POLY_SET(o.shape);p.Inflate(k.FromMM(contract.gap('SW_SOURCE',o.net)+.02),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.001));p.BooleanIntersection(bounds)
  if p.IsEmpty():continue
  unions.setdefault(o.net,k.SHAPE_POLY_SET()).BooleanAdd(p)
 for net,poly in unions.items():
  for i in range(poly.OutlineCount()):
   shape=poly.UnitSet(i);z=k.ZONE(b);z.SetIsRuleArea(True);z.SetLayer(layer);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False);z.SetZoneName('SOURCE_HV_POUR_GUARD_'+net+'_'+face+'_'+str(i));z.Outline().Append(shape);b.Add(z);guard_records.append({'name':z.GetZoneName(),'net_basis':net,'clearance_basis_mm':contract.gap('SW_SOURCE',net)+.02,'kind':'nativecopperpour-onlykeepout,notDRCexclusion'})
 z=k.ZONE(b);z.SetNet(next(p.GetNet() for f in b.GetFootprints() if f.GetReference()=='U1' for p in f.Pads() if p.GetNumber()=='5'));z.SetLayer(layer);z.SetZoneName('SOURCE_THERMAL_'+face);z.SetLocalClearance(k.FromMM(.32));z.SetMinThickness(k.FromMM(.3));z.SetPadConnection(k.ZONE_CONNECTION_FULL);z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS);z.SetAssignedPriority(1);z.Outline().Append(bounds);b.Add(z)
for layer in [k.F_Cu,k.B_Cu]:
 z=k.ZONE(b);z.SetNet(next(p.GetNet() for f in b.GetFootprints() if f.GetReference()=='D1' for p in f.Pads() if p.GetNumber()=='2'));z.SetLayer(layer);z.SetZoneName('DIODE_ANODE_THERMAL_'+b.GetLayerName(layer));z.SetLocalClearance(k.FromMM(2.02));z.SetMinThickness(k.FromMM(.3));z.SetPadConnection(k.ZONE_CONNECTION_FULL);z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS);z.SetAssignedPriority(1);z.Outline().Append(c.q.rectangle([136,111.5,147,119]));b.Add(z)
e={'__file__':str(root/'grid_stock.py')};os.environ['SC09_ROUTE_BOARD']=str(src);exec(compile((root/'grid_stock.py').read_text().split('\njobs=')[0],str(root/'grid_stock.py'),'exec'),e);field,vias=e['fields']('/SW_SOURCE',.4);assert not vias[423,78]
pad=next(p for f in b.GetFootprints() if f.GetReference()=='U1' for p in f.Pads() if p.GetNumber()=='5');via=k.PCB_VIA(b);via.SetNet(pad.GetNet());via.SetViaType(k.VIATYPE_THROUGH);via.SetLayerPair(k.F_Cu,k.B_Cu);via.SetPosition(k.VECTOR2I(k.FromMM(142.3),k.FromMM(107.8)));via.SetWidth(k.FromMM(.75));via.SetDrill(k.FromMM(.3));via.SetFrontTentingMode(k.TENTING_MODE_TENTED);via.SetBackTentingMode(k.TENTING_MODE_TENTED);b.Add(via)
t=k.PCB_TRACK(b);t.SetNet(pad.GetNet());t.SetLayer(k.B_Cu);t.SetWidth(k.FromMM(.4));t.SetStart(pad.GetPosition());t.SetEnd(via.GetPosition());b.Add(t)
b.BuildConnectivity();filler=k.ZONE_FILLER(b);assert filler.Fill(b.Zones());first=S/'.work/thermal-guards-first.kicad_pcb';assert k.SaveBoard(str(first),b,True)
# Reload before the second fill so native island connectivity is rebuilt from saved copper.
b2=c.q.load_native(first);b2.BuildConnectivity();f2=k.ZONE_FILLER(b2);assert f2.Fill(b2.Zones());b2.BuildConnectivity();out=S/'.work/thermal-guards.kicad_pcb';assert k.SaveBoard(str(out),b2,True)
areas=[{'name':z.GetZoneName(),'layer':b2.GetLayerName(z.GetLayer()),'net':z.GetNetname(),'filled_area_mm2':z.GetFilledPolysList(z.GetLayer()).Area()/1e12} for z in b2.Zones() if not z.GetIsRuleArea()]
(root/'thermal-guards.json').write_text(json.dumps({'candidate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'zones':areas,'guard_areas':guard_records,'native_unconnected':b2.GetConnectivity().GetUnconnectedCount(False),'basis':'HV2.02mmnativepourguards withinoriginalSOURCErect; native.3localclearance; unchanged55matrix. Two-passfreshnativefill; isolatedcopperDRCmandatory. Notmeasuredtemperatures.'},indent=2)+'\n');print('guards',len(guard_records),json.dumps(areas))

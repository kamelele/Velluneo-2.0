"""Author an unreleased native PCB engineering workspace using the exact approved graph."""
from pathlib import Path
import json,shutil,math,hashlib,xml.etree.ElementTree as ET
import pcbnew
D=Path(__file__).resolve().parent;P=D.parent;B='Velluneo_specification_reset'
layout=json.loads((P/'driver-entry-02/layout-proposal.json').read_text(encoding='utf-8'))
parts={p['ref']:p for p in json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'))}
inv=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'));native={p['ref']:p for p in inv['parts']}
heights={p['ref']:p['installed_envelope_mm']for p in json.loads((P/'assembly-fit-01/height-contract.json').read_text(encoding='utf-8'))['parts']}
bodies={p['ref']:p['native_fab_stroke_bbox_mm']for p in json.loads((P/'assembly-fit-01/native-body-bounds.json').read_text(encoding='utf-8'))['parts']}
root=ET.parse(D/'checks/current-netlist.xml').getroot();comps={c.attrib['ref']:c for c in root.findall('./components/comp')}
assert set(parts)==set(native)==set(layout['positions'])==set(comps)and len(parts)==31
brd=pcbnew.BOARD();brd.SetCopperLayerCount(2);brd.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(1.6))
logicalnames=sorted({n for c in parts.values()for n in c['pins'].values()if n is not None});assert len(logicalnames)==22
expected={n:{(ref,pin)for ref,c in parts.items()for pin,nn in c['pins'].items()if nn==n}for n in logicalnames}
actual={n.attrib['name']:{(p.attrib['ref'],p.attrib['pin'])for p in n.findall('node')}for n in root.findall('./nets/net')}
aliases={}
for n,pins in expected.items():
 matches=[nn for nn,pp in actual.items()if pp==pins];assert len(matches)==1,(n,matches);aliases[n]=matches[0]
physicalnet={pair:name for name,pins in actual.items()for pair in pins}
assert len(actual)==26 and len(physicalnet)==79
netnames=sorted(actual)
nets={}
for name in netnames:
 ni=pcbnew.NETINFO_ITEM(brd,name,len(nets)+1);brd.Add(ni);nets[name]=ni
models=D/'models';models.mkdir(exist_ok=True);modelrecords=[]
def envelope(ref):
 bb=bodies[ref];h=heights[ref]
 if ref=='T1':bb=[-15,-15,15,15]
 cx=(bb[0]+bb[2])/2;cy=-(bb[1]+bb[3])/2
 color=(.19,.29,.43)if ref=='T1'else(.23,.48,.63)if ref=='C1'else(.70,.49,.20)if ref=='R1'else(.28,.32,.37)
 appearance='appearance Appearance { material Material { diffuseColor '+' '.join(map(str,color))+' } }'
 # KiCad VRML convention: one model unit is2.54mm. This is an allocated envelope.
 if ref=='C1':
  # Use an explicit mesh after the primitive was missing in the observed native render.
  vertices=[(5.25*math.cos(i*math.tau/32)/2.54,5.25*math.sin(i*math.tau/32)/2.54,z/2.54)for z in(-h/2,h/2)for i in range(32)]
  faces=[list(reversed(range(32))),list(range(32,64))]+[[i,(i+1)%32,(i+1)%32+32,i+32]for i in range(32)]
  geom='Shape { '+appearance+' geometry IndexedFaceSet { solid FALSE coord Coordinate { point [ '+','.join(' '.join(f'{v:.9f}'for v in pt)for pt in vertices)+' ] } coordIndex [ '+','.join(' '.join(map(str,face))+', -1'for face in faces)+' ] } }'
 else:geom='Shape { '+appearance+f' geometry Box {{ size {(bb[2]-bb[0])/2.54:.9f} {(bb[3]-bb[1])/2.54:.9f} {h/2.54:.9f} }} }}'
 text='#VRML V2.0 utf8\n# PROJECT ALLOCATED ENVELOPE, NOT QUALIFIED VENDOR MECHANICAL MODEL\n'+f'Transform {{ translation {cx/2.54:.9f} {cy/2.54:.9f} {h/2/2.54:.9f} children [ '+geom+' ] }\n'
 f=models/(ref+'.wrl');f.write_text(text,encoding='utf-8',newline='\n');modelrecords.append({'ref':ref,'file':'models/'+f.name,'allocated_height_mm':h,'qualified_model':False,'units_mm_per_VRML_unit':2.54})
 return '${KIPRJMOD}/models/'+f.name
offset=(100.,100.)
for ref in sorted(parts):
 item=native[ref];c=layout['positions'][ref];name=item['footprint'].split(':')[1]
 f=pcbnew.FootprintLoad(str(P/'libraries/Velluneo_Driver.pretty'),name);assert f
 brd.Add(f);f.SetReference(ref);f.SetValue(comps[ref].findtext('value'))
 for field in comps[ref].findall('./fields/field'):
  fieldname=field.attrib['name']
  if fieldname in('MPN','Library_Status'):
   f.SetField(fieldname,field.text or'');f.GetField(fieldname).SetVisible(False)
 f.SetField('Description',comps[ref].findtext('description')or'');f.GetField('Description').SetVisible(False)
 fpid=f.GetFPID();fpid.SetLibNickname(pcbnew.UTF8('Velluneo_Driver'));fpid.SetLibItemName(pcbnew.UTF8(name));f.SetFPID(fpid)
 # Preserve schematic association; footprint IDs stay tied to the local source library.
 comp=comps[ref];sheet=comp.find('sheetpath').attrib['tstamps'];tstamps=comp.findtext('tstamps').strip().split()
 path=sheet.rstrip('/')+'/'+tstamps[-1];f.SetPath(pcbnew.KIID_PATH(path))
 if c['side']=='B':f.Flip(pcbnew.VECTOR2I(0,0),True)
 f.Rotate(pcbnew.VECTOR2I(0,0),pcbnew.EDA_ANGLE(c['angle_deg'],pcbnew.DEGREES_T));f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(c['x_mm']+100),pcbnew.FromMM(c['y_mm']+100)))
 f.Reference().SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(.8),pcbnew.FromMM(.8)));f.Reference().SetTextThickness(pcbnew.FromMM(.12));f.Reference().SetVisible(True);f.Value().SetVisible(False)
 for pad in f.Pads():
  number=pad.GetNumber();assert number in parts[ref]['pins'];net=parts[ref]['pins'][number]
  pad.SetNet(nets[physicalnet[(ref,number)]])
 model=pcbnew.FP_3DMODEL();model.m_Filename=envelope(ref);f.Add3DModel(model)
def point(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
for a,b in[((84,70),(116,70)),((116,70),(116,130)),((116,130),(84,130)),((84,130),(84,70))]:
 s=pcbnew.PCB_SHAPE();s.SetShape(pcbnew.SHAPE_T_SEGMENT);s.SetLayer(pcbnew.Edge_Cuts);s.SetStart(point(*a));s.SetEnd(point(*b));s.SetWidth(pcbnew.FromMM(.05));brd.Add(s)
# A genuine no-new-copper rule area spans the straight gap between saved domains.
primary=[];secondary=[]
for ref,c in layout['positions'].items():
 for pp,bb in zip(native[ref]['pads'],c['pads']):
  sec=(ref=='T1'and pp['pin']in('6','7','8','9','10'))or ref in{'C4','D3','J2','R11','R12'}
  (secondary if sec else primary).append(bb)
y0=max(b[3]for b in secondary)+.15;y1=min(b[1]for b in primary)-.15
assert y1>y0
zone=pcbnew.ZONE(brd);zone.SetIsRuleArea(True);zone.SetZoneName('DRAFT_PS_NO_NEW_COPPER_NOT_QUALIFIED_INSULATION');layers=pcbnew.LSET();layers.AddLayer(pcbnew.F_Cu);layers.AddLayer(pcbnew.B_Cu);zone.SetLayerSet(layers)
zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True);zone.SetDoNotAllowPads(True);zone.SetDoNotAllowZoneFills(True);zone.SetDoNotAllowFootprints(False)
poly=zone.Outline();poly.NewOutline()
for x,y in[(84,y0+100),(116,y0+100),(116,y1+100),(84,y1+100)]:poly.Append(pcbnew.FromMM(x),pcbnew.FromMM(y))
brd.Add(zone)
def annotation(s,x,y,size=.8,layer=pcbnew.Dwgs_User):
 t=pcbnew.PCB_TEXT(brd);t.SetText(s);t.SetPosition(point(x,y));t.SetLayer(layer);t.SetTextSize(point(size,size));t.SetTextThickness(pcbnew.FromMM(.12));brd.Add(t)
annotation('PCB ENGINEERING DRAFT - UNROUTED',100,66,1.0)
annotation('32 x 60 mm / 31 components / 79 pads',100,134,.8)
annotation('OPEN: STARTUP / FAULTS / T1 / INSULATION / THERMAL',100,136.2,.65)
annotation('T1 30x30x18 REQUIRED ENVELOPE; NOT VERIFIED',100,91,.65)
annotation('NO NEW COPPER - DRAFT RESERVATION',100,100+(y0+y1)/2,.55)
boardfile=D/(B+'.kicad_pcb');assert pcbnew.SaveBoard(str(boardfile),brd)
# Retain the actual schematic, symbol and footprint identities; relative tables work in this checkout.
shutil.copyfile(P/(B+'.kicad_sch'),D/(B+'.kicad_sch'))
for table in('fp-lib-table','sym-lib-table'):
 txt=(P/table).read_text(encoding='utf-8').replace('${KIPRJMOD}/libraries/','${KIPRJMOD}/../libraries/')
 (D/table).write_text(txt,encoding='utf-8',newline='\n')
pro={'meta':{'filename':B+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.25,'min_track_width':.3,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_copper_edge_clearance':.5}}}}
(D/(B+'.kicad_pro')).write_text(json.dumps(pro,indent=2)+'\n',encoding='utf-8',newline='\n')
def condition(names,obj):return '('+' || '.join(f"{obj}.NetName == '{aliases.get(n,n)}'"for n in names)+')'
s=['OUTPUT_POS','OUTPUT_NEG','SECONDARY_RAW'];p=[n for n in logicalnames if n not in s]
s += [physicalnet[('T1',pin)]for pin in('7','8','9')]
p += [physicalnet[('T1','3')]]
hv=['AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','BULK_POS','DRAIN','CLAMP'];quiet=['VDD','VS','NTC','CS','DRV','GATE','SENSE','PRIMARY_GND','AUX_RAW','AUX_RECT']
def between(a,b):return '('+condition(a,'A')+' && '+condition(b,'B')+') || ('+condition(b,'A')+' && '+condition(a,'B')+')'
rules='(version 1)\n# DRAFT engineering reservations; no product/IEC approval or exception.\n'+f'(rule "DRAFT_PRIMARY_SECONDARY_10mm_NOMINAL" (condition "{between(p,s)}") (constraint clearance (min 10 mm)))\n'+f'(rule "DRAFT_PRIMARY_HV_QUIET_3mm_UNRESOLVED" (condition "{between(hv,quiet)}") (constraint clearance (min 3 mm)))\n'
(D/(B+'.kicad_dru')).write_text(rules,encoding='utf-8',newline='\n')
record={'native_pcbnew':pcbnew.Version(),'base':'7b75131667252634584552b4094c608cd88b9f2a','approved_intent':'5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8','board':boardfile.name,'offset_mm':offset,'rectangle_mm':[32,60],'copper_layers':2,'thickness_mm':1.6,'native_footprints':len(list(brd.GetFootprints())),'native_pads':sum(len(list(f.Pads()))for f in brd.GetFootprints()),'tracks_or_vias':len(list(brd.GetTracks())),'net_names':netnames,'logical_nets':22,'intentional_single_pad_NC_nets':4,'logical_to_native_net_names':aliases,'keepout_global_Y_mm':[y0+100,y1+100],'keepout_is_insulation_approval':False,'models':modelrecords,'stage_approval':False,'qualification_complete':False}
(D/'build-result.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({k:record[k]for k in('native_pcbnew','native_footprints','native_pads','tracks_or_vias','keepout_global_Y_mm')}))

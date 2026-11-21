"""Complete proposed ECO PCB capture from its unapproved33-part intent and native sources."""
from pathlib import Path
import json,math,shutil,xml.etree.ElementTree as ET,pcbnew,hashlib
import full_geometry as geom
D=Path(__file__).resolve().parent;ROOT=D.parent.parent/'pcb-closure-04';P=ROOT.parent;B='Velluneo_specification_reset'
parts=geom.parts;pos=geom.pos;assign=json.loads((D/'assignments.json').read_text(encoding='utf-8'));xml=ET.parse(D/'checks/proposed-netlist.xml').getroot();comps={c.attrib['ref']:c for c in xml.findall('./components/comp')};assert set(comps)==set(parts)
actual={n.attrib['name']:{(p.attrib['ref'],p.attrib['pin'])for p in n.findall('node')}for n in xml.findall('./nets/net')};phys={pair:n for n,ps in actual.items()for pair in ps};assert len(phys)==81 and len(actual)==27
logical={n:{(r,pin)for r,p in parts.items()for pin,nn in p['pins'].items()if nn==n}for n in{n for p in parts.values()for n in p['pins'].values()if n is not None}};aliases={}
for n,pins in logical.items():
 matches=[name for name,p in actual.items()if p==pins];assert len(matches)==1;aliases[n]=matches[0]
brd=pcbnew.BOARD();brd.SetCopperLayerCount(2);brd.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(1.6));nets={}
for n in sorted(actual):net=pcbnew.NETINFO_ITEM(brd,n,len(nets)+1);brd.Add(net);nets[n]=net
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
models=D/'models';models.mkdir(exist_ok=True);modelrecords=[]
def model(ref):
 target=models/(ref+'.wrl')
 if ref not in{'U1','Q1','BR1','R16','R17'}:assert target.exists(),ref;h=None
 elif ref in{'R16','R17'}:shutil.copyfile(models/'R2.wrl',target)if not target.exists()else None;h=.9
 else:
  bb,h={'U1':([-.8,-1.45,.8,1.45],1.65),'Q1':([-5.2,-4.6,5.2,0],23.),'BR1':([-4.93,-4.93,4.93,4.93],10.)}[ref];cx=(bb[0]+bb[2])/2;cy=-(bb[1]+bb[3])/2
  s='#VRML V2.0 utf8\n# PROJECT ENVELOPE, NOT QUALIFIED MANUFACTURER MODEL/INSTALLED HEIGHT\n'+f'Transform {{ translation {cx/2.54:.9f} {cy/2.54:.9f} {h/5.08:.9f} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor .28 .32 .37 }} }} geometry Box {{ size {(bb[2]-bb[0])/2.54:.9f} {(bb[3]-bb[1])/2.54:.9f} {h/2.54:.9f} }} }} ] }}\n';target.write_text(s,encoding='utf-8',newline='\n')
 modelrecords.append(dict(ref=ref,path='models/'+target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),new_allocated_height_mm=h,qualified=False));return '${KIPRJMOD}/models/'+target.name
for ref,p in parts.items():
 fpid=assign[ref]['footprint'];lib,name=fpid.split(':');libpath=D/('Velluneo_ECO04.pretty'if lib=='Velluneo_ECO04'else'libraries/Velluneo_Driver.pretty');fp=pcbnew.FootprintLoad(str(libpath),name);assert fp;fp.SetReference(ref);fp.SetValue(comps[ref].findtext('value'));fp.SetFPID(pcbnew.LIB_ID(lib,name));brd.Add(fp)
 for field in comps[ref].findall('./fields/field'):
  if field.attrib['name']in('MPN','Library_Status'):fp.SetField(field.attrib['name'],field.text or'');fp.GetField(field.attrib['name']).SetVisible(False)
 fp.SetField('Description',comps[ref].findtext('description')or'');fp.GetField('Description').SetVisible(False)
 comp=comps[ref];fp.SetPath(pcbnew.KIID_PATH(comp.find('sheetpath').attrib['tstamps'].rstrip('/')+'/'+comp.findtext('tstamps').strip().split()[-1]))
 c=pos[ref]
 if c['side']=='B':fp.Flip(pt(0,0),True)
 fp.SetOrientation(pcbnew.EDA_ANGLE(c['angle_deg'],pcbnew.DEGREES_T));fp.SetPosition(pt(c['x_mm']+100,c['y_mm']+100));fp.Reference().SetTextSize(pt(.8,.8));fp.Reference().SetTextThickness(pcbnew.FromMM(.12));fp.Reference().SetVisible(True);fp.Value().SetVisible(False)
 for pad in fp.Pads():pad.SetNet(nets[phys[(ref,pad.GetNumber())]])
 m=pcbnew.FP_3DMODEL();m.m_Filename=model(ref);fp.Add3DModel(m)
x0,x1=100-geom.HW,100+geom.HW;ybottom,ytop=100-geom.HH,100+geom.HH
for a,b in[((x0,ybottom),(x1,ybottom)),((x1,ybottom),(x1,ytop)),((x1,ytop),(x0,ytop)),((x0,ytop),(x0,ybottom))]:
 edge=pcbnew.PCB_SHAPE();edge.SetShape(pcbnew.SHAPE_T_SEGMENT);edge.SetLayer(pcbnew.Edge_Cuts);edge.SetStart(pt(*a));edge.SetEnd(pt(*b));edge.SetWidth(pcbnew.FromMM(.05));brd.Add(edge)
y0=max(p['box'][3]for p in geom.pads.values()if p['domain']=='S')+.15;y1=min(p['box'][1]for p in geom.pads.values()if p['domain']=='P')-.15;assert y1>y0
zone=pcbnew.ZONE(brd);zone.SetIsRuleArea(True);zone.SetZoneName('PROPOSED_PS_NO_NEW_COPPER_NOT_QUALIFIED');ls=pcbnew.LSET();ls.AddLayer(pcbnew.F_Cu);ls.AddLayer(pcbnew.B_Cu);zone.SetLayerSet(ls)
zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True);zone.SetDoNotAllowPads(True);zone.SetDoNotAllowZoneFills(True);zone.SetDoNotAllowFootprints(False);poly=zone.Outline();poly.NewOutline()
for x,y in[(x0,y0+100),(x1,y0+100),(x1,y1+100),(x0,y1+100)]:poly.Append(pcbnew.FromMM(x),pcbnew.FromMM(y))
brd.Add(zone)
for text,y in [('OWNER-SELECTED33 BASIS - CONTROL05 DRAFT - UNROUTED',66),('FORMED TERMINALS / INSTALLED ENVELOPES / INSULATION UNQUALIFIED',134)]:
 t=pcbnew.PCB_TEXT(brd);t.SetText(text);t.SetPosition(pt(100,y));t.SetLayer(pcbnew.Dwgs_User);t.SetTextSize(pt(.65,.65));t.SetTextThickness(pcbnew.FromMM(.12));brd.Add(t)
assert pcbnew.SaveBoard(str(D/(B+'.kicad_pcb')),brd)
(D/(B+'.kicad_pro')).write_bytes((D/'project-settings-source.json').read_bytes())
def condition(names,obj):return '('+' || '.join(f"{obj}.NetName == '{aliases.get(n,n)}'"for n in names)+')'
def between(a,b):return '('+condition(a,'A')+' && '+condition(b,'B')+') || ('+condition(b,'A')+' && '+condition(a,'B')+')'
s=['OUTPUT_POS','OUTPUT_NEG','SECONDARY_RAW'];p=[n for n in logical if n not in s];s +=[phys[('T1',n)]for n in('7','8','9')];p +=[phys[('T1','3')]]
hv=['AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','BULK_POS','DRAIN','CLAMP','STARTUP_MID'];quiet=['VDD','VS','NTC','CS','DRV','GATE','SENSE','PRIMARY_GND','AUX_RAW','AUX_RECT']
rules='(version 1)\n# Unapproved ECO geometry; numeric3/10mm screens retained. No safety/process acceptance.\n'+f'(rule "PROPOSED_PS_10mm" (condition "{between(p,s)}") (constraint clearance (min 10 mm)))\n'+f'(rule "PROPOSED_HV_QUIET_3mm" (condition "{between(hv,quiet)}") (constraint clearance (min 3 mm)))\n'
(D/(B+'.kicad_dru')).write_text(rules,encoding='utf-8',newline='\n')
(D/'full-build-result.json').write_text(json.dumps(dict(parts=33,pads=81,functional_nets=23,NC_singletons=4,logical_to_native_netnames=aliases,actual_copper_free_band_y_mm=[y0+100,y1+100],models=modelrecords,basis_owner_selected=True,source_graph_technical_stage_approved=False,stage_approved=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Proposed complete33-part81-padnativePCBsaved; nointent/process/routingapproval')

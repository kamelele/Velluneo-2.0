from pathlib import Path
import json,hashlib,shutil,math
import pcbnew as k
HERE=Path(__file__).resolve().parent;S=HERE/'project';SRC=S/'SC09_compact.kicad_pcb';D=HERE/'routing';D.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def root_nodes(s):
 depth=0;quoted=False;esc=False;start=None;out=[]
 for i,c in enumerate(s):
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
   continue
  if c=='"':quoted=True
  elif c=='(':
   depth+=1
   if depth==2:start=i
  elif c==')':
   if depth==2:out.append((start,i+1,s[start:i+1]))
   depth-=1
 return out
orig=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(SRC));original={f.GetReference():f for f in orig.GetFootprints()};s=SRC.read_text();remove=[]
for a,z,t in root_nodes(s):
 if t.startswith('(segment') or t.startswith('(via') or (t.startswith('(zone') and 'C6_CAN_AND_VENT' not in t):remove.append((a,z))
 if t.startswith('(footprint') and any(f'(property "Reference" "{r}"' in t for r in ['T1','L1']):remove.append((a,z))
for a,z in sorted(set(remove),reverse=True):s=s[:a]+s[z:]
candidate=D/'SC09_compact.kicad_pcb';candidate.write_text(s)
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(candidate));v=lambda x,y:k.VECTOR2I(k.FromMM(x+100),k.FromMM(y+100))
def props(ref):return f'(fp_text reference "REF**"(at 0 -5)(layer "F.Fab")(effects(font(size .7 .7)(thickness .1))))(fp_text value "SC09_{ref}"(at 0 5)(layer "F.Fab")hide(effects(font(size .7 .7)(thickness .1))))'
def rect(x0,y0,x1,y1,layer,width):return f'(fp_rect(start {x0} {y0})(end {x1} {y1})(stroke(width {width})(type default))(fill none)(layer "{layer}"))'
t1='(footprint "SC09_T1"(version 20241229)(generator "pcbnew")(layer "F.Cu")(attr smd)(descr "CoilcraftMSS1210Hmanufacturerlandpattern;2nonpolarterminals;1.2mH400V;maxbody12.3square10.2high")'+props('T1')+rect(-6,-6,6,6,'F.Fab',.1)+rect(-6.4,-6.5,6.4,6.5,'F.CrtYd',.05)
for pin,y in [(1,4.75),(2,-4.75)]:t1+=f'(pad "{pin}" smd rect(at 0 {y})(size 5.5 3.0)(layers "F.Cu" "F.Paste" "F.Mask"))'
t1+='(model "${KIPRJMOD}/Models/SC09_T1.wrl"(offset(xyz 0 0 0))(scale(xyz 1 1 1))(rotate(xyz 0 0 0))))';(S/'E27SC09.pretty/SC09_T1.kicad_mod').write_text(t1)
l1='(footprint "SC09_L1"(version 20241229)(generator "pcbnew")(layer "F.Cu")(attr through_hole)(descr "Wurth768772332WE-TIHV3.3mH400V;nominalP5compatibleP5.0038;manualfreeleadadjustmentandfitinspection")'+props('L1')
l1+='(fp_circle(center 0 0)(end 4.15 0)(stroke(width .1)(type default))(fill none)(layer "F.Fab"))(fp_circle(center 0 0)(end 4.65 0)(stroke(width .05)(type default))(fill none)(layer "F.CrtYd"))'
for pin,x in [(1,-2.5019),(2,2.5019)]:l1+=f'(pad "{pin}" thru_hole {"rect" if pin==1 else "circle"}(at {x} 0)(size 2.3 2.3)(drill 1.2)(layers "*.Cu" "*.Mask"))'
l1+='(model "${KIPRJMOD}/Models/SC09_L1.wrl"(offset(xyz 0 0 0))(scale(xyz 1 1 1))(rotate(xyz 0 0 0))))';(S/'E27SC09.pretty/SC09_L1.kicad_mod').write_text(l1)
bom={c['ref']:c for c in load(S/'bom-build.json')['components']}
for ref,x,y in [('T1',43,6.95),('L1',6.5,22.2)]:
 fp=k.FootprintLoad(str(S/'E27SC09.pretty'),'SC09_'+ref);b.Add(fp);fp.SetReference(ref);fp.SetFPID(original[ref].GetFPID());fp.SetPath(original[ref].GetPath());fp.SetSheetname('/');fp.SetSheetfile('SC09_compact.kicad_sch');fp.SetPosition(v(x,y));fp.SetOrientationDegrees(0);fp.SetValue('1m2 / 400V catalogue' if ref=='T1' else original[ref].GetValue())
 for p in fp.Pads():p.SetNet(b.FindNet('/'+bom[ref]['pins'][p.GetNumber()]))
 for field in ['MPN','Datasheet']:fp.SetField(field,bom[ref]['mpn' if field=='MPN' else 'source']);fp.GetField(field).SetVisible(False)
fps={f.GetReference():f for f in b.GetFootprints()};fps['C4'].SetPosition(v(43,17));fps['R7'].SetValue('390k / HVR25');fps['R7'].SetField('MPN',bom['R7']['mpn']);fps['R7'].SetField('Datasheet',bom['R7']['source'])
for t in b.GetDrawings():
 if isinstance(t,k.PCB_TEXT) and t.GetText()=='SC09 LAB':t.SetText('SC09 CAT')
expected={(p['ref'],p['pin']):'/'+n['id'] for n in load(S/'intended-connectivity.CAT01.json')['nets'] for p in n['pins']};actual={(f.GetReference(),p.GetNumber()):p.GetNetname() for f in b.GetFootprints() for p in f.Pads()};assert actual==expected and len(actual)==46
assert k.SaveBoard(str(candidate),b,True)
for name in ['SC09_compact.kicad_pro','SC09_compact.kicad_dru','SC09_compact.kicad_sch','fp-lib-table','E27SC09.kicad_sym','PowerFlags.kicad_sym','sym-lib-table']:shutil.copy2(S/name,D/name)
shutil.copytree(S/'E27SC09.pretty',D/'E27SC09.pretty',dirs_exist_ok=True)
g=load(S/'footprint-geometry.json');g['T1']={'pads':[{'number':str(pin),'center_mm':[0,y],'size_mm':[5.5,3.0],'drill_mm':None,'kind':'smd','shape':'rect'} for pin,y in [(1,4.75),(2,-4.75)]],'max_body_bbox_xy_mm':[-6.15,-6.15,6.15,6.15],'planned_max_above_PCB_mm':10.3,'body_height_manufacturer_max_mm':10.2,'proposed_solder_seating_allowance_mm':.1,'courtyard_polygon':[[-6.4,-6.5],[6.4,-6.5],[6.4,6.5],[-6.4,6.5]],'footprint':'E27SC09:SC09_T1','design_basis':'ManufacturerMSS1210Hrecommendedlands,page2;nonpolarterminal1LED/2FBisexplicitdesignassignment.Notcustomcoil/3rdNC.'}
g['L1']['max_body_bbox_xy_mm']=[-4.15,-4.15,4.15,4.15];g['L1']['planned_max_above_PCB_mm']=10.5;g['L1']['courtyard_bbox_xy_mm']=[-4.65,-4.65,4.65,4.65];g['L1']['design_basis']='Wurth768772332catalogue3.3mHHV400V,bodyD8.3/H10max+.5seating,P5±.5/freeleadforming;manufacturerrecommended1.2holes;compatibleP5.0038retained.';save(S/'footprint-geometry.json',g)
print('PrivateunroutedcataloguePCB19refs46pins;newT1/L1physicalparts,C4+.5mm;allpinassignmentsmatchindependentCAT01')

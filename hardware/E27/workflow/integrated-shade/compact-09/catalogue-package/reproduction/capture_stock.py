"""SC09-A schematic writer. Requires actual approved independent graph and part reports."""
from pathlib import Path
import json,hashlib,uuid,math,re,shutil
root=Path(__file__).resolve().parents[2];R=root/'Velluneo-2.0';S=Path(__file__).resolve().parent/'project';W=Path(__file__).resolve().parent/'capture-evidence'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();save=lambda p,x:p.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
g=load(S/'intended-connectivity.CAT01.json');dg=hashlib.sha256(json.dumps({k:v for k,v in g.items() if k!='approval'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert (root/'compact09/capture-active/active-parts-report.json').exists()
assert (root/'compact09/capture-passive/report.json').exists(),'Finish part verification before capture'
parts=load(S/('bom-build.json' if (S/'bom-build.json').exists() else 'bom-proposal.A1.json'))['components'];by={c['ref']:c for c in parts}
fpids=load(S/'footprint-assignments.json') if (S/'footprint-assignments.json').exists() else {}
q=lambda x:json.dumps(str(x),ensure_ascii=False)
uid=lambda x:str(uuid.uuid5(uuid.NAMESPACE_URL,'Velluneo/SC09-A/'+x))
num=lambda x:f'{x:.5f}'.rstrip('0').rstrip('.') if x else '0'
def effects(size=1,justify=''):return f'(effects(font(size {size} {size})){"(justify "+justify+")" if justify else ""})'
def line(a,b):return f'(polyline(pts(xy {a[0]} {a[1]})(xy {b[0]} {b[1]}))(stroke(width .254)(type default))(fill(type none)))'
def poly(ps):return '(polyline(pts'+''.join(f'(xy {x} {y})' for x,y in ps)+')(stroke(width .254)(type default))(fill(type none)))'
def rect(a,b):return f'(rectangle(start {a[0]} {a[1]})(end {b[0]} {b[1]})(stroke(width .254)(type default))(fill(type background)))'
def pin(n,name,x,y,angle,kind='passive',length=2.54):return f'(pin {kind} line(at {x} {y} {angle})(length {length})(name {q(name)}{effects(.9)})(number {q(n)}{effects(.9)}))'
def prop(n,v,x,y,hide=False,size=1,angle=0):return f'(property {q(n)} {q(v)}(at {num(x)} {num(y)} {angle})(effects(font(size {size} {size})){"(hide yes)" if hide else ""}))'
maps={};symbols=[]
for c in parts:
 r=c['ref'];k=c['kind'];name='SC09_'+r;names={};types={};p={'1':(-5.08,0,0),'2':(5.08,0,180)};art=''
 if k in ['resistor','sense resistor','HV resistor','bleeder','fusible resistor']:art=rect((-2.54,1),(2.54,-1))
 elif k in ['film','MLCC','electrolytic']:
  p={'1':(-3.81,0,0),'2':(3.81,0,180)};art=line((-.635,1.8),(-.635,-1.8))+line((.635,1.8),(.635,-1.8))+line((-1.27,0),(-.635,0))+line((.635,0),(1.27,0))
  if k=='electrolytic':art+=f'(text "+"(at -1.7 2.4 0){effects()})'
 elif k=='MOV':art=rect((-2.54,1.8),(2.54,-1.8))+line((-3.3,-2.4),(3.3,2.4))
 elif k=='inductor':
  if r=='T1':p={'2':(-7.62,0,0),'1':(7.62,0,180)}
  art=poly([(-2.54,0),(-1.9,1.2),(-1.27,0),(-.64,1.2),(0,0),(.64,1.2),(1.27,0),(1.9,1.2),(2.54,0)])
  if r=='T1':art+=line((-5.08,0),(-2.54,0))+line((2.54,0),(5.08,0))
 elif k=='custom inductor':
  p={'8':(-7.62,0,0),'1':(7.62,0,180),'4':(0,-7.62,90)};art=poly([(-5.08,0),(-3.81,2.54),(-2.54,0),(-1.27,2.54),(0,0),(1.27,2.54),(2.54,0),(3.81,2.54),(5.08,0)])+line((-5.08,-1.27),(5.08,-1.27));names={'1':'WINDING','8':'WINDING','4':'UNWOUND'};types={'4':'no_connect'}
 elif k=='wirepads':
  p={'1':(5.08,1.27,180),'2':(5.08,-1.27,180)} if r=='J1' else {'1':(-5.08,1.27,0),'2':(-5.08,-1.27,0)}
  art=rect((-2.54,2.54),(2.54,-2.54));names={'1':'L' if r=='J1' else 'LED+','2':'N' if r=='J1' else 'RETURN'}
 elif k=='bridge':
  p={'1':(12.7,2.54,180),'2':(-12.7,2.54,0),'3':(12.7,-2.54,180),'4':(-12.7,-2.54,0)};names={'1':'+','2':'~','3':'-','4':'~'};art=rect((-10.16,5.08),(10.16,-5.08))
 elif k=='IC':
  p={'1':(-3.81,10.16,270),'2':(-3.81,-10.16,90),'3':(3.81,-10.16,90),'4':(-12.7,0,0),'5':(12.7,3.81,180),'6':(12.7,1.27,180),'7':(12.7,-1.27,180),'8':(12.7,-3.81,180)}
  names={'1':'BP','2':'M','3':'FB','4':'D','5':'S','6':'S','7':'S','8':'S'};types={'1':'power_out','2':'input','3':'input','4':'power_in'};art=rect((-10.16,7.62),(10.16,-7.62))
 elif k=='diode':
  names={'1':'K','2':'A'};art=poly([(1.27,1.27),(-1.27,0),(1.27,-1.27),(1.27,1.27)])+line((-1.27,-1.27),(-1.27,1.27))
 else:raise ValueError(k)
 assert set(p)==set(c['pins']),r
 props=prop('Reference',re.match('[A-Z]+',r)[0],0,8)+prop('Value',c['mpn'],0,-8)+prop('Footprint',fpids.get(r,''),0,0,True)+prop('Datasheet',c['source'],0,0,True)
 pinhide=' hide' if k not in ['IC','bridge','wirepads'] else ''
 symbols.append(f'(symbol {q(name)}(pin_names(offset .6){pinhide})(exclude_from_sim no)(in_bom yes)(on_board yes){props}(symbol {q(name+"_0_1")}{art})(symbol {q(name+"_1_1")}{"".join(pin(n,names.get(n,n),*v,types.get(n,"passive")) for n,v in p.items())}))')
 maps[r]={'library_id':'E27SC09:'+name,'pins':{n:dict(x=v[0],y=v[1],angle=v[2],electrical_type=types.get(n,'passive')) for n,v in p.items()}}
lib='(kicad_symbol_lib(version 20241209)(generator "kicad_symbol_editor")'+''.join(symbols)+')';save(S/'E27SC09.kicad_sym',lib)
pos={'J1':(22.86,58.42,0),'RF1':(50.8,57.15,0),'RV1':(68.58,76.2,270),'BR1':(96.52,59.69,0),'C1':(124.46,91.44,270),'L1':(147.32,57.15,0),'C4':(170.18,91.44,270),'U1':(222.25,60.96,0),'R5':(260.35,57.15,0),'R6':(260.35,76.2,0),'T1':(299.72,57.15,0),'D1':(278.13,110.49,270),'C6':(330.2,91.44,270),'R8':(351.79,91.44,270),'R9':(372.11,91.44,270),'J2':(393.7,58.42,0),'C5':(210.82,157.48,0),'R7':(147.32,152.4,0),'R4':(147.32,171.45,0)}
def pp(r,n):
 x,y,a=pos[r];v=maps[r]['pins'][str(n)];co=round(math.cos(math.radians(a)),12);si=round(math.sin(math.radians(a)),12)
 return round(x+co*v['x']-si*v['y'],5),round(y-si*v['x']-co*v['y'],5)
items=[];sheet=uid('sheet')
def wire(a,b):
 if a==b:return
 items.append(f'(wire(pts(xy {num(a[0])} {num(a[1])})(xy {num(b[0])} {num(b[1])}))(stroke(width 0)(type default))(uuid "{uid("wire"+str(a)+str(b))}"))')
def route(*pts):
 for a,b in zip(pts,pts[1:]):wire(a,b)
def label(n,point,side='right'):
 items.append(f'(label {q(n)}(at {num(point[0])} {num(point[1])} 0){effects(.95,("right" if side=="left" else "left")+" bottom")}(uuid "{uid("label"+n+str(point))}"))')
def stub(r,n,net,end,side='right'):wire(pp(r,n),end);label(net,end,side)
def note(t,x,y,size=1.4):items.append(f'(text {q(t)}(at {x} {y} 0){effects(size,"left")}(uuid "{uid("note"+t)}"))')
values={'RF1':'10R / 2W FUSIBLE','RV1':'275 VAC','BR1':'MB10S-13','C1':'47n / 400V','L1':'3m3 / EMI','C4':'150n / 630V','U1':'LYT1603D','R5':'0R68 / 0.5W','R6':'3R65','T1':'1m2 / 400V catalogue','D1':'US1J / 600V','C6':'150u / 100V','R8':'68k','R9':'68k','J1':'230 VAC','J2':'20S LED MODULE','C5':'4u7 / 25V','R4':'12k4','R7':'390k / HVR25'}
for c in parts:
 r=c['ref'];x,y,a=pos[r];sid=uid(r)
 if c['kind']=='IC':rx,ry=x,y-23;vx,vy=x,y
 elif c['kind']=='bridge':rx,ry=x,y-12;vx,vy=x,y+12
 elif a==270:rx,ry=x+9,y-2.54;vx,vy=x+10,y+3.81
 else:rx,ry=x,y-6.35;vx,vy=x,y+6.35
 if r=='T1':rx,ry=x,y-10.16;vx,vy=x,y+13.97
 if r=='J1':rx,ry=x-5.08,y-6.35;vx,vy=x,y+12.7
 if r=='J2':rx,ry=x,y-6.35;vx,vy=x-2.54,y+16.51
 if r in ['C1','C4','C6']:rx,ry=x+8.89,y-2.54;vx,vy=x+10.16,y+3.81
 items.append(f'(symbol(lib_id {q(maps[r]["library_id"])})(at {x} {y} {a})(unit 1)(exclude_from_sim no)(in_bom yes)(on_board yes)(dnp no)(uuid "{sid}")'+prop('Reference',r,rx,ry)+prop('Value',values[r],vx,vy)+prop('Footprint',fpids.get(r,''),x,y,True)+prop('Datasheet',c['source'],x,y,True)+prop('MPN',c['mpn'],x,y,True)+''.join(f'(pin {q(n)}(uuid "{uid(r+"pin"+n)}"))' for n in c['pins'])+f'(instances(project "SC09_compact"(path "/{sheet}"(reference "{r}")(unit 1)))))')
# Main energy paths, explicit common source connections, and parallel sense resistors.
route(pp('J1','1'),pp('RF1','1'));route(pp('RF1','2'),pp('BR1','2'))
route(pp('J1','2'),(34.29,59.69),(34.29,92.71),(78.74,92.71),(78.74,62.23),pp('BR1','4'))
route((68.58,57.15),pp('RV1','1'));route(pp('RV1','2'),(68.58,92.71))
route(pp('BR1','1'),pp('L1','1'));route((124.46,57.15),pp('C1','1'))
route(pp('L1','2'),(170.18,57.15),(184.15,57.15),(203.2,57.15),(203.2,60.96),pp('U1','4'));route((170.18,57.15),pp('C4','1'))
for n in ['5','6','7','8']:route(pp('U1',n),(241.3,pp('U1',n)[1]))
route((241.3,57.15),(241.3,64.77));route((241.3,57.15),pp('R5','1'))
route((247.65,57.15),(247.65,76.2),pp('R6','1'));route(pp('R5','2'),pp('T1','2'));route(pp('R6','2'),(273.05,76.2),(273.05,57.15))
route((278.13,57.15),pp('D1','1'));route(pp('T1','1'),pp('J2','1'))
for r in ['C6','R8','R9']:route((pp(r,'1')[0],57.15),pp(r,'1'))
for r,n in [('BR1','3'),('C1','2'),('C4','2'),('D1','2'),('C6','2'),('R8','2'),('R9','2')]:
 point=pp(r,n);stub(r,n,'DC_RETURN',(point[0],point[1]+7.62))
stub('J2','2','DC_RETURN',(388.62,68.58))
stub('U1','1','BP',(218.44,43.18),'left')
route(pp('U1','2'),(218.44,83.82),(208.28,83.82));label('M',(208.28,83.82),'left')
route(pp('U1','3'),(226.06,96.52),(233.68,96.52));label('FB_INDUCTOR',(233.68,96.52))
for r,n,net in [('R7','1','M'),('R7','2','LED_PLUS'),('R4','1','M'),('R4','2','SW_SOURCE'),('C5','1','BP'),('C5','2','SW_SOURCE')]:
 point=pp(r,n);stub(r,n,net,(point[0]+(-7.62 if n=='1' else 7.62),point[1]),'left' if n=='1' else 'right')
for net,point in [('AC_L',(38.1,57.15)),('AC_FUSED',(73.66,57.15)),('AC_N',(40.64,92.71)),('BUS_RECT',(114.3,57.15)),('BUS_FILTERED',(184.15,57.15)),('SW_SOURCE',(247.65,57.15)),('FB_INDUCTOR',(281.94,57.15)),('LED_PLUS',(312.42,57.15))]:label(net,point)
for x,y in [(68.58,57.15),(68.58,92.71),(124.46,57.15),(170.18,57.15),(241.3,59.69),(241.3,62.23),(247.65,57.15),(273.05,57.15),(278.13,57.15),(330.2,57.15),(351.79,57.15),(372.11,57.15)]:items.append(f'(junction(at {x} {y})(diameter 0)(color 0 0 0 0)(uuid "{uid("junction"+str((x,y)))}"))')
# Actual bridge/filter feed drives U1 D. A source declaration, not an ERC waiver.
power=Path('C:/Program Files/KiCad/10.0/share/kicad/symbols/power.kicad_sym').read_text(encoding='utf-8');st=power.index('\n\t(symbol "PWR_FLAG"');en=power.index('\n\t)',st)+len('\n\t)');flag=power[st:en]
save(S/'PowerFlags.kicad_sym','(kicad_symbol_lib(version 20241209)(generator "kicad_symbol_editor")'+flag+')')
items.append(f'(symbol(lib_id "power:PWR_FLAG")(at 184.15 57.15 0)(unit 1)(exclude_from_sim no)(in_bom no)(on_board no)(dnp no)(uuid "{uid("flag")}")'+prop('Reference','#FLG01',184.15,52.07,True)+prop('Value','PWR_FLAG',184.15,50.8,True)+f'(pin "1"(uuid "{uid("flagpin")}"))(instances(project "SC09_compact"(path "/{sheet}"(reference "#FLG01")(unit 1)))))')
note('VELLUNEO SC09-CAT01 | CATALOGUE NON-ISOLATED LED DRIVER | WORKING SCHEMATIC',15,16,2)
note('230 VAC / 50 Hz | 207-253 V screen | total ~135 mA, LED ~133 mA / 60 V / ~8 W LED | 4000 K, CRI >=80',15,24,1.3)
note('1. Fused input / MOV / bridge / EMI filter',15,35,1.5);note('2. High-side buck / current sense / base reservoir',206,35,1.5)
note('3. Output-voltage monitor / BP supply',116,136,1.5)
note('T1: catalogue MSS1210H-125KED, 1.2mH / 400V, two SMD terminals. No custom winding; NOT an isolation transformer.',15,200,1.2)
note('R5 || R6 = 0.57321 ohm. Estimated total = 135.2 mA; LED ~133.4 mA at 60 V after bleeders; actual corners unmeasured.',15,208,1.2)
note('C6 100 V. Static OVP nominal 77.9 V; dynamic COUT target <=90 V remains unverified. Dual 68k bleeders: one-open screen 36.45 s, 90 to 5 V.',15,216,1.2)
note('All nets and LED terminals are MAINS REFERENCED, NOT SELV. Replace LED module only deenergized with verified discharge. No powered hot-plug.',15,228,1.3)
note('LAB PROTOTYPE: owner authorized continued schematic/PCB design. Insulation, manufacturing release and powered tests remain unqualified.',15,237,1.3)
note('Before acceptance: environment/lifetime/optical assumptions, insulation/test basis, endpoint envelopes, current/OVP/fault corner review.',15,246,1.2)
note('Catalogue T1/L1/HVR25 and manufacturer lands; manual lead forming for RF1/R7/C6. Stock/thermal/fault qualification remain separate.',15,255,1.2)
embedded=lib[lib.index('(symbol '):lib.rfind(')')]
for c in parts:embedded=embedded.replace('(symbol "SC09_'+c['ref']+'"','(symbol "E27SC09:SC09_'+c['ref']+'"',1)
save(S/'SC09_compact.kicad_sch',f'(kicad_sch(version 20250114)(generator "eeschema")(uuid "{sheet}")(paper "A3")(title_block(title "Velluneo SC09-CAT01 catalogue driver working schematic")(date "2026-11-21")(rev "SC09-CAT01 engineering"))(lib_symbols{embedded}{flag.replace(chr(34)+"PWR_FLAG"+chr(34),chr(34)+"power:PWR_FLAG"+chr(34),1)})'+''.join(items)+')')
save(S/'sym-lib-table','(sym_lib_table\n(version 7)\n(lib (name "E27SC09")(type "KiCad")(uri "${KIPRJMOD}/E27SC09.kicad_sym")(options "")(descr "SC09 exact physical pins, unassigned footprints"))\n(lib (name "power")(type "KiCad")(uri "${KIPRJMOD}/PowerFlags.kicad_sym")(options "")(descr "Actual bridge/filter power feed"))\n)')
save(S/'symbol-pin-verification.json',{'kind':'Exact physicalpin symbols; not footprint or functionalqualification','engineering_intent_digest':dg,'symbols':maps,'U1_type_basis':'Dpower_in startup/regulatorfeed;BPpower_out internalregulator;M/FBinputs;SpassivecommonMOSFET/referenceconductionterminals. Not allpassive and not overrides.','PWR_FLAG_basis':'BR1rectifiedoutput through actualL1filter feedsU1D; one virtualflag BUS_FILTERED, not an invented externalrail.','footprints':'Assigned manufacturer lands and custom coil/forming contracts; physical qualification remains open.','parts_reports':{'active':'reference/active-parts-report.json','passive':'reference/passive-parts-report.json'},'native_component_count':19,'physicalpins':46,'NC':0})
print('Generated19symbols/46pinscatalogueSC09schematic;schematic updated independently of existing PCB')


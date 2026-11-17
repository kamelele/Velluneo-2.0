#!/usr/bin/env python3
"""Deterministic native KiCad draft capture from an independently approved pin contract.
Does not create/approve expected intent, fabricate footprints, or generate a PCB.
"""
from pathlib import Path
import json,uuid,csv,hashlib
P=Path(__file__).resolve().parent.parent
D=P/'schematic-capture';L=P/'libraries';L.mkdir(exist_ok=True)
NAME='Velluneo_specification_reset'
parts=json.loads((P/'schematic-intent/parts.json').read_text())
intent=json.loads((P/'schematic-intent/intended-connectivity.json').read_text())
digest=hashlib.sha256(json.dumps({k:v for k,v in intent.items() if k!='approval'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
assert intent['approval']['intent_digest']==digest=='b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'velluneo-driver-sch-r1/'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def fmt(n):return f'{n:.4f}'.rstrip('0').rstrip('.') if n else '0'
def effects(sz=1,hide=False,justify=''):
 return f'(effects (font (size {sz} {sz}))'+(f' (justify {justify})' if justify else '')+(' hide' if hide else '')+')'
def prop(n,v,x=0,y=0,hide=True,sz=1):return f'(property {q(n)} {q(v)} (at {fmt(x)} {fmt(y)} 0) {effects(sz,hide)})'
def line(points,w=.254):return '(polyline (pts '+''.join(f'(xy {fmt(x)} {fmt(y)})' for x,y in points)+f') (stroke (width {w}) (type default)) (fill (type none)))'
def rect(x1,y1,x2,y2):return f'(rectangle (start {x1} {y1}) (end {x2} {y2}) (stroke (width .254) (type default)) (fill (type background)))'
def circle(x,y,r):return f'(circle (center {x} {y}) (radius {r}) (stroke (width .15) (type default)) (fill (type outline)))'
def pin(n,name,x,y,angle=0,typ='passive',length=2.54):return {'n':str(n),'name':name,'x':x,'y':y,'angle':angle,'typ':typ,'length':length}
def pinsex(p):return f'(pin {p["typ"]} line (at {p["x"]} {p["y"]} {p["angle"]}) (length {p["length"]}) (name {q(p["name"])} {effects(.9)}) (number {q(p["n"])} {effects(.9)}))'
def two(names=('~','~')):return [pin('1',names[0],-7.62,0,length=5.08),pin('2',names[1],7.62,0,180,length=5.08)]
syms={}
syms['R']=(two(),rect(-2.54,1.016,2.54,-1.016),'R')
syms['FUSE']=(two(),rect(-2.54,1.27,2.54,-1.27)+line([(-2.54,0),(2.54,0)],.15),'F')
syms['C']=(two(),line([(-2.54,0),(-.762,0)])+line([(.762,0),(2.54,0)])+line([(-.762,2.54),(-.762,-2.54)])+line([(.762,2.54),(.762,-2.54)]),'C')
syms['CP']=(two(('+','-')),syms['C'][1]+line([(-3.556,3.048),(-1.524,3.048)],.15)+line([(-2.54,2.032),(-2.54,4.064)],.15),'C')
syms['D']=(two(('K','A')),line([(-2.54,0),(-1.27,0)])+line([(-1.27,2.032),(-1.27,-2.032)])+line([(-1.27,0),(1.27,2.032),(1.27,-2.032),(-1.27,0)])+line([(1.27,0),(2.54,0)]),'D')
syms['TVS']=(two(('K','A')),syms['D'][1]+line([(-2.032,2.032),(-1.27,2.032),(-1.27,-2.032),(-.508,-2.032)]),'D')
syms['NTC']=(two(),syms['R'][1]+line([(-3.81,-2.54),(3.81,2.54),(5.08,2.54)],.15),'RT')
syms['WIRE2']=([pin('1','1',-7.62,2.54,length=2.54),pin('2','2',-7.62,-2.54,length=2.54)],rect(-5.08,5.08,2.54,-5.08)+circle(-2.54,2.54,.762)+circle(-2.54,-2.54,.762)+line([(-5.08,2.54),(-3.302,2.54)])+line([(-5.08,-2.54),(-3.302,-2.54)]),'J')
syms['MB10S']=([pin('4','AC',-10.16,5.08,length=2.54),pin('2','AC',-10.16,-5.08,length=2.54),pin('1','+',10.16,5.08,180),pin('3','-',10.16,-5.08,180)],rect(-7.62,7.62,7.62,-7.62),'BR')
syms['UCC28711']=([pin('1','VDD',-12.7,7.62,typ='power_in',length=5.08),pin('2','VS',-12.7,2.54,typ='input',length=5.08),pin('3','NTC',-12.7,-2.54,typ='input',length=5.08),pin('4','GND',-12.7,-7.62,typ='power_in',length=5.08),pin('7','HV',12.7,7.62,180,typ='power_in',length=5.08),pin('6','DRV',12.7,-2.54,180,typ='output',length=5.08),pin('5','CS',12.7,-7.62,180,typ='input',length=5.08)],rect(-7.62,10.16,7.62,-10.16),'U')
syms['STN1NK80Z']=([pin('1','G',-10.16,0,typ='input',length=5.08),pin('2','D',0,10.16,270,length=5.08),pin('3','S',0,-10.16,90,length=5.08),pin('4','D_TAB',5.08,10.16,270,length=5.08)],line([(-5.08,0),(-2.54,0)])+line([(-2.54,3.81),(-2.54,-3.81)])+line([(-1.27,3.81),(-1.27,-3.81)])+line([(-1.27,2.54),(0,2.54),(0,5.08),(5.08,5.08)])+line([(-1.27,-2.54),(0,-2.54),(0,-5.08)]),'Q')
tp=[pin('1','P_DOT',-12.7,7.62,length=7.62),pin('5','P_END',-12.7,-7.62,length=7.62),pin('6','S_DOT',12.7,7.62,180,length=7.62),pin('10','S_END',12.7,-7.62,180,length=7.62),pin('2','A_DOT',-12.7,-20.32,length=7.62),pin('4','A_END',-12.7,-30.48,length=7.62)]
tg=line([(-.762,10.16),(-.762,-10.16)])+line([(.762,10.16),(.762,-10.16)])
for x,top,count,sgn in [(-5.08,7.62,6,1),(5.08,7.62,6,-1),(-5.08,-20.32,4,1)]:
 for i in range(count):
  y=top-i*2.54;tg+=f'(arc (start {x} {fmt(y)}) (mid {fmt(x+sgn*2.54)} {fmt(y-1.27)}) (end {x} {fmt(y-2.54)}) (stroke (width .254) (type default)) (fill (type none)))'
 tg+=circle(x-sgn*1.27,top+.762,.508)
for i,n in enumerate(['3','7','8','9']):tp.append(pin(n,'UNWOUND',12.7,-20.32-i*5.08,180,length=2.54));tg+=circle(10.16,-20.32-i*5.08,.508)
for pp in tp: pp['name']='~'
syms['CUSTOM_EFD25']=(tp,tg,'T')
syms['POWER_SOURCE']=([pin('1','~',0,0,90,typ='power_out',length=0)],line([(0,0),(0,2.54),(-1.27,3.81),(0,5.08),(1.27,3.81),(0,2.54)]),'#FLG')
def library_symbol(name,qualified=False):
 pins,graphics,ref=syms[name];symname='Velluneo_Driver:'+name if qualified else name
 return f'(symbol {q(symname)} '+('(power) ' if name=='POWER_SOURCE' else '')+f'(pin_names (offset .5)) (in_bom yes) (on_board yes) '+prop('Reference',ref,0,5.08,False)+prop('Value',name,0,-5.08,False)+prop('Footprint','')+f'(symbol {q(name+"_0_1")} {graphics})'+f'(symbol {q(name+"_1_1")} '+''.join(pinsex(p) for p in pins)+'))'
(L/'Velluneo_Driver.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "velluneo_capture")\n'+ '\n'.join(library_symbol(k) for k in syms)+'\n)\n')
(P/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "Velluneo_Driver") (type "KiCad") (uri "${KIPRJMOD}/libraries/Velluneo_Driver.kicad_sym") (options "") (descr "Source-derived local driver symbols; footprints pending qualification")))\n')
positions={
'J1':(30.48,50.8),'F1':(76.2,40.64),'RIN':(129.54,40.64),'BR1':(157.48,66.04),'CBULK':(45.72,91.44),'RB1':(96.52,91.44),'RB2':(152.4,91.44),
'T1':(246.38,50.8),'DCL':(226.06,106.68),'TVS1':(266.7,106.68),'Q1':(241.3,132.08),'RCS':(241.3,156.21),
'DOUT':(332.74,43.18),'COUT':(332.74,76.2),'J2':(381,55.88),'RBO1':(327.66,111.76),'RBO2':(381,111.76),
'U1':(63.5,162.56),'RVS1':(139.7,134.62),'RVS2':(139.7,160.02),'RLC':(139.7,185.42),'RT1':(139.7,210.82),'RG':(55.88,218.44),'RGS':(55.88,241.3),
'DAUX':(241.3,195.58),'RAUX':(317.5,195.58),'CV1':(241.3,231.14),'CV2':(317.5,231.14)}
styles={ref:('R' if ref.startswith('R') else 'D' if ref in ['DCL','DAUX','DOUT'] else 'WIRE2' if ref.startswith('J') else 'CP' if ref in ['CBULK','COUT'] else 'C' if ref.startswith('CV') else 'FUSE' if ref=='F1' else {'BR1':'MB10S','U1':'UCC28711','Q1':'STN1NK80Z','T1':'CUSTOM_EFD25','TVS1':'TVS'}[ref]) for ref in positions}
styles['RT1']='NTC'
vals={'RIN':'47R / AC05','RB1':'499k','RB2':'499k','RVS1':'80.6k','RVS2':'17.4k','RLC':'1.40k','RCS':'2.37R','RG':'4.7R','RGS':'47k','RAUX':'4.7R','RBO1':'20k','RBO2':'20k','RT1':'100k / B4100','CBULK':'15u / 450V','COUT':'10u / 63V HYBRID','CV1':'470n / 50V C0G','CV2':'470n / 50V C0G','F1':'250mA / 277VAC','T1':'120:30:22 / 2.304mH','J1':'E27 INTERNAL WIRES','J2':'INTERNAL LED WIRES'}
suppressed={('J1','1'),('J1','2'),('F1','1'),('F1','2'),('RIN','1'),('RIN','2'),('BR1','2'),('BR1','4'),('RB1','2'),('RB2','1'),('Q1','2'),('Q1','4'),('DCL','1'),('DCL','2'),('TVS1','1'),('DAUX','1'),('RAUX','1'),('CV1','1'),('CV2','1'),('CV2','2')}
for rr in ['J2','RBO1','RBO2']:suppressed.update((rr,n) for n in ['1','2'])
suppressed.add(('COUT','1'))
rootuid=uid('root');items=[]
def text(s,x,y,size=1.2):items.append(f'(text {q(s)} (at {x} {y} 0) {effects(size,False,"left")} (uuid {q(uid("text/"+s))}))')
def wire(x,y,xx,yy,key):items.append(f'(wire (pts (xy {fmt(x)} {fmt(y)}) (xy {fmt(xx)} {fmt(yy)})) (stroke (width 0) (type default)) (uuid {q(uid("wire/"+key))}))')
def label(n,x,y,angle,key):items.append(f'(label {q(n)} (at {fmt(x)} {fmt(y)} {angle}) {effects(.9,False,"left bottom")} (uuid {q(uid("label/"+key))}))')
for a in parts:
 ref=a['ref'];x,y=positions[ref];style=styles[ref];pins=syms[style][0]
 assert {p['n'] for p in pins}==set(a['pins'])
 yoff=20.32 if ref=='U1' else 15.24 if ref=='Q1' else 12.7 if ref in ['BR1','T1'] else 8.89 if ref in ['J1','J2'] else 5.08
 value=vals.get(ref,a['mpn']);rx=x+15.24 if ref=='Q1' else x; ry=y-2.54 if ref=='Q1' else y-yoff; vx=x+15.24 if ref=='Q1' else x;vy=y+2.54 if ref=='Q1' else y+yoff
 items.append(f'(symbol (lib_id {q("Velluneo_Driver:"+style)}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid(ref))}) '+prop('Reference',ref,rx,ry,False,1.2)+prop('Value',value,vx,vy,False,.95)+prop('Footprint','',x,y)+prop('MPN',a['mpn'],x,y)+prop('Description',a['value'],x,y)+prop('Library_Status','Symbol pin basis checked; physical footprint pending',x,y)+''.join(f'(pin {q(pp["n"])} (uuid {q(uid(ref+"/pin/"+pp["n"]))}))' for pp in pins)+f'(instances (project {q(NAME)} (path {q("/"+rootuid)} (reference {q(ref)}) (unit 1)))))')
 for pp in pins:
  n=pp['n'];net=a['pins'][n];px=x+pp['x'];py=y-pp['y'];ang=pp['angle'];k=ref+'/'+n
  if net is None:items.append(f'(no_connect (at {fmt(px)} {fmt(py)}) (uuid {q(uid("nc/"+k))}))');continue
  if (ref,n) in suppressed:continue
  # Label short wire stubs. Rotations follow native local pin frame (screen Y inverted).
  if ang==0:ex,ey=px-5.08,py;la=180
  elif ang==180:ex,ey=px+5.08,py;la=0
  elif ang==270:ex,ey=px,py-5.08;la=90
  else:ex,ey=px,py+5.08;la=90
  wire(px,py,ex,ey,k);label(net,ex,ey,la,k)
# Non-physical power-source declarations. They document actual passive source paths,
# retain truthful U1 power_in pins, and do not appear in physical XML component/pin sets.
# Native comparison verifies this independently; no expected graph change is made.
for ref,x,y,net,target in [('#FLG01',38.1,81.28,'BULK_POS',(38.1,91.44)),('#FLG02',60.96,101.6,'PRIMARY_GND',(53.34,91.44)),('#FLG03',330.2,190.5,'VDD',(330.2,195.58))]:
 items.append(f'(symbol (lib_id "Velluneo_Driver:POWER_SOURCE") (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid {q(uid(ref))}) '+prop('Reference',ref,x,y,True)+prop('Value','SOURCE',x,y-7.62,False,.75)+prop('Footprint','',x,y)+f'(pin "1" (uuid {q(uid(ref+"/pin/1"))})) (instances (project {q(NAME)} (path {q("/"+rootuid)} (reference {q(ref)}) (unit 1)))))')
 tx,ty=target
 if x!=tx:wire(x,y,x,ty,ref+'/vertical');wire(x,ty,tx,ty,ref+'/horizontal')
 else:wire(x,y,tx,ty,ref+'/vertical')
# Explicit local wires show current paths; global labels link distant functional blocks.
paths=[
 [(22.86,48.26),(45.72,48.26),(45.72,40.64),(68.58,40.64)],
 [(83.82,40.64),(121.92,40.64)],
 [(137.16,40.64),(147.32,40.64),(147.32,60.96)],
 [(22.86,53.34),(40.64,53.34),(40.64,71.12),(147.32,71.12)],
 [(104.14,91.44),(144.78,91.44)],
 [(233.68,58.42),(203.2,58.42),(203.2,116.84),(241.3,116.84),(241.3,121.92)],
 [(241.3,116.84),(246.38,116.84),(246.38,121.92)],
 [(233.68,106.68),(233.68,111.76),(203.2,111.76)],
 [(218.44,106.68),(218.44,99.06),(259.08,99.06),(259.08,106.68)],
 [(241.3,142.24),(241.3,148.59),(218.44,148.59),(218.44,156.21),(233.68,156.21)],
 [(325.12,43.18),(307.34,43.18),(307.34,121.92)],
 [(325.12,76.2),(307.34,76.2)],
 [(320.04,111.76),(307.34,111.76)],
 [(373.38,111.76),(373.38,121.92),(307.34,121.92)],
 [(373.38,53.34),(360.68,53.34),(360.68,33.02),(307.34,33.02),(307.34,43.18)],
 [(340.36,76.2),(396.24,76.2)],
 [(388.62,111.76),(396.24,111.76),(396.24,58.42),(396.24,66.04)],
 [(335.28,111.76),(347.98,111.76),(347.98,86.36),(396.24,86.36)],
 [(373.38,58.42),(365.76,58.42),(365.76,66.04),(396.24,66.04)],
 [(233.68,195.58),(222.25,195.58),(222.25,208.28),(309.88,208.28),(309.88,195.58)],
 [(325.12,195.58),(340.36,195.58),(340.36,218.44),(220.98,218.44),(220.98,231.14),(233.68,231.14)],
 [(309.88,231.14),(309.88,218.44)],
 [(248.92,231.14),(271.78,231.14),(271.78,246.38),(355.6,246.38),(355.6,231.14),(325.12,231.14)],
]
for i,pts in enumerate(paths):
 for j,(a,b) in enumerate(zip(pts,pts[1:])):wire(*a,*b,f'local/{i}/{j}')
# Only actual same-net branch points have junction markers.
for x,y in [(241.3,116.84),(203.2,111.76),(307.34,43.18),(307.34,76.2),(307.34,111.76),(396.24,76.2),(396.24,86.36),(396.24,66.04),(309.88,218.44)]:
 items.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid {q(uid("junction/"+str((x,y))))}))')
text('1  MAINS INPUT / PRIMARY BUFFER',16.51,25.4,1.5)
text('2  ISOLATED FLYBACK POWER STAGE',196.85,25.4,1.5)
text('3  ISOLATED LED OUTPUT',302.26,25.4,1.5)
text('4  PRIMARY-SIDE CONTROL / SENSING',16.51,118.11,1.5)
text('5  AUXILIARY BIAS / DECOUPLING',205.74,176.53,1.5)
text('PRIMARY GND IS NOT OUTPUT NEGATIVE. Labels join identical named nets only.',17.78,262.89,1.05)
text('DRAFT: NOT FOR MANUFACTURE. Footprints, startup, clamp/SOA, insulation and thermal qualification remain open.',17.78,269.24,1.05)
text('T1 dots: 1 / 2 / 6. Pins 3 / 7 / 8 / 9 are unwound raw-bobbin terminals.',196.85,166.37,.95)
text('J2 is internal wiring, not the final tool-free panel dock.',302.26,141.0,.95)
text('Kelvin sense: RCS top -> RLC; RCS bottom -> U1 GND.',17.78,251.46,.95)
header=f'(kicad_sch (version 20250114) (generator "velluneo_capture") (uuid {q(rootuid)}) (paper "A3") (title_block (title "Velluneo E27 - isolated LED driver") (date "2026-11-17") (rev "SCH-DRAFT-01") (company "Velluneo") (comment 1 "Approved physical-pin intent b6d09476; electrical qualification pending"))'
schematic=header+'\n(lib_symbols\n'+'\n'.join(library_symbol(k,True) for k in syms)+')\n'+'\n'.join(items)+'\n(sheet_instances (path "/" (page "1"))))\n'
(P/(NAME+'.kicad_sch')).write_text(schematic)
pro=P/(NAME+'.kicad_pro')
if not pro.exists():pro.write_text(json.dumps({'meta':{'filename':NAME+'.kicad_pro','version':1}},indent=2)+'\n')
with (D/'BOM.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Quantity','Value','MPN_or_custom_requirement','Symbol','Footprint_status'])
 for a in parts:w.writerow([a['ref'],1,vals.get(a['ref'],a['mpn']),a['mpn'],'Velluneo_Driver:'+styles[a['ref']],'Not selected/qualified; not order-ready'])
print('Generated native schematic, local symbols, project and BOM; approved intent unchanged:',digest)

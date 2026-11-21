from pathlib import Path
import pcbnew as p,json
from c16_sexpr import parse,dumps,children,child,strip_tracks,string
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';E=D/'design';B=E/'Velluneo_driver.kicad_pcb'
removed=strip_tracks(B);b=p.LoadBoard(str(B));fps={f.GetReference():f for f in b.GetFootprints()};f=fps['T1'];origin=f.GetPosition()
assert f.GetOrientationDegrees()==0
coords={'1':(-10,7.62),'2':(-5,7.62),'3':(0,7.62),'5':(10,7.62),'6':(10,-7.62),'7':(5,-7.62),'8':(0,-7.62),'9':(-5,-7.62),'10':(-10,-7.62)}
for pad in f.Pads():
 x,y=coords[pad.GetNumber()];pad.SetPosition(p.VECTOR2I(origin.x+p.FromMM(x),origin.y+p.FromMM(y)))
lib=E/'Velluneo_C16.pretty/MYRRA74032_E25_FACTORY.kicad_mod';t=parse(lib.read_text())
for pad in children(t,'pad'):
 at=child(pad,'at');x,y=coords[string(pad[1])];at[1:3]=[str(x),str(y)]
desc='MYRRA74032 factory E25. CORRECT component-side view: primary south1left/5right, pin4 absent at(+5,+7.62); secondary north10left/6right. Manufacturer pin-plan is bottom view, correlated against primary front elevation.9physicalpins.'
child(t,'descr')[1]=json.dumps(desc);lib.write_text(dumps(t)+'\n',encoding='utf-8',newline='\n');f.SetLibDescription(desc)
for r,x,y,a in [('TVS1',106.9,101.5,0),('D1',100.5,101.4,90),('D2',94,104.2,90),('C3',91.4,103.5,0),('R10',95.5,113,0),('R14',108,108,90),('R4',93,114.5,0),('R17',110.5,116.5,180),('R16',113.7,108,90),('J1',98.5,127.2,0),('R3',103.5,109,90),('RT1',106.5,123,0),('R13',107,120.2,0)]:
 fp=fps[r];fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));fp.SetOrientationDegrees(a)
for r,x,y,a in [('C1',106.8,121.8,180),('C2',96.5,117.5,-90),('R14',105.5,107.5,0),('R4',90,115.5,0),('R17',119,97.8,90),('R16',113.7,107.6,90),('RT1',96,117.5,0),('R13',96,120.5,0),('R2',112.5,114,0),('F1',119.15,110.2,-90),('BR1',118,124,0)]:
 fp=fps[r];fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));fp.SetOrientationDegrees(a)
for r,x,y,a in [('U1',92,116,-90),('C2',92,116,-90),('R6',90.2,119.8,0),('R5',94,119,90),('R9',86.35,120,0),('R4',97.2,112,0),('RT1',97,116.5,0),('R13',97,119.5,0),('R10',99,110.5,90)]:
 fp=fps[r];fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));fp.SetOrientationDegrees(a)
if fps['C1'].GetLayer()!=p.F_Cu:fps['C1'].Flip(fps['C1'].GetPosition(),False)
for r,x,y,a in [('C1',106.3,119.5,180),('C2',92.5,116,-90),('C3',91.6,103.5,0),('R4',96.7,110,0),('R5',94.8,120.2,90),('R13',97.9,122.1,0),('BR1',118.7,124,180),('F1',108,115,0),('R17',116,95.6,0),('R2',112.6,123.6,-90),('TVS1',110,103.5,90),('R16',103.1,109.4,0),('R14',116.5,106,90),('D1',100.3,101.4,90)]:
 fp=fps[r];fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));fp.SetOrientationDegrees(a)
for r,x,y,a in [('C1',106.1,119.25,180),('F1',108,112.4,0),('D1',103.8,100.1,90),('R16',103,106,0),('R4',94.6,108,0),('R14',116.5,104.8,90)]:
 fp=fps[r];fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));fp.SetOrientationDegrees(a)
p.SaveBoard(str(B),b)
record=dict(correction='C16-RC/CHANGE T1 mirror defect: maker pin-plan is bottom view; front elevation1left/5right establishes component-side coordinates.',component_side_coordinates_mm={str(pad.GetNumber()):[p.ToMM(pad.GetPosition().x-origin.x),p.ToMM(pad.GetPosition().y-origin.y)]for pad in f.Pads()},absent_pin4_mm=[5,7.62],physical_pin_count=9,source='https://www.atd-shop.com/www/prilohy/74032-datasheet.pdf',electrical_pin_intent_unchanged=True,removed_routes_for_complete_reroute=removed,scope='Source-correlated drawing interpretation; actual first-fit remains required.')
(D/'checks/T1-view-correction.json').write_text(json.dumps(record,indent=2)+'\n');print('T1 mirror corrected; reroute required')

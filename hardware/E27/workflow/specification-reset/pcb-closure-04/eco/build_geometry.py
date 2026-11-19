"""Unapplied component/terminal ECO coupons, NOT a functional replacement supply."""
from pathlib import Path
import json,math,hashlib,copy
import pcbnew
D=Path(__file__).resolve().parent;P=D.parents[1];ROOT=D.parent;L=D/'Velluneo_ECO04.pretty';L.mkdir(exist_ok=True)
def module(name,pads,court,fab,descr):
 s=f'(footprint "{name}" (version 20241229) (generator "velluneo_eco04") (layer "F.Cu") (descr "{descr}") '
 s+='(attr '+('through_hole'if any(p[-1]for p in pads)else'smd')+')'
 s+='(property "Reference" "REF**" (at 0 -8) (layer "F.SilkS") (effects (font (size 1 1) (thickness .12))))'
 s+=f'(property "Value" "{name}" (at 0 9) (layer "F.Fab") (effects (font (size 1 1))))'
 for bb,layer in((court,'F.CrtYd'),(fab,'F.Fab')):s+=f'(fp_rect (start {bb[0]} {bb[1]}) (end {bb[2]} {bb[3]}) (stroke (width .05) (type default)) (fill none) (layer "{layer}"))'
 for n,x,y,w,h,drill in pads:
  if drill:s+=f'(pad "{n}" thru_hole circle (at {x} {y}) (size {w} {h}) (drill {drill}) (layers "*.Cu" "*.Mask"))'
  else:s+=f'(pad "{n}" smd rect (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask"))'
 s+=')\n';(L/(name+'.kicad_mod')).write_text(s,encoding='utf-8',newline='\n')
module('UCC28701_DBV_Native',[(1,-1.3,-.95,1.1,.6,0),(2,-1.3,0,1.1,.6,0),(3,-1.3,.95,1.1,.6,0),(6,1.3,-.95,1.1,.6,0),(5,1.3,0,1.1,.6,0),(4,1.3,.95,1.1,.6,0)],[-2.1,-1.55,2.1,1.55],[-.8,-1.45,.8,1.45],'TI DBV0006A native land example; UCC28701 new controller requires full circuit revalidation')
module('W10G_Formed5p5_PROJECT',[(1,-2.75,-2.75,2,2,1.2),(2,2.75,-2.75,2,2,1.2),(3,2.75,2.75,2,2,1.2),(4,-2.75,2.75,2,2,1.2)],[-5.43,-5.43,5.43,5.43],[-4.93,-4.93,4.93,4.93],'PROJECT formed5.5mm grid, not native fixed pitch; polarity datum plus lead NW, AC NE and SW, minus SE; process unqualified')
module('STF2N80K5_Stagger5p08_PROJECT',[(1,-2.54,0,2.2,2.2,1.5),(2,0,5.08,2.2,2.2,1.5),(3,2.54,0,2.2,2.2,1.5)],[-5.7,-5.1,5.7,6.68],[-5.2,-4.6,5.2,0],'PROJECT formed lead stagger G1 D2 S3; root clearance, bend radius, seating and jig unqualified')
src=P/'libraries/Velluneo_Driver.pretty/TDK_B66422W1010D001_EFD25_RAW_CANDIDATE.kicad_mod';s=src.read_text(encoding='utf-8');assert s.count('(size 2.4 2.4)')==10
s=s.replace('TDK_B66422W1010D001_EFD25_RAW_CANDIDATE','TDK_EFD25_Pad2p0_PROJECT').replace('(size 2.4 2.4)','(size 2.0 2.0)');(L/'TDK_EFD25_Pad2p0_PROJECT.kicad_mod').write_text(s,encoding='utf-8',newline='\n')
parts=json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'));by={p['ref']:p for p in parts}
by['U1'].update(mpn='UCC28701DBVR',value='PROPOSED no-HV NTC PSR controller',pins={'1':'NTC','2':'VDD','3':'DRV','4':'CS','5':'PRIMARY_GND','6':'VS'})
by['Q1'].update(mpn='STF2N80K5',value='PROPOSED 800V TO220FP formed terminals',pins={'1':'GATE','2':'DRAIN','3':'SENSE'})
by['BR1'].update(mpn='W10G-E4/51',value='PROPOSED 1000V bridge, formed grid')
by['R9'].update(mpn='CRCW12062R32FKEA',value='PROPOSED 2.32ohm, E96; procurement unconfirmed')
by['R13'].update(mpn='CRCW060380K6FKEA',value='PROPOSED 80.6kohm VDD feed bleeder')
parts.extend([dict(ref='R16',mpn='CRCW2512402KFKEG',value='PROPOSED 402kohm startup',pins={'1':'BULK_POS','2':'STARTUP_MID'}),dict(ref='R17',mpn='CRCW2512402KFKEG',value='PROPOSED 402kohm startup',pins={'1':'STARTUP_MID','2':'VDD'})])
assert len(parts)==33 and sum(len(p['pins'])for p in parts)==81
(D/'proposed-parts.json').write_text(json.dumps(parts,indent=2)+'\n',encoding='utf-8',newline='\n')
mapping={'U1':'UCC28701_DBV_Native','BR1':'W10G_Formed5p5_PROJECT','Q1':'STF2N80K5_Stagger5p08_PROJECT','T1':'TDK_EFD25_Pad2p0_PROJECT'}
board=pcbnew.BOARD();board.SetCopperLayerCount(2);board.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(1.6))
aliases=json.loads((ROOT/'checks/board-parity.json').read_text(encoding='utf-8'))['logical_to_native_netnames'];nets={}
for p in parts:
 for n in p['pins'].values():
  if n is not None and n not in nets:
   net=pcbnew.NETINFO_ITEM(board,aliases.get(n,'/'+n));board.Add(net);nets[n]=net
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
for ref,(x,y)in {'U1':(20,20),'BR1':(50,20),'Q1':(85,20),'T1':(60,60)}.items():
 fp=pcbnew.FootprintLoad(str(L),mapping[ref]);assert fp;fp.SetReference(ref);fp.SetValue(by[ref]['mpn']);fp.SetFPID(pcbnew.LIB_ID('Velluneo_ECO04',mapping[ref]));fp.SetPosition(pt(x,y));board.Add(fp)
 for pad in fp.Pads():
  n=by[ref]['pins'][pad.GetNumber()]
  if n is None:
   net=pcbnew.NETINFO_ITEM(board,f'unconnected-(T1-Pad{pad.GetNumber()})');board.Add(net);pad.SetNet(net)
  else:pad.SetNet(nets[n])
 fp.Reference().SetTextSize(pt(1,1));fp.Reference().SetTextThickness(pcbnew.FromMM(.12));fp.Reference().SetPosition(pt(x,y-9));fp.Reference().SetVisible(True)
for a,b in [((3,3),(112,3)),((112,3),(112,80)),((112,80),(3,80)),((3,80),(3,3))]:
 e=pcbnew.PCB_SHAPE();e.SetShape(pcbnew.SHAPE_T_SEGMENT);e.SetLayer(pcbnew.Edge_Cuts);e.SetStart(pt(*a));e.SetEnd(pt(*b));e.SetWidth(pcbnew.FromMM(.05));board.Add(e)
text=pcbnew.PCB_TEXT(board);text.SetText('UNAPPLIED ECO LAND COUPONS - NOT A FUNCTIONAL POWER SUPPLY');text.SetLayer(pcbnew.F_SilkS);text.SetTextSize(pt(.9,.9));text.SetTextThickness(pcbnew.FromMM(.12));text.SetPosition(pt(57,7));board.Add(text)
path=D/'ECO04_land_geometry.kicad_pcb';pcbnew.SaveBoard(str(path),board)
rules=(ROOT/'Velluneo_specification_reset.kicad_dru').read_text(encoding='utf-8')
for k in('A','B'):rules=rules.replace(f"{k}.NetName == '/BULK_POS'",f"({k}.NetName == '/BULK_POS' || {k}.NetName == '/STARTUP_MID')")
(D/'ECO04_land_geometry.kicad_dru').write_text(rules,encoding='utf-8',newline='\n')
(D/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Velluneo_ECO04") (type "KiCad") (uri "${KIPRJMOD}/Velluneo_ECO04.pretty") (options "") (descr "Unapplied proposed ECO land geometry")) (lib (name "Velluneo_Driver") (type "KiCad") (uri "${KIPRJMOD}/libraries/Velluneo_Driver.pretty") (options "") (descr "Retained passive lands")))\n',encoding='utf-8',newline='\n')
(D/'ECO04_land_geometry.kicad_pro').write_text(json.dumps({'board':{'design_settings':{'rules':{'min_clearance':.25,'min_track_width':.3,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_copper_edge_clearance':.5}}}},indent=2)+'\n',encoding='utf-8',newline='\n')
rows=[dict(object='BR1 formed adjacent lands',nominal_gap_mm=3.5,annulus_mm=.4,qualified=False),dict(object='Q1 formed G-D and D-S',nominal_gap_mm=math.hypot(2.54,5.08)-2.2,annulus_mm=.35,qualified=False),dict(object='T1 adjacent project lands',nominal_gap_mm=3.,annulus_mm=.325,qualified=False),dict(object='U1 former HV-DRV pair',nominal_gap_mm=None,reason='High-voltage pin physically absent on new controller; real circuit/startup ECO, not a new net label',qualified=False)]
(D/'geometry-contract.json').write_text(json.dumps(dict(status='Unapplied proposal',part_count_proposed=33,pads_proposed=81,coupon_footprints=4,coupon_pads=23,pairs=rows,pin_mapping=mapping,scope='These isolated land coupons are not a complete placed/functional33-part driver. No routing/safety/assembly or source-process approval. Original driver remains31parts/79pads and retains its8clearance failures.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(proposed_parts=33,proposed_pads=81,coupon_footprints=4,coupon_pads=23,saved=str(path),functional_board=False)))

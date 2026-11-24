from pathlib import Path
import sys,json,hashlib,xml.etree.ElementTree as ET,zipfile
import pcbnew as k
H=Path(__file__).resolve().parent;ROOT=H.parents[1];C=H/'candidate';P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def geometry(p):
 b=k.LoadBoard(str(p));b.BuildConnectivity()
 pads=sorted((f.GetReference(),p.GetNumber(),p.GetLayer(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y,p.GetShape(),p.GetNetname(),tuple(p.GetLayerSet().Seq()))for f in b.GetFootprints()for p in f.Pads())
 tracks=sorted((t.m_Uuid.AsString(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth(k.F_Cu)if isinstance(t,k.PCB_VIA)else t.GetWidth(),t.GetLayer(),t.GetNetname(),t.GetDrillValue()if isinstance(t,k.PCB_VIA)else None)for t in b.GetTracks())
 edges=sorted((x.m_Uuid.AsString(),x.GetShape(),x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y,x.GetWidth())for x in b.GetDrawings()if x.GetLayer()==k.Edge_Cuts)
 return {'pads':pads,'tracks_vias':tracks,'outline':edges,'unconnected':b.GetConnectivity().GetUnconnectedCount(False),'zone_count':len(list(b.Zones()))}
old=geometry(P/'SC09_compact.kicad_pcb');new=geometry(C/'SC09_compact.kicad_pcb');assert old==new
expected={ref+'.'+pin:net for c in json.loads((P/'bom-build.json').read_text())['components']for ref in [c['ref']]for pin,net in c['pins'].items()}
actual={node.get('ref')+'.'+node.get('pin'):net.get('name').lstrip('/')for net in ET.parse(H/'native-final2/netlist.xml').findall('./nets/net')for node in net.findall('node')};assert expected==actual
bnew=k.LoadBoard(str(C/'SC09_compact.kicad_pcb'));native={f.GetReference():f for f in bnew.GetFootprints()}
assert native['L1'].GetField('MPN').GetText()=='PR02FS0201000KR500'
with zipfile.ZipFile(C/'release-refinement-R2/SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip')as z:
 assert z.testzip()is None;assert len(z.namelist())==8
 for n in z.namelist():assert z.read(n)==(H.parent/'sc09-sb01-refine/final-native'/('drills'if n.endswith('.drl')else'gerbers')/n).read_bytes()
report={'source_board_sha256':sha(C/'SC09_compact.kicad_pcb'),'base_board_sha256':sha(P/'SC09_compact.kicad_pcb'),'all_pad_copper_track_via_outline_geometry_and_membership_unchanged':True,'independent_before_BOM_pin_graph_equals_new_schematic':True,'physical_pins':len(expected),'net_count':len(set(expected.values())),'native_unconnected':new['unconnected'],'retained_23_spacing_geometry_scope':'Same exact copper/pad/track UUIDs and positions; previous geometry-only findings retained. No electrical waiver/approval transferred.','manufacturing_ZIP_sha256':sha(C/'release-refinement-R2/SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip'),'ZIP_all_eight_bytes_identical_to_R1':True,'native_pro_and_dru_unchanged':all(sha(C/n)==sha(P/n)for n in ['SC09_compact.kicad_pro','SC09_compact.kicad_dru']),'passed':True,'full_release_passed':False,'powered_qualification_passed':False}
(H/'native-final2/geometry-and-graph.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


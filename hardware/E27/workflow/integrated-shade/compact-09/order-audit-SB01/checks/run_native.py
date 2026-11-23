from pathlib import Path
import json,hashlib,shutil,subprocess,sys,xml.etree.ElementTree as ET,datetime
import pcbnew as k
ROOT=Path.cwd();H=ROOT/'work/sc09-order-audit/fabrication';S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';C=H/'native-copy';O=ROOT/'outputs/SC09_weryfikacja_i_kompendium/fabrication-candidate';G=O/'gerbers';G.mkdir(exist_ok=True);D=O/'drills';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source={p.relative_to(S).as_posix():sha(p)for p in S.rglob('*')if p.is_file()and '.work'not in p.parts and p.suffix not in ['.kicad_prl','.lck']}
assert source['SC09_compact.kicad_pcb']=='a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19'
shutil.copytree(S,C,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.work','release-candidate','*.kicad_prl','*.lck'))
(H/'source-inputs.json').write_text(json.dumps({'PCB_sha256':source['SC09_compact.kicad_pcb'],'files':source},indent=2)+'\n')
cli=str(Path(sys.executable).with_name('kicad-cli.exe'));logs=[]
def run(args):
 p=subprocess.run([cli]+args,capture_output=True,encoding='utf-8',errors='replace');rec={'args':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};logs.append(rec);(H/'commands.json').write_text(json.dumps(logs,indent=2)+'\n');print(args[0:3],p.returncode,flush=True);return p.returncode
run(['sch','erc','--format','json','--severity-all','--exit-code-violations','-o',str(H/'ERC.json'),str(C/'SC09_compact.kicad_sch')])
run(['sch','export','netlist','--format','kicadxml','-o',str(H/'netlist.xml'),str(C/'SC09_compact.kicad_sch')])
b=k.LoadBoard(str(C/'SC09_compact.kicad_pcb'));beforezones=[str(z.GetFilledPolysList(i).Format())for z in b.Zones()for i in [k.F_Cu,k.B_Cu]if z.GetLayerSet().Contains(i)]
run(['pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','--exit-code-violations','--refill-zones','--save-board','-o',str(H/'DRC-refilled.json'),str(C/'SC09_compact.kicad_pcb')])
b=k.LoadBoard(str(C/'SC09_compact.kicad_pcb'));afterzones=[str(z.GetFilledPolysList(i).Format())for z in b.Zones()for i in [k.F_Cu,k.B_Cu]if z.GetLayerSet().Contains(i)]
run(['pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts','--precision','6','--subtract-soldermask','--check-zones','-o',str(G),str(C/'SC09_compact.kicad_pcb')])
run(['pcb','export','drill','--format','excellon','--drill-origin','absolute','--excellon-units','mm','--excellon-zeros-format','decimal','--excellon-separate-th','--generate-report','--generate-map','--map-format','pdf','--report-path',str(D/'drill-report.txt'),'-o',str(D),str(C/'SC09_compact.kicad_pcb')])
run(['pcb','export','pdf','--layers','F.Cu,B.Cu,Edge.Cuts','--mode-multipage','-o',str(H/'native-copper-views.pdf'),str(C/'SC09_compact.kicad_pcb')])
# Independent intent graph: compare physical memberships, not net names.
intent=json.loads((S/'intended-connectivity.SB01.json').read_text());expected={frozenset((p['ref'],str(p['pin']))for p in n['pins'])for n in intent['nets']};xml=ET.parse(H/'netlist.xml');actual={frozenset((p.attrib['ref'],p.attrib['pin'])for p in n.findall('node'))for n in xml.findall('./nets/net')};actual.discard(frozenset())
missing=expected-actual;extra=actual-expected
native={(f.GetReference(),p.GetNumber()):p.GetNetname().lstrip('/')for f in b.GetFootprints()for p in f.Pads()};pin_expect={(p['ref'],str(p['pin'])):n['id']for n in intent['nets']for p in n['pins']}
box=b.GetBoardEdgesBoundingBox();mm=k.ToMM
report={'revision':'SC09-SB01 freshfabricationcandidate','date':'2026-11-23','actor':'/root/sb01_fabrication_audit','source_PCB_sha256':source['SC09_compact.kicad_pcb'],'source_unchanged':all(sha(S/p)==v for p,v in source.items()),'source_files':source,'copy_refilled_PCB_sha256':sha(C/'SC09_compact.kicad_pcb'),'native_version':k.GetBuildVersion(),'zones':{'count':len(list(b.Zones())),'filled_geometry_before_after_equal':beforezones==afterzones},'graph':{'expected_net_groups':len(expected),'actual_net_groups':len(actual),'missing_groups':[sorted(x)for x in missing],'extra_groups':[sorted(x)for x in extra],'physical_pin_count':len(native),'native_pin_difference':{str(p):[pin_expect.get(p),native.get(p)]for p in set(pin_expect)|set(native)if pin_expect.get(p)!=native.get(p)}},'outline_mm':[mm(box.GetWidth()),mm(box.GetHeight())],'copper_layers':b.GetCopperLayerCount(),'track_widths_mm':sorted(set(round(mm(t.GetWidth()),6)for t in b.GetTracks()if not isinstance(t,k.PCB_VIA))),'via_inventory':[{'position_mm':[mm(t.GetPosition().x),mm(t.GetPosition().y)],'drill_mm':mm(t.GetDrillValue()),'pad_mm':mm(t.GetWidth(k.F_Cu))}for t in b.GetTracks()if isinstance(t,k.PCB_VIA)],'through_pad_inventory':[{'ref':f.GetReference(),'pin':p.GetNumber(),'position_mm':[mm(p.GetPosition().x),mm(p.GetPosition().y)],'drill_mm':[mm(p.GetDrillSize().x),mm(p.GetDrillSize().y)],'pad_mm':[mm(p.GetSize().x),mm(p.GetSize().y)]}for f in b.GetFootprints()for p in f.Pads()if p.GetDrillSize().x>0],'native_reports':{'ERC':'ERC.json','DRC':'DRC-refilled.json'},'commands_all_success':all(x['exit_code']==0 for x in logs),'full_product_release':False,'order_submitted':False}
(H/'native-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('Finished native audit',report['source_unchanged'],report['outline_mm'],report['graph'],flush=True)


from pathlib import Path
import json,hashlib,subprocess,shutil,sys,os
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'pcb-cleanup-10';D=P/'pcb-cleanup-10';K=W/'kicad-10.0.6/bin';B=D/'design/Velluneo_driver.kicad_pcb';D.mkdir(exist_ok=True);(D/'checks').mkdir(exist_ok=True);(D/'fabrication').mkdir(exist_ok=True);(D/'assembly-reference').mkdir(exist_ok=True)
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
commands=[]
def run(name,args,allowed=(0,)):
 cmd=[str(x)for x in args];r=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 for ext,t in [('stdout.log',r.stdout),('stderr.log',r.stderr)]:(D/'checks'/(name+'.'+ext)).write_text(t,encoding='utf-8')
 commands.append(dict(name=name,command=cmd,exit_code=r.returncode));put(D/'checks/commands.json',commands);print(name,r.returncode,flush=True);assert r.returncode in allowed,(name,r.stdout,r.stderr)
before={ext:sha(B.with_suffix(ext))for ext in('.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_dru')}
put(D/'export-authorization-reference.json',dict(owner='Kamil',actual_message='Okej, działaj dalej i przygotuj tę płytkę do zamówienia prototypu. Stosuj toolkit, zapisuj wszystko na GitHubie i pokaż podgląd tutaj.',scope='Prepare exact selected board for prototype procurement review; publish files. No order, payment, supplier messages, powered testing or invented technical approval.',base_commit='538b2dee8e61cf8c944e494fa893732858ed648c'))
(D/'historical-export-contract-not-current.md').write_text('''# PROTOTYPE09 task contract

Prepare the one selected DRIVER08 45×60mm four-layer bare-board prototype package. Root owns exports/documents, no shared CAD/library edits. Preserve33parts81pads/approved intent and exact source bytes. Requirements R-BUILD/R-COST/R-BOARD-FORM/R-SIZE/R-SUPPLY/R-FAULT and original operating/insulation/thermal findings remain traceable. User request authorizes preparation and GitHub save, not supplier messages/orders/payment or physical tests. Bare-board files do not qualify assembled mains electronics.

Acceptance: fresh native ERC/DRC/parity; source hashes unchanged; four copper layers, masks, legends, one outline, PTH/NPTH drills and explicit via-fill map; independent CAM parsing, common-origin drill/outline/source reconciliation and actual CAM previews; BOM/placements separated from bare-board upload; concrete order settings and prototype receipt/bring-up gates; toolkit release reports retained honestly; ZIP manifest/CRC/remote verification; four actual independent read-only role reviews of one frozen body. Root is sole writer; reviews do not approve a technical stage. Do not hide an open release gate or declare cost/vendor acceptance without evidence.
''',encoding='utf-8')
run('drc',[K/'kicad-cli.exe','pcb','drc','--schematic-parity','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/drc.json',B]);j=json.loads((D/'checks/drc.json').read_text());assert not j['violations']and not j['unconnected_items']and not j['schematic_parity']
run('erc',[K/'kicad-cli.exe','sch','erc','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/erc.json',B.with_suffix('.kicad_sch')])
run('gerbers',[K/'kicad-cli.exe','pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts','--use-drill-file-origin','--subtract-soldermask','--precision','6','--output',str(D/'fabrication')+os.sep,B])
run('drill',[K/'kicad-cli.exe','pcb','export','drill','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','svg','--generate-report','--report-path',D/'checks/drill-report.txt','--output',str(D/'fabrication')+os.sep,B])
run('ipc356',[K/'kicad-cli.exe','pcb','export','ipcd356','--output',D/'fabrication/Velluneo_driver.d356',B])
run('position',[K/'kicad-cli.exe','pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--output',D/'assembly-reference/positions-native.csv',B])
for name in('BOM.csv',):shutil.copyfile(D/'design'/name,D/'assembly-reference'/name)
shutil.copyfile(D/'selected-process.json',D/'fabrication/selected-process.json')
run('schematic-pdf',[K/'kicad-cli.exe','sch','export','pdf','--output',D/'assembly-reference/Velluneo_driver.pdf',B.with_suffix('.kicad_sch')])
for side in('top','bottom'):
 run('render-'+side,[K/'kicad-cli.exe','pcb','render','--width','1400','--height','1100','--side',side,'--rotate','325,0,30','--perspective','--zoom','.68','--background','opaque','--quality','basic','--output',D/('native-'+side+'.png'),B])
put(D/'source-binding.json',dict(base_commit='538b2dee8e61cf8c944e494fa893732858ed648c',source_board=B.relative_to(R).as_posix(),source_files=[dict(path=B.with_suffix(ext).relative_to(R).as_posix(),sha256=h)for ext,h in before.items()],toolkit_commit='86614c3b9b43713031e0ea481edbe26b71cd1b8f',KiCad='10.0.6',CAD_unchanged=all(sha(B.with_suffix(ext))==h for ext,h in before.items()),historical_C09_preview_sha256=sha(P/'pcb-prototype-09/pcb-preview.png')))
assert all(sha(B.with_suffix(ext))==h for ext,h in before.items())
print('Prepared native export package',D,flush=True)

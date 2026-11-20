from pathlib import Path
import os,subprocess,json,hashlib,zipfile,shutil
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'supplier-review-13';D=P/'jlcpcb-quote-14';Q=D/'.work/project';K=W/'kicad-10.0.6/bin/kicad-cli.exe'
for n in('checks','gerbers','support','assembly-feasibility','reviews','implementation-history','.work/export'):(D/n).mkdir(parents=True,exist_ok=True)
(D/'.gitignore').write_text('.work/\n__pycache__/\n*.kicad_prl\n')
(D/'task-contract.md').write_text('''# JLC14 — JLCPCB-specific quotation handoff

Actual owner asks to prepare everything according to JLCPCB instructions so a quotation
can be requested. Owner explicitly chose PCB plus a separate assembly-feasibility quote.
Base b33e57c78eb3c1d644e3d00e96ccc5e47dc8bcaa; authoritative design is RFQ13, board
SHA256 05e08b6cafcf2a980c1dd7d66d020364d72356808b41bf197c5b594edb8bb236.
Root alone writes packaging, auxiliary CAM and documents; no production CAD/library,
rules, requirements or approval changes. Do not contact/upload to supplier, order, pay,
approve substitutions or claim accepted PCBA/import/process/physical qualification.

Deliver: freshly checked native exports for JLCPCB, 4Cu/2mask/2silk/2paste/oneoutline,
Excellon42PTH, explicit17via SKlayer/map, commonorigin/layer/drill/equivalentartwork
verification, exact settings/PCBremarks/manualsupportenquiry, all33partMPNs and
26SMTreferenceBOM/CPL with7manualoperations clearly separated. Do not invent LCSC IDs,
centroid corrections, feeder rotations, stock or a quote. Document any tutorial adaptation.
Include public JLCPCB rule/source mapping, tighter-hole/registration conflicts,
Standardtwo-sidedPCBA/min70x70panel/tooling needs, existingphysical/approvalholds.
Freeze once complete, four actual independent read-only final contexts, then publish
on existing review branch and independently verify GitHub bytes. English repo artifacts;
concise Polish instructions for owner. No stage advance or main merge.
''',encoding='utf-8')
with zipfile.ZipFile(S/'Velluneo_RFQ13_Engineering.zip')as z:z.extractall(Q)
B=Q/'Velluneo_driver.kicad_pcb';F=D/'.work/export';rows=[]
inputs={p.relative_to(S/'design').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted((S/'design').rglob('*'))if p.is_file()and p.suffix!='.kicad_prl'and not any(v in p.relative_to(S/'design').parts for v in('.work','__pycache__'))}
jobs=[('drc',['pcb','drc','--schematic-parity','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/drc.json',B]),('erc',['sch','erc','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/erc.json',B.with_suffix('.kicad_sch')]),('gerbers',['pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,F.Paste,B.Paste,Edge.Cuts','--use-drill-file-origin','--subtract-soldermask','--no-x2','--no-netlist','--check-zones','--precision','6','--output',str(F)+os.sep,B]),('drill',['pcb','export','drill','--drill-origin','plot','--excellon-units','mm','--excellon-zeros-format','decimal','--excellon-oval-format','alternate','--excellon-separate-th','--generate-map','--map-format','svg','--generate-report','--report-path',D/'checks/drill-report.txt','--output',str(F)+os.sep,B]),('positions',['pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--output',D/'support/positions-native.csv',B])]
for name,args in jobs:
 cmd=[str(K),*map(str,args)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 (D/'checks'/(name+'.stdout.log')).write_text(r.stdout,encoding='utf-8');(D/'checks'/(name+'.stderr.log')).write_text(r.stderr,encoding='utf-8');assert r.returncode==0,(name,r.stdout,r.stderr);rows.append(dict(check=name,command=cmd,exit_code=r.returncode));print(name,'PASS',flush=True)
mapping={'F_Cu.gtl':'GTL','In1_Cu.g1':'G2L','In2_Cu.g2':'G3L','B_Cu.gbl':'GBL','F_Mask.gts':'GTS','B_Mask.gbs':'GBS','F_Silkscreen.gto':'GTO','B_Silkscreen.gbo':'GBO','F_Paste.gtp':'GTP','B_Paste.gbp':'GBP','Edge_Cuts.gm1':'GKO','PTH.drl':'XLN'}
for old,new in mapping.items():shutil.copyfile(F/('Velluneo_driver-'+old),D/'gerbers'/('Velluneo_JLC14.'+new))
shutil.copyfile(F/'Velluneo_driver-PTH-drl_map.svg',D/'gerbers/Velluneo_JLC14-drill_map.svg')
inv=json.loads((S/'checks/native-inventory.json').read_text());vias=inv['vias']
assert len(vias)==17
sk=['G04 JLC14 sk: AUXILIARY VIA FILL SELECTION ONLY - NOT COPPER OR OUTLINE*','G04 Nonconductive epoxy fill and copper cap both ends of ALL 17 marked 0.300mm vias*','G04 Keep all 25 component insertion holes open; same origin as all other files*','%FSLAX46Y46*%','%MOMM*%','%LPD*%','%ADD10C,0.300000*%','D10*']
for v in vias:sk.append('X%dY%dD03*'%(round(v['output_x_mm']*1e6),round(v['output_y_mm']*1e6)))
sk.append('M02*');(D/'gerbers/Velluneo_JLC14.sk').write_text('\n'.join(sk)+'\n',encoding='ascii')
for n in('designated-filled-vias.csv','selected-process.json'):shutil.copyfile(S/'fabrication'/n,D/'support'/n)
shutil.copyfile(S/'drawings/Velluneo_RFQ13_Dimensioned_Review.pdf',D/'support/Velluneo_RFQ13_Dimensioned_Review.pdf')
shutil.copyfile(S/'assembly-reference/Velluneo_driver.pdf',D/'support/Velluneo_driver_schematic.pdf')
shutil.copyfile(S/'fabrication/Velluneo_driver.d356',D/'support/Velluneo_driver.d356')
for p,h in inputs.items():assert hashlib.sha256((S/'design'/p).read_bytes()).hexdigest()==h,p
assert hashlib.sha256(B.read_bytes()).hexdigest()==inputs['Velluneo_driver.kicad_pcb'],'Export clone changed'
(D/'source-binding.json').write_text(json.dumps(dict(base_commit='b33e57c78eb3c1d644e3d00e96ccc5e47dc8bcaa',source_project='supplier-review-13/design',source_files=inputs,original_sources_unchanged=True,export_clone_board_unchanged=True,native_KiCad='10.0.6',toolkit_manifest_sha256='b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97',commands=rows,coordinate_frame='Native77.5,130mm plot origin; outputX=x-77.5,Y=130-y. All manufacturing/CPL/SK use this same frame, board0..45x0..60. Tutorial Absolute example adapted deliberately to retained project common datum; no mirror or physical CAD change.'),indent=2)+'\n')
print('JLC14 native export and 17flash SK generated; RFQ13 source bytes retained',flush=True)

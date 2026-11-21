from pathlib import Path
import sys, os, json, csv, hashlib, shutil, subprocess, zipfile
W=Path(__file__).resolve().parent
sys.path[:0]=[str(W/'python-libs'),str(W/'cam-libs')]
R=W/'Velluneo-readiness'; P=R/'hardware/E27/workflow/specification-reset'
S=P/'catalogue-pcb-16'; E=S/'design'; D=P/'manufacturing-c17'; K=W/'kicad-10.0.6/bin/kicad-cli.exe'
for n in ['checks','gerbers','assembly','support','drawings','preview','implementation','.work/export','.work/project','reviews']:(D/n).mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def txt(p,s):p.write_text(s,encoding='utf-8')
def files(p):return [f for f in sorted(p.rglob('*')) if f.is_file() and not any(x in f.relative_to(p).parts for x in ('.work','__pycache__')) and f.suffix!='.kicad_prl']
def csvout(p,cols,data):
 with p.open('w',encoding='utf-8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(data)
base='a283213194bb16990d7614874d12336524f66fcf'
txt(D/'.gitignore','.work/\n__pycache__/\n')
source={p.relative_to(E).as_posix():sha(p)for p in files(E)}
for f in files(E):
 out=D/'.work/project'/f.relative_to(E);out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,out)
B=D/'.work/project/Velluneo_driver.kicad_pcb'; F=D/'.work/export';commands=[]
def run(name,args,allow_fail=False):
 cmd=list(map(str,args));r=subprocess.run(cmd,capture_output=True,timeout=240,cwd=R)
 (D/'checks'/f'{name}.stdout.log').write_bytes(r.stdout);(D/'checks'/f'{name}.stderr.log').write_bytes(r.stderr)
 commands.append(dict(name=name,command=cmd,exit_code=r.returncode))
 if not allow_fail:assert r.returncode==0,(name,r.stdout[-2000:],r.stderr[-1000:])
 print(name,r.returncode,flush=True);return r
jobs=[('erc',['sch','erc','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/erc.json',B.with_suffix('.kicad_sch')]),('drc',['pcb','drc','--schematic-parity','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/drc.json',B]),('gerbers',['pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,F.Paste,B.Paste,Edge.Cuts','--use-drill-file-origin','--subtract-soldermask','--no-x2','--no-netlist','--check-zones','--precision','6','--output',str(F)+os.sep,B]),('drill',['pcb','export','drill','--drill-origin','plot','--excellon-units','mm','--excellon-zeros-format','decimal','--excellon-oval-format','alternate','--excellon-separate-th','--generate-map','--map-format','svg','--generate-report','--report-path',D/'checks/drill-report.txt','--output',str(F)+os.sep,B]),('positions',['pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--output',D/'assembly/positions-native.csv',B]),('ipc356',['pcb','export','ipc2581','--help'])]
for name,args in jobs[:-1]:run(name,[K,*args])
run('schematic-pdf',[K,'sch','export','pdf','--output',D/'drawings/Velluneo_C17_schematic.pdf',B.with_suffix('.kicad_sch')])
run('netlist',[K,'sch','export','netlist','--format','kicadxml','--output',D/'support/netlist.xml',B.with_suffix('.kicad_sch')])
for side,layers in [('top','F.Fab,F.SilkS,Edge.Cuts'),('bottom','B.Fab,B.SilkS,Edge.Cuts')]:
 args=[K,'pcb','export','svg','--mode-single','--layers',layers,'--sketch-pads-on-fab-layers','--fit-page-to-board','--exclude-drawing-sheet','--black-and-white','--output',D/'drawings'/f'assembly-{side}.svg']
 if side=='bottom':args+=['--mirror']
 run('assembly-'+side,[*args,B])
mapping={'F_Cu.gtl':'GTL','In1_Cu.g1':'G2L','In2_Cu.g2':'G3L','B_Cu.gbl':'GBL','F_Mask.gts':'GTS','B_Mask.gbs':'GBS','F_Silkscreen.gto':'GTO','B_Silkscreen.gbo':'GBO','F_Paste.gtp':'GTP','B_Paste.gbp':'GBP','Edge_Cuts.gm1':'GKO','PTH.drl':'XLN'}
for old,new in mapping.items():shutil.copyfile(F/('Velluneo_driver-'+old),D/'gerbers'/('Velluneo_C17.'+new))
shutil.copyfile(F/'Velluneo_driver-PTH-drl_map.svg',D/'gerbers/Velluneo_C17-drill_map.svg')
audit=json.loads((S/'checks/native-audit.json').read_text());origin=[77.5,130.]
def xy(a):return [a[0]-origin[0],origin[1]-a[1]]
holes=[]
for a in audit['pads']:
 if a['hole_mm']>0:
  x,y=xy(a['xy_mm']);holes.append(dict(Pad=a['id'],X_mm=round(x,6),Y_mm=round(y,6),Finished_target_mm=a['hole_mm'],Fill='OPEN',Tolerance='T1 +/-0.05mm; others capability confirmation',Net=a['net']))
vias=[]
for i,a in enumerate(audit['vias'],1):
 x,y=xy(a['a']);vias.append(dict(ID='V'+str(i),X_mm=round(x,6),Y_mm=round(y,6),Diameter_mm=a['hole_mm'],Net=a['net']))
assert len(holes)==18 and len(vias)==24
csvout(D/'support/component-holes.csv',list(holes[0]),holes);csvout(D/'support/filled-vias.csv',list(vias[0]),vias)
sk=['G04 C17 AUXILIARY VIA FILL SELECTION ONLY - NOT COPPER OR OUTLINE*','G04 Epoxy fill and copper cap BOTH ends of 24 marked 0.300mm vias ONLY*','G04 Leave all 18 component PTH open*','%FSLAX46Y46*%','%MOMM*%','%LPD*%','%ADD10C,0.300000*%','D10*']
for a in vias:sk.append('X%dY%dD03*'%(round(a['X_mm']*1e6),round(a['Y_mm']*1e6)))
txt(D/'gerbers/Velluneo_C17.sk','\n'.join(sk+['M02*'])+'\n')
# Native BOM identity, positions and explicit machine-data limitations.
stock=json.loads((S/'selected-bom.json').read_text());byref={x['ref']:x for x in stock['components']}
pos={x['Ref']:x for x in csv.DictReader((D/'assembly/positions-native.csv').open(encoding='utf-8-sig'))}
parts={x['ref']:x for x in audit['parts']};assert set(byref)==set(pos)==set(parts) and len(parts)==33
full=[];smt=[];cpl=[];allpos=[]
for ref in sorted(parts):
 a=parts[ref];s=byref[ref];p=pos[ref];assert s['mpn']==a['mpn']
 is_smt=ref not in ['T1','Q1','C1','J1','J2']
 assert max(abs(float(p['PosX'])-xy(a['xy_mm'])[0]),abs(float(p['PosY'])-xy(a['xy_mm'])[1]))<1e-5
 row={'Comment':a['value'],'Designator':ref,'Footprint':a['footprint'].split(':')[-1],'Quantity':1,'LCSC Part #':'','Manufacturer':s['manufacturer'],'Manufacturer Part Number':s['mpn']}
 full.append(dict(**row,Process='SMT'if is_smt else'WIRE OPERATION'if ref in ['J1','J2']else'THT',Purchase_URL=s.get('preferred_purchase',{}).get('url',''),Observed_JLC_Code=(s.get('jlcpcb')or{}).get('code',''),Sourcing_status='Exact MPN; availability/consignment must be reconfirmed; no automatic substitution'))
 cp={'Designator':ref,'Mid X':f"{float(p['PosX']):.6f}",'Mid Y':f"{float(p['PosY']):.6f}",'Rotation':f"{float(p['Rot'])%360:.6f}",'Layer':p['Side'].capitalize()};allpos.append(cp)
 if is_smt:smt.append(row);cpl.append(cp)
assert len(smt)==len(cpl)==28
csvout(D/'assembly/BOM_33_FULL.csv',list(full[0]),full);csvout(D/'assembly/BOM_28_SMT.csv',list(smt[0]),smt);csvout(D/'assembly/CPL_28_SMT.csv',list(cpl[0]),cpl);csvout(D/'assembly/POSITIONS_33_REFERENCE.csv',list(allpos[0]),allpos)
csvout(D/'assembly/operations.csv',['Designator','Operation','Acceptance'],[dict(Designator='T1',Operation='Factory MYRRA74032; insert and solder 9 pins',Acceptance='Current body 26.5x22.5x26.5mm max; pin4 absent; actual lot/fit check. No winding or lead forming.'),dict(Designator='Q1',Operation='Straight TO-3PF; fixture then solder/trim',Acceptance='Lowest wide shoulder >=3mm above PCB; body-bottom approx6.5mm, height reservation29.7mm; mechanical support must be agreed.'),dict(Designator='C1',Operation='Radial THT; insert and solder',Acceptance='Front side, correct polarity; no lead stress, vent clearance >=2mm.'),dict(Designator='J1 J2',Operation='Optional external harness soldering',Acceptance='Wire material in full BOM; cut lengths, sleeves, strain relief and routing not defined. Exclude harness from populated-board base quote.')])
shutil.copyfile(S/'selected-bom.json',D/'support/sourcing-register-C16.json')
shutil.copyfile(S/'bring-up-and-assembly.md',D/'support/bring-up-and-assembly.md')
shutil.copyfile(S/'open-engineering-holds.json',D/'support/open-engineering-holds.json')
for n in ['MYRRA74032.pdf','MYRRA74032-PCN.pdf']:shutil.copyfile(W/'c17-sources'/n,D/'support'/n)
for n in ['C16_both_faces.png','C16_inner_layers.png']:shutil.copyfile(S/'preview'/n,D/'preview'/n)
for name,args in [('doctor',['doctor']),('requirements-release',['run','requirements',E.relative_to(R).as_posix(),'--stage','release']),('toolkit-release',['run','check',E.relative_to(R).as_posix(),'--mode','release'])]:
 os.environ['KICAD_CLI']=str(K);os.environ['KICAD_PYTHON']=str(W/'kicad-10.0.6/bin/python.exe')
 run(name,[sys.executable,R/'pcb-toolkit.py',*args],allow_fail=name!='doctor')
 out=E/'.work'/('requirements.json'if name=='requirements-release'else'check.json')
 if name!='doctor'and out.exists():shutil.copyfile(out,D/'checks'/(name+'.json'))
assert all(sha(E/p)==h for p,h in source.items())
assert sha(B)==source['Velluneo_driver.kicad_pcb']
put(D/'source-binding.json',dict(base_commit=base,source_project='catalogue-pcb-16/design',source_files=source,source_board_sha256=source['Velluneo_driver.kicad_pcb'],native_tool='KiCad10.0.6',toolkit_manifest_sha256='b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97',source_files_unchanged=True,export_clone_board_unchanged=True,coordinate_frame='Top view mm: X=nativeX-77.5; Y=130-nativeY. Board0..45 x0..60. Both sides share XY; only human bottom drawing is mirrored.',commands=commands))
put(D/'checks/assembly-check.json',dict(passed=True,positions=33,SMT=28,THT=3,wire_pairs=2,SMT_BOM_CPL_sets_equal={x['Designator']for x in smt}=={x['Designator']for x in cpl},native_position_crosscheck=True,LCSC_upload_fields_blank=True,why_blank='Exact MPNs carried; observed JLC codes are sourcing hints in FULL BOM, not confirmed matching stock. Manual support sourcing/consignment required.',machine_centroids_and_feeder_rotations_verified=False,portal_import_performed=False))
print('C17 native exports and BOM complete',flush=True)

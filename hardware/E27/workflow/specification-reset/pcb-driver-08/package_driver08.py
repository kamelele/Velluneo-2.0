from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import fitz
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-driver-08';E=D/'design';O=E/'checks';K=W/'kicad-10.0.6/bin';base='8c57a24d9cdfe50ad1bc3b28f238287200b5c51b'
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mode=sys.argv[1]
if mode=='docs':
 evidence=D/'evidence';evidence.mkdir(exist_ok=True);shutil.copyfile(D/'.work/routing-input.kicad_pcb',evidence/'routing-input.kicad_pcb')
 for name in('verify_saved_geometry.py',):
  p=D/name;p.write_text(p.read_text().replace("D/'.work/routing-input.kicad_pcb'","D/'evidence/routing-input.kicad_pcb'"))
 for src in('finish_driver08_native.py','check_export_driver08.py','package_driver08.py'):shutil.copyfile(W/src,D/src)
 m=json.loads((D/'route-metrics.json').read_text());a=json.loads((O/'native-analysis.json').read_text());branches={r['label']:r for r in m['branches']}
 def n(key):return branches[key]['planar_length_mm']
 readme=f'''# Velluneo DRIVER08 — selected routed driver PCB

The owner's latest instruction delegates selection and completion. The coordinator selects one four-layer driver PCB, rectangular **45 × 60 mm**, with all **33 components, 81 pads, 23 functional nets and four explicit NC singleton nets** retained. Open **design/Velluneo_driver.kicad_pro**, or the same file at the root of Velluneo_driver_KiCad.zip. There is one selected project, not two alternatives. Selection does not invent human safety/stage acceptance.

## Completed CAD

Saved KiCad10.0.6: **{a['track_segments']} track segments, {a['vias']} through-vias; native DRC zero violations, zero unconnected, zero schematic parity findings; ERC zero**. Fresh independently exported schematic netlist and native pin memberships match the approved intent digest `87b164503d5c5894dfe592608a172bd858c960b3a40b1b141f3588bfeffd716b`. The stricter canonical C06 project/rules are preserved, including 3mm HV/quiet and 10mm primary/secondary scoped rules. No new waiver, altered pin type or rule weakening hides routing errors. Five inherited ignored check categories remain as before; 0DRC is conditional on that disclosed policy.

DRV U1.3→R7.1 decreases from43.072mm to **{m['drv_planar_mm']:.3f}mm**, width0.4mm, entirely front copper, zero vias. R7→Q1 gate is {n('gate') if 'gate'in branches else next(r['planar_length_mm']for r in m['branches']if r['a']=='R7.2'and r['b']=='Q1.1'):.3f}mm. Main primary feed and drain/clamp branches now use0.8mm; the IC return uses0.6mm. R9-negative→C1 shared strap is widened from1.0 to1.8mm. The native cut diagnostics keep IC, shunt, bridge and auxiliary branches separate outside the C1 junction neighborhood; separate source/sense and gate-pulldown pickups remain. Dedicated six-segment SENSE25.197855mm and CS1.931321mm are unchanged. Projected different-layer HV-track/all-HV-via gaps remain at least3.381mm and5.165mm respectively. These are saved geometry checks, not measured noise, inductance, loop impedance or current ratings.

The C1 star is deliberate: exact UCC28700-family TI datasheet SLUSB41A §11.1 directs IC/power grounds to the bulk capacitor return. IC GND also carries gate-driver current. The2.7mm shared negative strap is **not** a complete negative Kelvin pickup; no such claim is made. The actual local C2 VDD branch remains about1.583mm and C2-ground→U1 about1.521mm. TI source details and unqualified operating checks appear in engineering-status.md.

## Concrete process definition

Selected four-layer construction JLC04161H-7628, nominal1.6mm FR4 Tg155 request, outer35µm/inner15.2µm, ENIG/greenmask. Listed layers total1.5862mm; the0.0138mm difference to nominal is disclosed, not allocated to invented dielectric. The native PCB includes this physical stackup. **All17 designated PCB_VIA holes are explicitly epoxy-filled/copper-capped** (0.6mm pad/0.3mm hole), including via-in-land sites. Component insertion holes stay open. See selected-process.json and designated-filled-vias.csv. Nearest component-hole edge gap exceeds1.303mm. This is a selected process definition from official capabilities, not a vendor quote, confirmation or manufacturing acceptance. The output origin is board(77.5,130)mm, Xright/Yup, shared by positions and via map.

The lamp target remains Ø60×120mm. This packet completes driver CAD routing, not finished housing fit; rectangular45×60 PCB and30×30 transformer allocation need assembled wall/wire/tolerance assessment. Models shown are envelope allocations, not exact finished manufacturer bodies.

## Verification and boundaries

Fresh reports live in design/checks. Surface-short, inner-layer isolation-breach and same-net return-shortcut diagnostic copies are deliberately invalid and are detected. They never replace product CAD. Saved-copper coverage and all33 local model paths are checked. The immutable pre-routing source is evidence/routing-input.kicad_pcb; its hash matches the applied plan. Other intermediate geometry/attempt reports are historical inputs, not final board reports. Final board SHA is bound throughout checks/preview/portable manifest.

Toolkit pin86614c3b9b43713031e0ea481edbe26b71cd1b8f is used without modifying the toolkit. Fresh requirements/work checks still fail product-level open inputs and managed configuration/spatial adoption; configuration preview is read-only, never applied. These failures are retained honestly. Prior finding history remains in ../pcb-return-06/acceptance-ledger.json and ../pcb-route-07/acceptance-ledger.json. Selection/longDRV/incomplete-routing findings are superseded only to the demonstrated CAD scope; all operating/thermal/finished-transformer-insulation/assembly/fit findings remain unqualified. Full safety standards are unavailable and the owner has no TINA-TI; no simulated waveform or laboratory result is invented.

**Completed routed CAD is not a released production or mains-powered prototype design.** No Gerbers, manufacturing order, supplier contact, powered tests, CE/safety acceptance or human stage approval are represented. Next engineering acceptance needs qualified transformer construction, actual current/voltage/fault/startup and thermal measurements, assembled creepage/clearance/material assessment and process confirmation. These are physical validation work on this same selected design, not another PCB choice. Four independent reviews recommend only the exact bounded CAD publication if their findings close.

pcb-preview.png shows actual native 3D and four actual copper exports. Velluneo_driver.pdf is the current schematic. assembly-positions.csv is a reference placement export; rotations are native, not assembly-house calibration. The portable ZIP contains the one matching project plus local libraries/models and process/assembly notes. Fresh extracted ERC/DRC and member hashes verify portability.
'''
 (D/'README.md').write_text(readme,encoding='utf-8')
 (D/'engineering-status.md').write_text('''# Engineering scope and residual qualification

One4layer CAD selected under the owner's explicit delegated choice; routing complete. See exact native reports and selected process. This is not a claim of functional completion of a certified mains lamp.

## Current paths and sensing

TI SLUSB41A UCC2870x datasheet https://www.ti.com/lit/ds/symlink/ucc28700.pdf §11.1 p24 joins IC and power grounds at bulk capacitor return; §8.3.1.2 p10 requires local VDD bypass, §8.3.1.4–5 p11 describes DRV and RLC; GND is gate-driver return as well as analog reference. Keep bridge/aux/main shunt currents off the IC-return branch. TI SLUA783 https://www.ti.com/lit/an/slua783/slua783.pdf §2.6.1 p6 discusses CS spikes/RLC placement and CC effects; §2.7.2 p7–8 VS susceptibility. Primary documents checked19Nov2026. Their guidance supports the topology, not a measured error margin. No requirement for a fabricated negative-Kelvin topology is attributed to TI.

Wider bulk/drain and1.8mm shunt return reduce geometric conductor resistance but no current rating follows without operating RMS/pulse current, actual copper tolerance/temperature and thermal boundary. Inner copper is15.2µm, not35µm. Native plan lengths exclude via barrels, pads and component internal leads. No closed-loop area or inductance is inferred from one branch length. No ground pour was added that would short the intentional C1 star branches. Native cuts are conditional topology diagnostics, not impedance isolation. The CS/SENSE corridor is a conservative additional projection screen, not electric/magnetic field simulation or primary/secondary insulation proof.

## Remaining physical evidence on this selected board

Verify cold/hot start, VDD charge and auxiliary handover, line/load extremes, brownout/reset/retry, output-open/short/no-panel/partial-contact, sensor open/short, clamp drain peak/energy, shunt pulse/RLC error and actual gate Vgs/ringing at suitable isolated test facilities. Retain the C05/C06 electrical/transformer calculation assumptions; no new waveform closes them. Transformer core/gap/winding wire, termination forming, creepage through winding/finished joints, dielectric/hipot and thermal endurance require actual qualified construction evidence.3/10mm PCB rules and nominal FR4 do not establish full IEC/EN60598/61347 compliance. Tg155 does not establish CTI, RTI or a continuous service temperature.

Selected fab process includes filled/capped through-vias; confirm precise stackup/material, mask, copper tolerance, hole filling/capping and assembly with the vendor before order. Component PTH/NPTH holes stay open. Whole-lamp thermal design and Ø60×120 fit remain outside this driver-only CAD completion. No standard clauses/tables not accessible were invented. No physical qualification, supplier response, release or human approval is asserted.
''',encoding='utf-8')
 put(D/'completion-status.json',dict(base_commit=base,selected_layers=4,selected_board_mm=[45,60],owner_delegated_choice=True,routed_CAD_complete=True,native_violations=0,native_unconnected=0,native_parity=0,erc=0,physical_product_qualified=False,manufacturing_released=False,powered_tests_performed=False,board_sha256=sha(E/'Velluneo_driver.kicad_pcb')))
 print('Wrote selected board documentation')
elif mode=='preview':
 fontpath='C:/Windows/Fonts/arial.ttf';f=lambda size:ImageFont.truetype(fontpath,size)
 canvas=Image.new('RGB',(1800,1620),'#101827');draw=ImageDraw.Draw(canvas);draw.text((50,30),'VELLUNEO / ZASILACZ',font=f(38),fill='white');draw.text((50,88),'Jedna wybrana płytka • 45 × 60 mm • 4 warstwy • 33 elementy',font=f(25),fill='#aabbd0')
 for i,side in enumerate(('top','bottom')):
  im=Image.open(D/('native-'+side+'.png')).convert('RGB');im.thumbnail((820,650));x=45+i*880;y=150;canvas.paste(im,(x+(820-im.width)//2,y));draw.text((x,y+655),'Widok z góry'if i==0 else'Widok od spodu',font=f(24),fill='white')
 for i,name in enumerate(('front','inner1','inner2','back')):
  p=D/('copper-'+name+'.svg');doc=fitz.open(stream=p.read_bytes(),filetype='svg');pix=doc[0].get_pixmap(matrix=fitz.Matrix(4,4),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((410,600));x=45+i*440;y=885;canvas.paste(im,(x+(410-im.width)//2,y));draw.text((x,y-40),('F.Cu','In1.Cu','In2.Cu','B.Cu')[i],font=f(23),fill='white')
 draw.text((50,1510),'Wszystkie połączenia poprowadzone • DRC: 0 naruszeń / 0 brakujących połączeń',font=f(26),fill='#72e0b0');draw.text((50,1560),'Rzeczywisty eksport KiCada. Bryły pokazują gabaryty. Weryfikacja prototypu i izolacji pozostaje do wykonania.',font=f(20),fill='#aabbd0')
 canvas.save(D/'pcb-preview.png');target=W.parent/'outputs/Velluneo_driver08.png';target.parent.mkdir(exist_ok=True);shutil.copyfile(D/'pcb-preview.png',target)
 inputs=[E/'Velluneo_driver.kicad_pcb',D/'route-metrics.json',D/'native-top.png',D/'native-bottom.png',*[D/('copper-'+n+'.svg')for n in('front','inner1','inner2','back')]]
 put(D/'preview-manifest.json',dict(inputs=[dict(path=p.relative_to(D).as_posix(),sha256=sha(p))for p in inputs],output=dict(path='pcb-preview.png',sha256=sha(D/'pcb-preview.png')),native_actual_geometry=True,models_are_allocations=True))
 print('Preview',target)
elif mode=='zip':
 members={};root=D/'.work/portable';root.mkdir(parents=True,exist_ok=True)
 for p in E.rglob('*'):
  rel=p.relative_to(E)
  if p.is_file()and not any(x in rel.parts for x in('checks','.work','__pycache__'))and(p.suffix in('.kicad_pro','.kicad_sch','.kicad_pcb','.kicad_dru','.kicad_mod','.kicad_sym','.wrl')or p.name in('fp-lib-table','sym-lib-table','BOM.csv')):members[rel.as_posix()]=p.read_bytes()
 for name in('README.md','engineering-status.md','selected-process.json','designated-filled-vias.csv','assembly-positions.csv'):members[name]=(D/name).read_bytes()
 for name,raw in members.items():p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 zp=D/'Velluneo_driver_KiCad.zip'
 with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED)as z:
  for name,raw in sorted(members.items()):z.writestr(zipfile.ZipInfo(name,date_time=(2026,11,19,0,0,0)),raw,compress_type=zipfile.ZIP_DEFLATED)
 with zipfile.ZipFile(zp)as z:
  assert z.testzip()is None
  for name,raw in members.items():assert z.read(name)==raw
 checks=[]
 for kind in('drc','erc'):
  output=O/('portable-'+kind+'.json');cmd=[str(K/'kicad-cli.exe'),*(['pcb','drc','--schematic-parity']if kind=='drc'else['sch','erc']),'--format','json','--severity-all','--exit-code-violations','--output',str(output),str(root/('Velluneo_driver.'+('kicad_pcb'if kind=='drc'else'kicad_sch')))];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180);assert r.returncode==0,(kind,r.stdout,r.stderr);j=json.loads(output.read_text());assert not(j['violations']if kind=='drc'else[v for s in j['sheets']for v in s['violations']])
  if kind=='drc':assert not j['unconnected_items']and not j['schematic_parity']
  checks.append(dict(check=kind,exit_code=r.returncode,violations=0,command=cmd));print('Portable',kind,0,flush=True)
 put(D/'portable-artifacts.json',dict(zip=zp.name,sha256=sha(zp),crc_pass=True,members=[dict(path=n,bytes=len(r),sha256=hashlib.sha256(r).hexdigest())for n,r in sorted(members.items())],extracted_native_checks=checks,project_at_archive_root='Velluneo_driver.kicad_pro',one_selected_project=True,source_CAD_bytes_unchanged=True))
elif mode=='inventory':
 h=P/'hardware.json';old=json.loads(subprocess.check_output(['git','show',base+':hardware/E27/workflow/specification-reset/hardware.json'],cwd=R));j=json.loads(h.read_text());assert j==old
 files=sorted(p for p in D.rglob('*')if p.is_file()and not any(x in p.relative_to(D).parts for x in('.work','__pycache__','reviews','checks'))and p.suffix in('.py','.json','.md','.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_dru','.kicad_mod','.kicad_sym','.wrl')and p.name not in('frozen-files.json','review-record.json','integration-record.md','stage-packet.md','inventory-delta.json'))
 added=[p.relative_to(P).as_posix()for p in files if p.relative_to(P).as_posix()not in j['source_files']];j['source_files']+=added;put(h,j);put(D/'inventory-delta.json',dict(base_commit=base,prior_entries=len(old['source_files']),appended=len(added),entries=added,other_fields_unchanged=True))
 index=R/'hardware/E27/workflow/project-index.md';s=index.read_text();heading='''## Current selected routed driver — DRIVER08,19November2026

[DRIVER08](specification-reset/pcb-driver-08/README.md) is the one selected four-layer45×60mm driver under the owner's delegated choice. All33parts/81pads are retained; actual native0DRC/0unconnected/0parity and0ERC. DRV is14.467mm, no vias. Power/return copper is strengthened and measurement branches preserved. The single portable project, actual preview, stackup and designated filled/capped via map are supplied. Routed CAD is complete; operating/fault/thermal/finished-transformer-insulation/fit/process confirmation and human product/stage acceptance remain unqualified. No order or powered tests are represented. Older packets below retain historical decisions and are superseded only to the explicit DRIVER08 CAD scope.

'''
 index.write_text(s.replace('# E27 workflow index\n\n','# E27 workflow index\n\n'+heading,1),encoding='utf-8',newline='\n');print('Appended',len(added),'sources')

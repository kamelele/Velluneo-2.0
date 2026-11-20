from pathlib import Path
import json,hashlib,csv,subprocess,pcbnew as p
W=Path(__file__).resolve().parent
if W.name=='implementation':
 D=W.parent;P=D.parent;R=P.parents[3];W=R.parent
else:
 R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'catalogue-redesign-15'
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def put(n,j):
 q=D/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8')
b=p.LoadBoard(str(P/'supplier-review-13/design/Velluneo_driver.kicad_pcb'))
native={f.GetReference():dict(mpn=f.GetField('MPN').GetText(),value=f.GetValue(),footprint=str(f.GetFPID().GetLibItemName()),pads=f.GetPadCount())for f in b.GetFootprints()}
s=json.loads((D/'selected-bom.json').read_text(encoding='utf-8'));rows=s['components']
assert len(rows)==len(native)==33 and len({x['ref']for x in rows})==33
assert set(native)=={x['ref']for x in rows}
for x in rows:
 assert x['old_mpn']==native[x['ref']]['mpn'],x['ref']
 assert x['old_value']==native[x['ref']]['value'],x['ref']
 assert x['preferred_purchase']['url'].startswith('https://')
 assert x['preferred_purchase']['MOQ'] is not None
 assert not x['assembly_release']
 if x['ref']not in('J1','J2'):assert isinstance(x['preferred_purchase']['stock'],int)and x['preferred_purchase']['stock']>0
assert next(x for x in rows if x['ref']=='T1')['mpn']=='74215'
assert not any(x['mpn'].startswith(('CUSTOM:','PROJECT:'))for x in rows)
pin=json.loads((D/'interfaces/transformer-pin-intent.json').read_text())
assert pin['pins']['3']=='physically absent'and 'tap' in pin['pins']['8']and 'tap' in pin['pins']['9']
assert pin['windings']==[dict(pins=[4,6],turns=120),dict(pins=[2,1],turns=14),dict(pins=[7,10],turns=27),dict(pins=[8,10],turns=17),dict(pins=[9,10],turns=6)]
c=json.loads((D/'calculations/transformer-screen.json').read_text())['results']
# Independent dimensional form: t_demag = Lp*Ipk/(Np/Ns*(Vout+Vf)); f=Ddemag/t_demag.
t=.0018*(.75/2.55)/((120/27)*(24+.8));freq=.425/t
assert abs(c['CC_demag_frequency_at_24V_Hz']-freq)<1e-7 and 88000<freq<89000
assert .249<c['nominal_current_A']<.251 and abs(c['RCS_for_250mA']-2.552)<1e-10
assert c['static_fault_Ipk_at_1p6V_A']>.5
assert c['DPAK_maker_pad_gap_mm']<3
assert c['estimated_copper_gap_active_1p55mm']>=10.7
# Preserve every one of the bound actual RFQ13 design sources, not merely the PCB.
binding=json.loads((P/'jlcpcb-quote-14/source-binding.json').read_text())
files=binding['source_files'];bad=[n for n,h in files.items()if sha(P/'supplier-review-13/design'/n)!=h]
assert not bad,bad
lock=json.loads((R/'.pcb-toolkit/lock.json').read_text())['current']
assert lock['manifest_sha256']=='b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97'
toolkit=R/'.pcb-toolkit/versions'/lock['manifest_sha256'];mf=toolkit/'PACKAGE-MANIFEST.json'
assert sha(mf)==lock['manifest_sha256']
manifest=json.loads(mf.read_text())
for n,v in manifest['files'].items():
 q=toolkit/n;assert q.stat().st_size==v['size']and sha(q)==v['sha256'],n
put('checks/toolkit-content-integrity.json',dict(manifest_sha256=sha(mf),payload_files_checked=len(manifest['files']),all_payload_sizes_and_hashes_match=True,toolkit_modified=False))
put('checks/selection-check.json',dict(status='PASS for purchasing-map consistency, not electrical/PCB release',positions=len(rows),stocked_JLC_positions=sum(bool(x.get('jlcpcb')and x['jlcpcb']['status']=='available')for x in rows),external_or_wire_positions=sum(not(x.get('jlcpcb')and x['jlcpcb']['status']=='available')for x in rows),changed_electronic_positions=[x['ref']for x in rows if x['changed']and x['ref']not in('J1','J2')],wire_raw_material_positions=['J1','J2'],old_native_MPN_and_value_match=True,old_native_pad_count=sum(x['pads']for x in native.values()),RFQ13_design_files_retained=len(files),all_RFQ13_bound_bytes_unchanged=True,product_native_CAD_edited=False,toolkit_lock=lock,independent_demag_frequency_Hz=freq,new_ERC_DRC_CAM_claimed=False,all_parts_electrically_qualified=False,PCB_ready_for_new_parts=False))
put('checks/baseline-native-parts.json',native)
put('checks/baseline-source-binding.json',dict(base_commit='b31e08da7c2b7e2b81717df6e9f2d094b04fed39',source='supplier-review-13/design',files=files,all_unchanged=True))
cmd=[str(W/'kicad-10.0.6/bin/python.exe'),str(R/'pcb-toolkit.py'),'doctor','--kicad-cli',str(W/'kicad-10.0.6/bin/kicad-cli.exe'),'--cad-python',str(W/'kicad-10.0.6/bin/python.exe')]
r=subprocess.run(cmd,capture_output=True,timeout=60);stdout=r.stdout.decode('utf-8',errors='replace');stderr=r.stderr.decode('utf-8',errors='replace');doctor=json.loads(stdout)
assert r.returncode==0 and doctor['passed']
put('checks/toolkit-doctor.json',dict(command=cmd,exit_code=r.returncode,report=doctor,stderr=stderr,limitation='The launcher reports passed, but a subprocess reader emits UnicodeDecodeError on the Polish host. Retained as an environment warning, not a clean stderr claim. Pin and actual baseline CAD bytes are checked separately.'))
print('CAT15 PASS:33 actual references, stock routes and exact old/native MPNs; all baseline CAD bytes preserved. New electrical/PCB release remains blocked.')

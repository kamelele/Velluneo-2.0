from pathlib import Path
import json,hashlib,csv,shutil
H=Path(__file__).resolve().parent;C=H/'candidate';N=H/'native';REL=C/'release-refinement-R2';REL.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
eco=json.loads((C/'startup-correction.SB01-R2.json').read_text());eco['analysis_files']={}
for folder in ['startup','protection']:
 d=json.loads((H/folder/'handoff.json').read_text());eco['analysis_files'][folder+'_handoff_sha256']=sha(H/folder/'handoff.json')
save(C/'startup-correction.SB01-R2.json',eco)
part=next(x for x in json.loads((C/'bom-build.json').read_text())['components']if x['ref']=='L1')
p=C/'source-basis.SB01.json';d=json.loads(p.read_text());d['revision']='SC09-SB01-R2';d['part_changes']['L1']=part;d['R2_precedence']='L1 legacy slot now PR02FS100 resistor, not inductor. Earlier LC/stock/thermal claims are historical; new startup-correction.SB01-R2.json and R2 engineering reports govern.';save(p,d)
p=C/'footprint-geometry.json';d=json.loads(p.read_text());d['L1'].update(mpn=part['mpn'],max_body_bbox_xy_mm=[-4.4519,-1.95,2.9169,1.95],planned_max_above_PCB_mm=16,sources=['https://www.vishay.com/docs/28915/pr02fs.pdf'],design_basis='PR02-FS max D3.9/bodyL10/totalL12/lead.78±.05; upright pad1 over original5.0038mm pad pair. Original conservative circular9.3mm courtyard retained.',notes=['Physical legacyL1 slot now resistor; R10inanalysis. NativeF.Fabcircle remains original conservative reservation, not literal resistor body.', '2mm standoff plus12mm total plus2mm turn =16mm planning; actual formed-lead/support inspection required. 0.1981mm nominal circle-envelope margin is not tolerance qualification.']);save(p,d)
p=C/'power-supply-specification.json';d=json.loads(p.read_text());d['revision']='SC09-SB01-R2';d['R2_overrides']={'L1':part,'old_LC_transient_and_choke_thermal_sections':'Historical; do not apply to R2 resistor','incremental_R10_loss_at60mArms_W':0.4059,'loss_limit':'Calculated resistor-only loss with112.75ohm screen; actual RMS input/filter current unmeasured; previous total-driver-loss figures do not include this changed part','provisional_resistor_body_stop_C':90,'no_powered_tests':True};save(p,d)
p=C/'thermal-planning.json';d=json.loads(p.read_text());d['R2_override']={'L1':'PR02FS100 resistor at legacy L1 slot; prior choke DCR/core estimates historical','resistor_loss_at60mArms_screen_W':.4059,'resistor_loss_at80mArms_screen_W':.7216,'provisional_body_stop_C':90,'total_loss_and_closed_enclosure_temperature':'Unverified; previous whole-base loss/temperature values not retained as R2 guarantees'};save(p,d)
p=C/'prototype-gates.SB01.json';d=json.loads(p.read_text());d['revision']='SC09-SB01-R2';d['R2_open_items']=['Hot repetitive/restart pulse behavior of PR02FS100 at actual board temperature','Actual RMS current, resistor body temperature and EMI with RC instead ofLC','Output OVP dynamics, short faults, surge and maximumT1winding/U1VDS remain measurement-gated','C6 cannot be guaranteed protected from U1D-Sshort by ordinary input fuse; no fail-safe claim','Unpowered formed-lead fit and restraint for legacyL1 resistor'];save(p,d)
with (REL/'BOM.csv').open('w',newline='',encoding='utf-8')as f:
 w=csv.writer(f);w.writerow(['Reference','Value','MPN','Footprint','Quantity','DNP'])
 for c in json.loads((C/'bom-build.json').read_text())['components']:w.writerow([c['ref'],c['value'],c['mpn'],'E27SC09:SC09_'+c['ref'],1,''])
shutil.copy2(C/'release-refinement-R1/SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip',REL/'SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip')
shutil.copy2(N/'views/assembly-F.pdf',REL/'assembly-F.pdf');shutil.copy2(N/'views/assembly-B.pdf',REL/'assembly-B.pdf')
(REL/'BRINGUP_UNPOWERED.md').write_text('''# R2 unpowered inspection only

Fit PR02FS0201000KR500,100ohm/2W at legacyL1; do not install old3.3mH choke.
Retain RF1=FW20A47R0JA. Check exact resistor marking, sample lead diameter,
formed lead strain/support, >=2mm standoff and <=16mm planning height; retain
original C6 vent free space. Inspect high-voltage clearances including solder.
Check no short and intended continuity without power. This file authorizes no
energization. A qualified human must define setup/stop conditions separately.

Before powered acceptance measure both input rails, U1D-S and T1winding stress,
LED current/OVP/short response, R10RMS/bodytemperature and EMI at input/load/
temperature corners. Cold RC calculation does not close hot pulse or surge tests.
Record actual data, not a fabricated PASS. Stop at unexpected current/ringing,
any part limit, R10body90C provisional stop or COUT90V investigation threshold.
Thresholds are test planning, not protective trips. U1D-Sshort can overchargeC6;
do not perform that destructive fault test without a separately engineered setup.
''',encoding='utf-8')
p=C/'hardware.json';d=json.loads(p.read_text());d['procurement_revision']='SC09-SB01-R2';d['historical_release_note']='R1 release metadata is historical. R2engineering RC change at physicalL1; full releaseFAIL/no humanapproval/no order/no poweredtests. New fabrication copper identity independently checked; R1approval cannottransferto changed assembly.'
for key,rows in d['release_files'].items():
 for row in rows:
  row.pop('snapshot',None)
  if key=='gerbers':name='SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip'
  elif key=='bom':name='BOM.csv'
  elif key=='bringup_plan':name='BRINGUP_UNPOWERED.md'
  elif key=='assembly_drawing':name='assembly-F.pdf'
  else:continue
  row['path']='release-refinement-R2/'+name;row['sha256']=sha(REL/name)
save(p,d)
print('R2 metadata and assembly package updated; all stage approvals remain unasserted.')

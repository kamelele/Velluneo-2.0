from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os
W=Path(__file__).parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'led-compatibility-19'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
j=json.loads((D/'results.json').read_text(encoding='utf-8'));binding=json.loads((D/'input-binding.json').read_text(encoding='utf-8'))
assert all(sha(P/p)==h for p,h in binding['repository_files'].items())
os.environ['KICAD_CLI']=str(W/'kicad-10.0.6/bin/kicad-cli.exe');os.environ['KICAD_PYTHON']=str(W/'kicad-10.0.6/bin/python.exe')
r=subprocess.run([sys.executable,str(R/'pcb-toolkit.py'),'doctor'],cwd=R,capture_output=True,timeout=120);assert r.returncode==0,(r.stdout,r.stderr);(D/'toolkit-doctor.json').write_bytes(r.stdout)
(D/'measurement-plan.md').write_text('''# LED19 verification plan - no measurements performed

First panel candidate: seven series JB2835BWT-G-H40GA0000-N0000001,4000K/80CRIclass.
Begin panel-only characterization with an isolated/current-limited laboratory DC
source and a controlled thermal fixture. This is not permission to energize the
unfinished mains driver. Use exact reel/bin identity, calibrated current/voltage,
photometry and a properly attached solder-point temperature sensor; do not infer
junction temperature directly from an uncorrected infrared surface reading.

Record DC voltage/current and LED solder-point temperature at303.624/319/336.057mA,
cold start and stabilized heating, with the actual selected substrate/TIM/heat path.
The currentpoints are C16 calculations at assumed transformer delivery0.90, not
complete guaranteed operating bounds. Characterize actual driver current separately.
Use95C solder-point and115C estimatedjunction as conservative engineering stop
targets from the preceding thermal study, not manufacturer life guarantees or
approved final product limits. The maker125C junction absolute limit remains binding.
Actual Rjs uncertainty, sensor error and spatial gradients must be accounted for.

For the complete lamp, retain the accepted230Vac/50Hz,25+/-1Cambient,base-up,complete
milky diffuser and stabilization protocol. Require at least750lm with the laboratory
uncertainty allowance; no850lm rejection ceiling after the owner's21Novembermessage.
Record actualflux rather than asserting959lm. Check4000+/-200K/Ra>=80 under the
actual drive and thermal conditions. Eventual three-colour matching remains due.

When the driver is qualified for controlled bring-up, capture actual LED ripple and
startup/transient current, VDD margin and switchingfrequency over line/load/temperature.
Check first/repeatedfaults, clamp, PstLM/SVM, transformer surroundingambient<=50C,
driver componenttemperatures and final housing/service conditions using the existing
C16bring-upplan. No finished safety, lifetime, EMC or manufacturing acceptance follows
from the present typical-curves calculation.
''',encoding='utf-8')
(D/'toolkit-impact.json').write_text(json.dumps(dict(toolkit_manifest_sha256='b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97',doctor_passed=True,scope='Analytical task and explicit owner upper-flux addendum; no CAD/library/rules/BOM/manufacturing/process changes',old_upper_flux_rejection_superseded=True,old_frozen_packets_preserved=True,numerical_checks=j['numerical_verification'],formal_release_check_not_repeated_reason='No CAD or release-file changes. Current task does not claim manufacturing release; existing process/physical/human gates remain. Product acceptance must use the new owner addendum, not the historical850lm ceiling.',physical_measurements=False),indent=2)+'\n',encoding='utf-8')
for n in ['check_led19.py','update_led19_docs.py','freeze_led19.py']:shutil.copyfile(W/n,D/n)
shutil.copyfile(W/'led19-run.log',D/'calculation-run.log')
idx=R/'hardware/E27/workflow/project-index.md';s=idx.read_text(encoding='utf-8');head='''## Current LED/driver compatibility and higher-flux acceptance - LED19, 21 November 2026

[LED19](specification-reset/led-compatibility-19/README.md) checks the currentC16
319mA supply against exact CreeG-class candidates. Owner explicitly permits higher
lumens; requirements-and-plan.md revision13 removes only the850lm rejectionceiling.
Retain seven seriesH40/4000K as first verificationpanel: typical20.652V/6.588W,
~959lm at assumedtau0.87 andcalculated85Cjunctionfluxreference. Conditionalcurrent
points303.624..336.057mA give918..1004lm; this is not measured orguaranteed output.
Thermalderating/actualVf/currentripple/bin/diffuser/CCT/CRI/life andfinishedpanel
remain unqualified. SixLEDsbias andeightLEDsvoltage issues prevent blindcountchanges;
R9-onlydimming does not pass the existingfrequency screen. No driverCAD/BOM/rule,
C17manufacturing orapprovedstage change. Higherflux isnot a blocker; thermal/safety
requirements remain. Eventual2700/6500familycompatibility is not closed.

'''
if '## Current LED/driver compatibility and higher-flux acceptance - LED19,'not in s:idx.write_text(s.replace('# E27 workflow index\n\n','# E27 workflow index\n\n'+head,1),encoding='utf-8')
# Freeze genuine task inputs and outputs. Actual review/lifecycle records excluded.
paths=[p for p in sorted(D.rglob('*'))if p.is_file()and not any(x in p.relative_to(D).parts for x in ('.work','reviews','__pycache__'))and p.name not in ('frozen-files.json','review-record.json','integration-record.md')]
records=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size)for p in paths]
records.append(dict(path=(P/'requirements-and-plan.md').relative_to(R).as_posix(),sha256=sha(P/'requirements-and-plan.md'),bytes=(P/'requirements-and-plan.md').stat().st_size))
body=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();(D/'frozen-files.json').write_text(json.dumps(dict(body_sha256=body,base_commit=j['source_commit'],files=records,scope='LED19data andowner-authorizedrevision13append-onlyspecaddendum. Reviews/lifecycle/indexexcluded. NoCADchange.'),indent=2)+'\n',encoding='utf-8');print(body,len(records))

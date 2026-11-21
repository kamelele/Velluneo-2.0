from pathlib import Path
import json,hashlib,sys
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-toolkit-11';E=D/'design'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
b=json.loads((D/'isolation-policy-baseline.json').read_text());h=json.loads((E/'hardware.json').read_text())
h['fabrication']['service']='FR4-4L-1oz-epoxy-filled-capped-routed'
h['product']['scoped_clearances']=[dict(id='HV_QUIET' if r['min_mm']==3 else 'PRIMARY_SECONDARY',nets_a=r['side_a'],nets_b=r['side_b'],min_mm=r['min_mm'])for r in b['scoped_pairs']]
h['product']['copper_layers']=['F.Cu','In1.Cu','In2.Cu','B.Cu'];h['product']['spatial_file']='spatial-constraints.json'
h['severity_overrides']={'board':{'npth_inside_courtyard':'error','pth_inside_courtyard':'error'}}
h['configuration_migration']='configuration-migration.json'
p=E/'Velluneo_driver.kicad_pro';pro=json.loads(p.read_text());pro['board']['design_settings']['rules']['min_via_diameter']=.7
for c in pro['net_settings']['classes']:
 if c['name']=='Default':c['via_diameter']=.7;c['via_drill']=.3
put(p,pro)
put(E/'configuration-migration.json',dict(schema_version=1,legacy_rules_sha256=sha(E/'Velluneo_driver.kicad_dru'),legacy_project_sha256=sha(p),net_names=b['declared_nets'],reviewed_by='/root coordinator: bounded preservation review',reason='Owner requested explicit toolkit extension. Preserve legacy exact-net 3/10mm rules and all stronger native settings; add four-layer managed exclusion. This is not human stage, supplier or insulation qualification approval.'))
basis=E/'spatial-basis.md';basis.write_text('''# Declared allocation preservation basis — TOOLKIT11

The owner selects one rectangular driver, separate from the round LED insert.
The selected existing allocation is 45 x 60 mm. This coordinator decision restates
the retained legacy boundary before managed-area generation: native outline
[77.5,70,122.5,130] mm and protected rectangle [77.5,82.9,122.5,92.135] mm on all
four copper layers. No copper, via, pad or poured zone may enter this rectangle.
The existing unmanaged no-new-copper exclusion remains in place unchanged.
These are allocation preservation requirements, not independent normative
creepage tables, qualified transformer construction or approval of the layout.
The exact-net 3 mm HV/quiet and 10 mm primary/secondary requirements remain
separate from this rectangle and apply to actual object spacing on every layer.

PB-ROUTING requires the selected graph and dedicated measurement copper to remain
unchanged. U1 current sense connects to the shunt-positive measurement node;
switching and auxiliary returns must retain their separate C1/shunt/source branch
topology. C1 is the primary return star reference. The current layout is checked
geometrically using branch cuts and projected separation; no full negative Kelvin
connection, EMI behavior, powered fault behavior or physical performance is inferred.
The UCC28711 application layout guidance and previously recorded current-loop
review are the functional basis; a geometry pass cannot replace powered tests.
This newly explicit contract awaits the authorized person's final snapshot review.
''',encoding='utf-8')
card=dict(id='DRIVER_POWER_SENSE',requirement_id='PB-ROUTING',basis='Preserve selected circuit/return topology and current-sense separation. See spatial-basis.md; geometric audit is not EMI/fault qualification.')
records={
'sensitive_nets':(['SENSE','CS'],'Preserve dedicated current-sense copper and review HV projection on every copper layer.'),
'switching_nodes':(['Q1','T1','U1','D1'],'Retain selected switching node placement and source-bound loop review.'),
'return_paths':(['C1','R9','Q1','T1'],'Retain separate capacitor/shunt/source/auxiliary branches; no shared shortcut bypass.'),
'loops':(['C1','T1','Q1','R9'],'Retain compact power loop and approved graph while isolating measurement path.'),
'kelvin_connections':(['R9','U1'],'Preserve dedicated positive sense connection; negative return is branch-controlled, not claimed as a complete Kelvin pair.')}
for k,(objects,rationale)in records.items():card[k]=dict(objects=objects,rationale=rationale)
doc=dict(schema_version=1,revision='toolkit11-all-four-copper-preservation',basis='Explicit coordinator restatement of legacy allocation before managed generation; source provenance and physical qualification limits retained.',basis_sources=[dict(path=basis.name,sha256=sha(basis))],outline_mm=[77.5,70,122.5,130],areas=[dict(id='ISOLATION',rectangle_mm=[77.5,82.9,122.5,92.135],layers=h['product']['copper_layers'],disallow=['track','via','pad','zone'],basis='Retain existing primary/secondary no-new-copper allocation on all enabled layers; additional managed constraint, not a normative clearance substitute.',exceptions=[])],blocks=[card],approval=None)
put(E/'spatial-constraints.json',doc)
for name in ('spatial-basis.md','spatial-constraints.json','configuration-migration.json'):
 if name not in h['source_files']:h['source_files'].append(name)
put(E/'hardware.json',h)
print('Prepared explicit scoped/four-layer contracts; no approval fabricated.')

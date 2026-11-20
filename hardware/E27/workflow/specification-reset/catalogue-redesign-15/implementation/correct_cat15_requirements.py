from pathlib import Path
import json
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'catalogue-redesign-15'
q=P/'requirements.json';r=json.loads(q.read_text(encoding='utf-8'))
r['revision']='specification-contract-catalogue-sourcing-7'
items=[
 ('R-SOURCING','release','Every driver-board electronic component must have an exact orderable manufacturer part. Prefer actual JLCPCB assembly catalogue stock; reputable external distributors are acceptable when JLCPCB cannot supply it.','Before final parts/assembly release, verify manufacturer identity, relevant electrical/mechanical ratings, exact source code, dated stock/leadtime, MOQ/packing, intended quantity plus assembly attrition, and supplier acceptance of external parts. Distinguish purchase availability from qualified circuit operation; wire raw material is not a completed harness.'),
 ('R-STOCK-T1','schematic','The driver transformer must be a complete factory-wound off-the-shelf manufacturer catalogue part. No custom/customer winding, custom magnetic build or bare core/bobbin kit is permitted.','Before accepting the revised schematic/library basis, identify the complete purchasable transformer and source, independently verify real pins/winding taps/polarity and dimensions, and establish suitability for declared normal/fault/startup and insulation conditions. A catalogue listing alone does not close electrical qualification.')]
r['requirements']=[x for x in r['requirements']if x['id']not in{v[0]for v in items}]
for id,gate,text,acceptance in items:
 r['requirements'].append(dict(id=id,revision='owner-instruction-2026-11-20',owner='Owner (mandatory sourcing intent); coordinator (implementation and qualification)',text=text,basis='catalogue-redesign-15/owner-sourcing-instruction.md; explicit owner request in current conversation',acceptance=acceptance,gate=gate,implementation=[dict(subsystem='BASE',object='CAT15 proposed purchase map and engineering holds; actual revised CAD remains incomplete',path='catalogue-redesign-15/selected-bom.json')],method='review',evidence_ids=[]))
q.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(D/'owner-sourcing-instruction.md').write_text('''# Owner sourcing instruction —20 November2026

The owner explicitly requires every component to be orderable, preferably through
the JLCPCB assembly catalogue. An outside shop/distributor is acceptable for a part
such as the transformer when JLCPCB does not stock it. The transformer must be
supplied complete and factory-wound; the project will not wind it or commission a
custom winding. These are mandatory product constraints, not a supplier's text.

This instruction authorizes component research and a concrete redesign proposal.
It does not accept an unqualified transformer application, waive spacing, approve
a new schematic/placement/release snapshot or authorize a purchase/payment.
Configured requirements R-SOURCING and R-STOCK-T1 carry the instruction forward;
their empty evidence lists truthfully retain the outstanding implementation gates.
Historic scope reviews keep their original digest and are not silently renewed.
''',encoding='utf-8')
print('Added mandatory R-SOURCING/R-STOCK-T1; no fabricated acceptance evidence or old evidence refresh.')

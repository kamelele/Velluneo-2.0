"""Execute contract evidence checks for a synthetic workflow tabletop scenario.

Does not launch agents, enforce a production state machine or create human approvals.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import product_contracts as contracts


def main():
    original=json.loads((ROOT/'examples/multi-board/requirements.json').read_text(encoding='utf-8'))
    notes=(ROOT/'examples/multi-board/design-review.md').read_bytes()
    outcomes=[]
    for case in ['incompatible-candidate','corrected-with-stale-review','ready-for-human-review']:
        folder=ROOT/'.work/agent-workflow-walkthrough'/case
        folder.mkdir(parents=True,exist_ok=True)
        document=copy.deepcopy(original)
        document['revision']='2-draft' if case=='incompatible-candidate' else '2'
        document['interfaces'][0]['revision']='2'
        document['requirements'][1]['revision']='2'
        document['interfaces'][0]['endpoints'][1]['pins'][0]['current_ma']=650
        evidence_notes=notes
        if case!='incompatible-candidate':
            document['interfaces'][0]['endpoints'][0]['pins'][0]['current_ma']=800
            startup=copy.deepcopy(document['requirements'][1])
            startup.update(id='REQ-STARTUP',revision='1',
                text='Fictional startup load is 650 mA, within the agreed 800 mA source budget.',
                acceptance='Review the 650/800 mA declared startup budget and preserve fault response.')
            document['requirements'].append(startup)
            document['interfaces'][0]['requirements'].append('REQ-STARTUP')
            evidence_notes=(
                '# Synthetic corrected design review\n\n'
                'Fictional source budget 800 mA and startup load 650 mA. Protection is retained.\n'
                'REQ-STARTUP is added. Existing UART/mechanical agreements are unchanged.\n'
                'This is not actual human approval, measurement or manufacturing qualification.\n'
            ).encode()
        (folder/'design-review.md').write_bytes(evidence_notes)
        if case=='ready-for-human-review':
            for item in document['evidence']:
                item.update(intent_digest=contracts.intent_digest(document),
                            sha256=hashlib.sha256(evidence_notes).hexdigest())
        (folder/'requirements.json').write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        report=contracts.evaluate(folder,'requirements.json','schematic')
        (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        expected=case=='ready-for-human-review'
        messages=[item['message'] for item in report['errors']]
        specific=(any('current budget' in x for x in messages) if case=='incompatible-candidate' else
                  any('different intent' in x for x in messages) if case=='corrected-with-stale-review' else
                  report['passed'])
        outcomes.append({'case':case,'expected_contract_pass':expected,'actual_contract_pass':report['passed'],
            'expectation_met':report['passed']==expected and specific,
            'intent_digest':report.get('intent_digest'),'errors':report['errors']})
    summary={'validation_mode':'synthetic_tabletop_with_executed_contract_checks',
        'actual_agents_launched':0,'actual_human_approvals':0,'cad_edited':False,
        'executed_contract_cases':outcomes,'passed':all(x['expectation_met'] for x in outcomes),
        'final_workflow_state':'awaiting_human_review',
        'manual_tabletop_cases':9,
        'scope_note':'Process cases are reviewed expectations, not a runtime transition validator. Real pilot remains #20.'}
    (ROOT/'reports/agent-workflow-walkthrough.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':summary['passed'],'executed_cases':len(outcomes),
                      'final_state':summary['final_workflow_state'],'actual_agents_launched':0}))
    return 0 if summary['passed'] else 1


if __name__=='__main__':raise SystemExit(main())

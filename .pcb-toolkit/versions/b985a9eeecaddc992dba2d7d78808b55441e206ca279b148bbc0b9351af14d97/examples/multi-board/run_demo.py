"""Reproduce valid and deliberately broken product contracts without KiCad."""
import copy
import json
import shutil
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import product_contracts as contracts


def main():
    original=json.loads((Path(__file__).parent/'requirements.json').read_text(encoding='utf-8'))
    outcomes=[]
    for case in ['valid','missing-requirement','interface-conflict','stale-evidence','unknown-before-placement']:
        folder=ROOT/'.work/multi-board-demo'/case
        folder.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(Path(__file__).parent/'design-review.md',folder/'design-review.md')
        document=copy.deepcopy(original)
        stage='placement'
        if case=='missing-requirement':
            document['requirements']=[r for r in document['requirements'] if r['id']!='REQ-POWER']
        elif case=='interface-conflict':
            document['interfaces'][0]['endpoints'][0]['pins'][0]['voltage_max_v']=12
        elif case=='stale-evidence':
            document['requirements'][0]['acceptance']='Changed acceptance without a new review'
        elif case=='unknown-before-placement':
            document['interfaces'][2]['geometry']['tolerance_mm']=None
            document['unknowns']=[{'id':'UNKNOWN-FIT','record_id':'IF-FIT','field':'geometry.tolerance_mm',
                'owner':'example-mechanical-owner','question':'What tolerance is approved?',
                'status':'open','blocks_stage':'placement'}]
        # Rebinding is synthetic setup so conflict/missing-field tests isolate
        # those checks. It is never a real review or an approval shortcut.
        if case!='stale-evidence':
            for item in document['evidence']:item['intent_digest']=contracts.intent_digest(document)
        (folder/'requirements.json').write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        report=contracts.evaluate(folder,'requirements.json',stage)
        (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        expected=case=='valid'
        outcomes.append({'case':case,'expected_pass':expected,'actual_pass':report['passed'],
                         'expectation_met':report['passed']==expected,
                         'errors':report['errors'],'blocked_stages':report['blocked_stages']})
    summary={'synthetic':True,'not_human_approval':True,'cases':outcomes,
             'passed':all(x['expectation_met'] for x in outcomes)}
    (ROOT/'reports/product-contract-example.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return 0 if summary['passed'] else 1


if __name__=='__main__':raise SystemExit(main())

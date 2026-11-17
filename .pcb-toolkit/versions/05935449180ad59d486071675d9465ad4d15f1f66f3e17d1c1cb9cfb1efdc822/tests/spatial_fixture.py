"""Original spatial requirements; synthetic approvals exercise gates only."""
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import spatial


def install(root,config,areas=None):
    basis=root/'spatial-basis.md';basis.write_text('Fictional 40 mm square test board. A protected rectangle tests geometry only.\n',encoding='utf-8')
    document={'schema_version':1,'revision':'fixture-1','basis':'Independent fictional fixture specification',
        'basis_sources':[{'path':basis.name,'sha256':hashlib.sha256(basis.read_bytes()).hexdigest()}],
        'outline_mm':[0,0,40,40],'areas':areas or [],'blocks':[],
        'no_blocks_reason':'Synthetic fixture has no functional analog/power blocks; not a product claim.'}
    document['approval']={'approved_by':'synthetic-test-not-human-approval',
                          'evidence':'Original fixture gate test only','intent_digest':spatial.intent_digest(document)}
    config['product']['spatial_file']='spatial-constraints.json'
    (root/'spatial-constraints.json').write_text(json.dumps(document,indent=2),encoding='utf-8')
    return document


def area(exception=None,rectangle=None,layers=None,disallow=None):
    return {'id':'QUIET','rectangle_mm':rectangle or [8,4,12,6],'layers':layers or ['F.Cu'],
            'disallow':disallow or ['track','via'],'basis':'Deliberate fixture boundary, not a design recommendation',
            'exceptions':[] if exception is None else [{'net':exception,'reason':'Local fixture exception',
                         'approved_by':'synthetic-test-not-human-approval','evidence':'Fixture only'}]}

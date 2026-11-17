"""Independent synthetic intent; never derive expected topology from exported CAD."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import connectivity


def approve(document):
    document['approval']={'approved_by':'synthetic-test-not-real-human-approval',
                          'evidence':'original acceptance fixture only; never manufacture',
                          'intent_digest':connectivity.intent_digest(document)}
    return document


def empty(folder):
    document={'schema_version':1,'revision':'1','basis':'Original empty CAD gate fixture',
              'basis_sources':[],'components':[],'nets':[],'no_connects':[], 'barriers':[],
              'empty_design_reason':'Synthetic empty schematic for gate acceptance tests, not a product.'}
    approve(document)
    (folder/'intended-connectivity.json').write_text(json.dumps(document,indent=2)+'\n',encoding='utf-8')
    return document

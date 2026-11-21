import copy
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import spatial
import pcb_rules as rules
import spatial_fixture as fixture


class SpatialTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.config=rules.read(rules.ROOT/'templates/project/hardware.json')
        self.config.update(name='board',source_files=[])
        self.config['fabrication']['vendor']='jlcpcb';self.config['assembly']['mode']='supplier'
        self.doc=fixture.install(self.root,self.config,[fixture.area()])
        _,_,self.values=rules.resolve(self.config)
        self.classes=rules.project_settings('board',self.values,[])['net_settings']

    def save(self):rules.write(self.root/'spatial-constraints.json',self.doc)
    def load(self):self.save();return spatial.load(self.root,self.config,self.values,self.classes)

    def test_one_resolved_payload_and_drc_scope(self):
        model=self.load();self.assertEqual(model['payload']['minimums_mm'],self.values)
        self.assertEqual(model['payload']['net_settings'],self.classes)
        self.assertIn("A.intersectsArea('HW-SPATIAL-QUIET')",spatial.rules(model))
        self.assertIn('disallow track via',spatial.rules(model))

    def test_invalid_geometry_and_layers_fail(self):
        for key,value in [('rectangle_mm',[1,1,1,2]),('rectangle_mm',[0,0,41,5]),('layers',['In1.Cu']),('disallow',['anything'])]:
            before=copy.deepcopy(self.doc);self.doc['areas'][0][key]=value
            with self.assertRaises(ValueError):self.load()
            self.doc=before

    def test_injection_or_unapproved_exception_fails(self):
        self.doc['areas']=[fixture.area('A')];self.doc['areas'][0]['exceptions'][0]['net']="A' || true"
        with self.assertRaises(ValueError):self.load()
        self.doc['areas']=[fixture.area('A')];self.doc['areas'][0]['exceptions'][0]['evidence']=''
        with self.assertRaises(ValueError):self.load()

    def test_independent_basis_hash_must_match(self):
        (self.root/'spatial-basis.md').write_text('Changed basis')
        with self.assertRaisesRegex(ValueError,'basis changed'):self.load()

    def test_block_cards_cannot_omit_topology_topics(self):
        rules.write(self.root/'requirements.json',{'requirements':[{'id':'REQ-PWR'}]})
        self.doc['blocks']=[{'id':'POWER','basis':'Datasheet','requirement_id':'REQ-PWR'}]
        with self.assertRaisesRegex(ValueError,'card incomplete'):self.load()

    def test_consumer_paths_and_basis_are_tracked(self):
        paths={p.name for p in spatial.tracked_inputs(self.root,self.config)}
        self.assertEqual(paths,{'spatial-constraints.json','spatial-basis.md','placement-input.json','routing-input.json'})

    def test_pre_cad_prepare_identical_consumer_inputs(self):
        extra,conflicts,model=spatial.prepare(self.root,self.config,self.values,self.classes)
        self.assertEqual(conflicts,[])
        self.assertEqual(extra[spatial.CONSUMERS['placement']],extra[spatial.CONSUMERS['routing']])
        self.assertEqual(json.loads(extra[spatial.CONSUMERS['routing']])['constraints_digest'],model['digest'])

    def test_settings_or_exception_changes_invalidate_digest(self):
        before=self.load()['digest'];self.values['track_width']+=.1
        self.assertNotEqual(before,self.load()['digest'])
        before=self.load()['digest'];self.doc['areas']=[fixture.area('A')]
        self.assertNotEqual(before,self.load()['digest'])

    def test_unapproved_or_changed_consumer_inputs_are_rejected(self):
        extra,_,_=spatial.prepare(self.root,self.config,self.values,self.classes)
        for path,data in extra.items():
            p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        with patch.object(spatial,'geometry',return_value={'errors':[],'inventory':{}}):
            self.assertTrue(spatial.verify(self.root,self.config,self.values,self.classes)['passed'])
            self.doc['revision']='changed';self.save()
            report=spatial.verify(self.root,self.config,self.values,self.classes)
            self.assertFalse(report['passed']);self.assertTrue(any('approval' in e for e in report['errors']))
            self.assertTrue(any('routing consumer' in e for e in report['errors']))

    def test_declared_block_must_link_existing_requirement(self):
        rules.write(self.root/'requirements.json',{'requirements':[{'id':'REQ-PWR'}]})
        self.doc['blocks']=[{'id':'POWER','basis':'Datasheet','requirement_id':'UNKNOWN'}]
        with self.assertRaisesRegex(ValueError,'unknown requirement'):self.load()

    def test_complete_block_card_retains_review_topics(self):
        rules.write(self.root/'requirements.json',{'requirements':[{'id':'REQ-PWR'}]})
        block={'id':'POWER','basis':'Independent datasheet review','requirement_id':'REQ-PWR'}
        for topic in ['sensitive_nets','switching_nodes','return_paths','loops','kelvin_connections']:
            block[topic]={'objects':[],'rationale':'Fictional structural test; no physical claim'}
        self.doc['blocks']=[block]
        self.assertEqual(self.load()['payload']['blocks'],[block])
if __name__=='__main__':unittest.main()

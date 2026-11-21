import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import scoped_policy as policy
import configuration as cfg

class ScopedPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.old={'board':{'design_settings':{'rules':{'min_clearance':.25,'min_track_width':.3,'min_through_hole_diameter':.3,'min_via_annular_width':.2,'min_via_diameter':.7,'min_copper_edge_clearance':.5,'min_silk_clearance':.15},'rule_severities':{'clearance':'error'}}},'erc':{'rule_severities':{'pin_to_pin':'error'},'pin_map':[[0,2],[2,0]]},'net_settings':{'classes':[{'name':'Default','clearance':.25,'track_width':.3}],'netclass_patterns':[]}}
        self.config={'name':'test','configuration_migration':'migration.json','product':{'scoped_clearances':[{'id':'HVQ','nets_a':['H'],'nets_b':['Q'],'min_mm':3},{'id':'PS','nets_a':['H','Q'],'nets_b':['S'],'min_mm':10}]}}
        self.legacy='(version 1)\n(rule "OLD_PS" (condition "((A.NetName == \'H\' || A.NetName == \'Q\') && B.NetName == \'S\') || (A.NetName == \'S\' && (B.NetName == \'H\' || B.NetName == \'Q\'))") (constraint clearance (min 10 mm)))\n(rule "OLD_HVQ" (condition "(A.NetName == \'H\' && B.NetName == \'Q\') || (A.NetName == \'Q\' && B.NetName == \'H\')") (constraint clearance (min 3 mm)))\n'
        (self.root/'test.kicad_pcb').write_text('(kicad_pcb (net "H") (net "Q") (net "S") (property "note" "(net FAKE)"))')
        (self.root/'test.kicad_pro').write_text(json.dumps(self.old))
        self.bind(self.legacy)
    def bind(self,text):
        (self.root/'test.kicad_dru').write_text(text)
        self.descriptor={'schema_version':1,'legacy_rules_sha256':cfg.sha((self.root/'test.kicad_dru').read_bytes()),'legacy_project_sha256':cfg.sha((self.root/'test.kicad_pro').read_bytes()),'net_names':['H','Q','S'],'reviewed_by':'synthetic test actor','reason':'synthetic regression; no approval'}
        (self.root/'migration.json').write_text(json.dumps(self.descriptor))
    def generated(self):
        return '(version 1)\n(rule "HW-clearance" (constraint clearance (min 0.250000mm)))\n(rule "HW-track" (constraint track_width (min 0.300000mm)))\n'+policy.rules(self.config)
    def review(self,generated=None,project=None):
        return policy.review_legacy(self.root,self.config,project or copy.deepcopy(self.old),generated if generated is not None else self.generated())
    def test_exact_inventory_and_complete_pair_proof(self):
        proof=self.review();self.assertEqual(proof['actual_net_names'],['H','Q','S']);self.assertEqual(proof['ordered_pair_cases'],25)
        rows={(r[0],r[1]):r[2:] for r in proof['effective_pairs']}
        self.assertEqual(rows['H','Q'],[3,3]);self.assertEqual(rows['Q','H'],[3,3]);self.assertEqual(rows['H','S'],[10,10]);self.assertEqual(rows['',''],[.25,.25]);self.assertEqual(rows['H','H'],[.25,.25])
    def test_omitted_generated_rules_rejected(self):
        with self.assertRaises(ValueError):self.review('(version 1)\n')
    def test_altered_generated_three_rejected(self):
        with self.assertRaises(ValueError):self.review(self.generated().replace('(min 3.000000mm)','(min 2.000000mm)'))
    def test_altered_generated_ten_rejected(self):
        with self.assertRaises(ValueError):self.review(self.generated().replace('(min 10.000000mm)','(min 9.000000mm)'))
    def test_declared_weakening_rejected(self):
        self.config['product']['scoped_clearances'][0]['min_mm']=2
        with self.assertRaises(ValueError):self.review()
    def test_strengthening_allowed(self):
        self.config['product']['scoped_clearances'][0]['min_mm']=4
        self.review()
    def test_hash_bypass_fails(self):
        self.descriptor['legacy_rules_sha256']='0'*64;(self.root/'migration.json').write_text(json.dumps(self.descriptor))
        with self.assertRaises(ValueError):self.review()
    def test_omitted_actual_net_rejected(self):
        self.descriptor['net_names'].remove('S');(self.root/'migration.json').write_text(json.dumps(self.descriptor))
        with self.assertRaises(ValueError):self.review()
    def test_unknown_scope_net_rejected(self):
        self.config['product']['scoped_clearances'][0]['nets_a']=['OTHER']
        with self.assertRaises(ValueError):self.review()
    def test_native_minimum_weakening_rejected(self):
        p=copy.deepcopy(self.old);p['board']['design_settings']['rules']['min_silk_clearance']=.1
        with self.assertRaises(ValueError):self.review(project=p)
    def test_severity_weakening_rejected(self):
        p=copy.deepcopy(self.old);p['board']['design_settings']['rule_severities']['clearance']='warning'
        with self.assertRaises(ValueError):self.review(project=p)
    def test_erc_matrix_change_rejected(self):
        p=copy.deepcopy(self.old);p['erc']['pin_map'][0][1]=0
        with self.assertRaises(ValueError):self.review(project=p)
    def test_arbitrary_legacy_scope_rejected(self):
        self.bind('(version 1)\n(rule "bad" (condition "A.Layer == \'F.Cu\'") (constraint clearance (min 10mm)))\n')
        with self.assertRaises(ValueError):self.review()
    def test_downgrade_override_refused(self):
        p=copy.deepcopy(self.old);self.config['severity_overrides']={'board':{'clearance':'warning'}}
        with self.assertRaises(ValueError):policy.apply_to_expected(p,self.config)
    def test_error_override_allowed(self):
        p=copy.deepcopy(self.old);p['board']['design_settings']['rule_severities']['clearance']='warning';self.config['severity_overrides']={'board':{'clearance':'error'}}
        self.assertEqual(policy.apply_to_expected(p,self.config)['board']['design_settings']['rule_severities']['clearance'],'error')
    def test_duplicate_and_unsafe_exact_names_rejected(self):
        for values in [['H','H'],['H*'],["H' || A.NetName == 'Q"]]:
            self.config['product']['scoped_clearances'][0]['nets_a']=values
            with self.assertRaises(ValueError):policy.rules(self.config)
    def test_actual_board_regular_validation(self):
        policy.validate_board(self.root,self.config)
        self.config['product']['scoped_clearances'][0]['nets_a']=['OTHER']
        with self.assertRaises(ValueError):policy.validate_board(self.root,self.config)
    def test_no_scoped_policy_preserves_existing_preview_scope(self):
        self.config['product']['scoped_clearances']=[]
        (self.root/'test.kicad_pcb').write_text('Synthetic non-CAD snapshot fixture')
        policy.validate_board(self.root,self.config)
    def test_owned_generated_policy_cannot_be_weakened(self):
        old_generated=self.generated();self.bind(old_generated)
        self.config['product']['scoped_clearances'][0]['min_mm']=2
        with self.assertRaises(ValueError):self.review()
    def test_owned_generated_disallow_cannot_disappear(self):
        extra='(rule "AREA" (condition "A.intersectsArea(\'X\')") (constraint disallow track via))\n';self.bind(self.generated()+extra)
        with self.assertRaises(ValueError):self.review(self.generated())
    def test_descending_legacy_precedence_rejected(self):
        self.bind(self.legacy+'(rule "LOWER" (constraint clearance (min 0.25mm)))\n')
        with self.assertRaises(ValueError):self.review()
    def test_owned_scope_removal_cannot_bypass_configuration_build(self):
        self.bind(self.generated())
        state={'schema_version':1,'managed':cfg.fields(self.old),'dru_sha256':cfg.sha((self.root/'test.kicad_dru').read_bytes())}
        (self.root/'.electronics-rules').mkdir();(self.root/'.electronics-rules/config-state.json').write_text(json.dumps(state))
        self.config['product']['scoped_clearances']=[];self.config['source_files']=[]
        plan=cfg.build(self.root,self.config,copy.deepcopy(self.old),'(version 1)\n(rule "HW-clearance" (constraint clearance (min 0.250000mm)))\n(rule "HW-track" (constraint track_width (min 0.300000mm)))\n',{'version':'synthetic-test'})
        self.assertTrue(any('Legacy scoped migration refused'in c for c in plan['conflicts']))

if __name__=='__main__':unittest.main()

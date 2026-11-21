"""Requirement/interface consistency and evidence freshness; no physical-proof claims."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import contract_fixture

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import product_contracts as pc
import pcb_rules as rules


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.doc=contract_fixture.install(self.root)
        shutil_path=ROOT/'templates/project/intended-connectivity.json'
        (self.root/'intended-connectivity.json').write_bytes(shutil_path.read_bytes())
        self.config=rules.read(ROOT/'templates/project/hardware.json')
        self.config.update(name='board',source_files=['board.kicad_pro','board.kicad_dru','board.kicad_pcb','board.kicad_sch'])
        self.config['fabrication']['vendor']='jlcpcb';self.config['assembly']['mode']='supplier'
        rules.write(self.root/'hardware.json',self.config)

    def save(self,rebind=False):
        if rebind:
            for evidence in self.doc['evidence']:
                evidence['intent_digest']=pc.intent_digest(self.doc)
        rules.write(self.root/'requirements.json',self.doc)

    def run_contract(self,stage='release',rebind=False):
        self.save(rebind)
        return pc.evaluate(self.root,'requirements.json',stage)

    def assert_blocked(self,needle=None,stage='release',rebind=False):
        report=self.run_contract(stage,rebind)
        self.assertFalse(report['passed'])
        if needle:self.assertTrue(any(needle in e['message'] for e in report['errors']),report['errors'])
        return report

    def test_complete_original_multiboard_example_and_evidence_levels(self):
        report=self.run_contract()
        self.assertTrue(report['passed'],report['errors'])
        self.assertEqual(len(report['matrix']),7)
        self.assertTrue(all(row['observed_levels']==['reviewed'] for row in report['matrix']))

    def test_missing_requirement_referenced_by_interface(self):
        self.doc['requirements']=[r for r in self.doc['requirements'] if r['id']!='REQ-POWER']
        self.assert_blocked('existing requirement IDs',rebind=True)

    def test_requirements_missing_acceptance_or_implementation(self):
        for key in ['acceptance','implementation']:
            original=copy.deepcopy(self.doc)
            self.doc['requirements'][0].pop(key)
            self.assert_blocked(rebind=True)
            self.doc=original

    def test_duplicate_ids_and_unknown_subsystems(self):
        original=copy.deepcopy(self.doc)
        self.doc['requirements'][0]['id']='POWER'
        self.assert_blocked('globally unique')
        self.doc=original
        self.doc['interfaces'][0]['endpoints'][0]['subsystem']='MISSING'
        self.assert_blocked('known subsystem')

    def test_explicit_unknown_blocks_placement_not_specification(self):
        self.doc['interfaces'][2]['geometry']['tolerance_mm']=None
        self.doc['unknowns']=[{'id':'UNKNOWN-FIT','record_id':'IF-FIT','field':'geometry.tolerance_mm',
            'owner':'mechanical-owner','question':'What tolerance is approved?',
            'blocks_stage':'placement','status':'open'}]
        self.save(rebind=True)
        early=pc.evaluate(self.root,'requirements.json','specification')
        self.assertTrue(early['passed'],early['errors'])
        self.assertIn('placement',early['blocked_stages'])
        late=pc.evaluate(self.root,'requirements.json','placement')
        self.assertFalse(late['passed'])
        self.assertEqual(late['open_questions'][0]['owner'],'mechanical-owner')

    def test_resolved_unknown_needs_resolution_and_fresh_evidence(self):
        self.doc['unknowns']=[{'id':'UNKNOWN-FIT','record_id':'IF-FIT','field':'geometry.tolerance_mm',
            'owner':'mechanical-owner','question':'What tolerance is approved?',
            'blocks_stage':'placement','status':'resolved'}]
        self.assert_blocked('resolution/evidence',rebind=True)
        self.doc['unknowns'][0].update(resolution='Reviewed fictional tolerance',evidence_ids=['EV-REVIEW'])
        self.assertTrue(self.run_contract(rebind=True)['passed'])
        self.doc['unknowns'][0]['evidence_ids']=['MISSING']
        self.assert_blocked('stale/missing/failed',rebind=True)

    def test_interface_voltage_conflict_with_fresh_review_hash(self):
        self.doc['interfaces'][0]['endpoints'][0]['pins'][0]['voltage_max_v']=12
        self.assert_blocked('voltage envelope',rebind=True)

    def test_interface_current_budget_conflict(self):
        self.doc['interfaces'][0]['endpoints'][0]['pins'][0]['current_ma']=100
        self.assert_blocked('current budget',rebind=True)

    def test_pinout_role_and_drive_conflicts(self):
        original=copy.deepcopy(self.doc)
        self.doc['interfaces'][0]['connections']=[{'a':'1','b':'2'},{'a':'2','b':'1'}]
        self.assert_blocked('roles/signals',rebind=True)
        self.doc=original
        self.doc['interfaces'][0]['endpoints'][1]['pins'][0]['direction']='source'
        self.assert_blocked('directions',rebind=True)

    def test_mapping_missing_duplicate_or_nonexistent_pins(self):
        original=copy.deepcopy(self.doc)
        for links in [[{'a':'1','b':'1'}],[{'a':'1','b':'1'},{'a':'1','b':'2'}],[{'a':'9','b':'1'},{'a':'2','b':'2'}]]:
            self.doc=copy.deepcopy(original);self.doc['interfaces'][0]['connections']=links
            self.assert_blocked('exactly once',rebind=True)

    def test_duplicate_pin_numbers(self):
        pins=self.doc['interfaces'][0]['endpoints'][0]['pins'];pins[1]['pin']='1'
        self.assert_blocked('unique strings',rebind=True)

    def test_firmware_protocol_and_parameters_must_agree(self):
        self.doc['interfaces'][1]['endpoints'][1]['parameters']['baud_hz']=9600
        self.assert_blocked('parameters conflict',rebind=True)

    def test_matching_unknown_firmware_values_cannot_pass(self):
        for endpoint in self.doc['interfaces'][1]['endpoints']:
            endpoint['parameters']['baud_hz']=None
        self.assert_blocked('unknown/invalid values',rebind=True)

    def test_startup_and_fault_behavior_required(self):
        self.doc['interfaces'][0]['fault_behavior']=None
        self.assert_blocked('fault_behavior',rebind=True)

    def test_mechanics_required_before_placement(self):
        self.doc['interfaces'][2]['geometry']['connector_positions']=None
        self.assertTrue(self.run_contract('schematic',rebind=True)['passed'])
        self.assert_blocked('mechanical list',stage='placement')

    def test_interface_gate_cannot_be_delayed_to_release(self):
        self.doc['interfaces'][2]['gate']='release'
        self.assert_blocked('gate is too late',stage='specification',rebind=True)

    def test_units_and_nonfinite_or_boolean_dimensions(self):
        original=copy.deepcopy(self.doc)
        self.doc['interfaces'][2]['geometry']['unit']='inch'
        self.assert_blocked('must use mm',rebind=True)
        self.doc=copy.deepcopy(original);self.doc['interfaces'][2]['geometry']['tolerance_mm']=True
        self.assert_blocked('mechanical value',rebind=True)
        self.doc=copy.deepcopy(original);self.doc['interfaces'][0]['endpoints'][0]['pins'][0]['voltage_max_v']=float('nan')
        self.assert_blocked()

    def test_requirement_change_invalidates_evidence_without_revision_bump(self):
        self.doc['requirements'][0]['acceptance']='A changed acceptance criterion'
        self.assert_blocked('different intent')

    def test_interface_revision_change_invalidates_evidence(self):
        self.doc['interfaces'][0]['revision']='2'
        self.assert_blocked('different intent')

    def test_changed_artifact_and_input_hashes(self):
        original=copy.deepcopy(self.doc)
        self.doc['evidence'][0]['sha256']='0'*64
        self.assert_blocked('artifact')
        self.doc=original
        (self.root/'calculation.txt').write_text('declared input')
        self.doc['evidence'][0]['inputs']=[{'path':'calculation.txt','sha256':'0'*64}]
        self.assert_blocked('input missing or modified')

    def test_review_cannot_claim_measurement_and_failed_evidence_blocks(self):
        self.doc['requirements'][0]['method']='measurement'
        report=self.assert_blocked('Required evidence kind',rebind=True)
        row=next(x for x in report['matrix'] if x['id']=='REQ-PRODUCT')
        self.assertEqual(row['observed_levels'],['reviewed'])
        self.doc['requirements'][0]['method']='review';self.doc['evidence'][0]['result']='fail'
        self.assert_blocked('result is fail',rebind=True)

    def test_technical_evidence_needs_actual_hashed_implementation_inputs(self):
        self.doc['requirements'][0]['method']='measurement'
        self.doc['evidence'][0]['kind']='measurement'
        self.assert_blocked('hashed verification inputs',rebind=True)
        self.doc['requirements'][0]['implementation'][0]['path']='measurement-input.txt'
        (self.root/'measurement-input.txt').write_text('synthetic input, not a physical measurement')
        self.doc['evidence'][0]['inputs']=[{'path':'measurement-input.txt',
            'sha256':rules.digest(self.root/'measurement-input.txt')}]
        # Other records still demand review, so use a separate synthetic review record.
        review=copy.deepcopy(self.doc['evidence'][0]);review.update(id='EV-SECOND',kind='review')
        self.doc['evidence'].append(review)
        for record in self.doc['requirements'][1:]+self.doc['interfaces']:
            record['evidence_ids']=['EV-SECOND']
        self.assertTrue(self.run_contract(rebind=True)['passed'])
        (self.root/'measurement-input.txt').write_text('changed implementation')
        self.assert_blocked('input missing or modified')

    def test_path_escape_work_report_and_symlink_refused(self):
        for artifact in ['../outside','.work/check.json']:
            self.doc['evidence'][0]['artifact']=artifact
            self.assert_blocked()

    def test_snapshot_and_configuration_preview_bind_contract_and_evidence(self):
        self.save()
        first=rules.configure(self.root,self.config)
        (self.root/'design-review.md').write_text('changed input')
        with self.assertRaisesRegex(ValueError,'stale'):
            rules.configure(self.root,self.config,apply_plan=first['id'])
        # Snapshot can include declaration and evidence without manual source-list duplication.
        for extension in ['.kicad_pro','.kicad_dru','.kicad_pcb','.kicad_sch']:
            (self.root/('board'+extension)).write_text('test-only')
        _,hashes=rules.snapshot(self.root,self.config)
        self.assertIn('requirements.json',hashes)
        self.assertIn('design-review.md',hashes)

    def test_pre_cad_cli_and_legacy_contract_refusal(self):
        self.save()
        result=subprocess.run([sys.executable,str(ROOT/'scripts/pcb_rules.py'),'requirements',str(self.root),
                               '--stage','placement'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(rules.read(self.root/'.work/requirements.json')['passed'])
        self.assertFalse((self.root/'board.kicad_pcb').exists())
        self.config['product'].pop('requirements_file');rules.write(self.root/'hardware.json',self.config)
        result=subprocess.run([sys.executable,str(ROOT/'scripts/pcb_rules.py'),'requirements',str(self.root)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertFalse(rules.read(self.root/'.work/requirements.json')['passed'])


if __name__=='__main__':unittest.main()

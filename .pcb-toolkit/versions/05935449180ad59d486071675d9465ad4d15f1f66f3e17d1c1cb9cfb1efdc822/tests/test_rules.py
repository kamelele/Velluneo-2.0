import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('pcb_rules', Path(__file__).resolve().parents[1]/'scripts/pcb_rules.py')
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


class ProfileTests(unittest.TestCase):
    def config(self, vendor='jlcpcb', assembly='supplier'):
        c = r.read(r.ROOT/'templates/project/hardware.json')
        c['fabrication']['vendor'] = vendor
        c['assembly']['mode'] = assembly
        c['name'] = 'demo'
        return c

    def test_four_combinations(self):
        for vendor in ['jlcpcb', 'eurocircuits']:
            for assembly in ['supplier', 'inhouse']:
                f, a, values = r.resolve(self.config(vendor, assembly))
                self.assertEqual(f['id'], vendor)
                self.assertEqual(a['id'], assembly)
                self.assertGreater(values['hole_size'], 0)

    def test_product_can_only_tighten(self):
        c = self.config()
        c['product']['minimums_mm'] = {'clearance': 3.2, 'track_width': .01}
        values = r.resolve(c)[2]
        self.assertEqual(values['clearance'], 3.2)
        self.assertGreaterEqual(values['track_width'], .2)
        for bad in [-1, float('nan'), '6mil', True]:
            c['product']['minimums_mm']['clearance'] = bad
            with self.assertRaises(ValueError):
                r.resolve(c)

    def test_netclass_cannot_weaken(self):
        values = r.resolve(self.config())[2]
        with self.assertRaises(ValueError):
            r.project_settings('demo', values, [{'name':'Power','nets':['VCC'],'track_width':.01}])

    def test_no_path_escape(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                r.safe_path(Path(d), '../secrets')

    def test_waiver_bound_to_exact_finding_and_snapshot(self):
        f = {'type':'clearance','severity':'error','items':[{'uuid':'a'}]}
        sig = r.hashlib.sha256(json.dumps(f, sort_keys=True).encode()).hexdigest()
        w = {'finding_sha256':sig,'snapshot':'current','rule_id':'DFM-001',
             'object_ids':['a'],'reason':'reviewed','approved_by':'test-human',
             'approval_evidence':'test-only'}
        self.assertTrue(r.waive(f, [w], 'current'))
        self.assertFalse(r.waive(f, [w], 'changed'))
        self.assertFalse(r.waive({**f,'type':'shorting_items'}, [w], 'current'))
        self.assertFalse(r.waive(f, [{**w,'approved_by':''}], 'current'))

    def test_decoder_keeps_excluded_findings(self):
        data={'sheets':[{'violations':[{'type':'pin_to_pin','severity':'exclusion'}]}]}
        self.assertEqual(len(r.violations(data)), 1)

    def test_pin_matrix_symmetry_and_output_conflict(self):
        matrix = r.read(r.ROOT/'templates/kicad/board.kicad_pro')['erc']['pin_map']
        self.assertEqual(len(matrix), 12)
        self.assertEqual(matrix[1][1], 2)
        self.assertEqual(matrix, list(map(list, zip(*matrix))))


if __name__=='__main__':
    unittest.main()

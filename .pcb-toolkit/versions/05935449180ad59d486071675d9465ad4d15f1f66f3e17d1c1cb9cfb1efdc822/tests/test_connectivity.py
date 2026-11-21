"""Physical-pin graph comparisons and fail-closed exporter handling."""
import copy
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import connectivity as c
import pcb_rules as rules
import connectivity_fixture as fixture


def document():
    result={'schema_version':1,'revision':'1','basis':'Independent fictional pin specification',
        'basis_sources':[{'path':'basis.md','sha256':'0'*64}],
        'components':[{'ref':'U1','units':[{'name':'A','pins':['1','2']},{'name':'B','pins':['3','4']}]},
                      {'ref':'J1','units':[{'name':'A','pins':['1','2','3','4']}]}],
        'nets':[{'id':'N'+str(i),'pins':[{'ref':'U1','pin':str(i)},{'ref':'J1','pin':str(i)}]} for i in [1,2,3]],
        'no_connects':[{'ref':ref,'pin':'4','reason':'Explicitly unused in fictional product'} for ref in ['U1','J1']],
        'barriers':[{'id':'SEP','side_a':['N1'],'side_b':['N2'],'basis':'Separate electrical nets, not insulation qualification'}]}
    return fixture.approve(result)


def export_xml(intent,groups=None,nc=None,source='board.kicad_sch',version='10.0.6'):
    model=c.validate_intent(intent)
    root=ET.Element('export',version='E');design=ET.SubElement(root,'design')
    ET.SubElement(design,'tool').text='Eeschema '+version
    ET.SubElement(design,'source').text=source
    components=ET.SubElement(root,'components');parts=ET.SubElement(root,'libparts')
    for ref,units in model['components'].items():
        comp=ET.SubElement(components,'comp',ref=ref);ET.SubElement(comp,'libsource',lib='Fixture',part=ref)
        ET.SubElement(comp,'tstamps').text=' '.join('instance-'+ref+'-'+name for name in units)
        part=ET.SubElement(parts,'libpart',lib='Fixture',part=ref);physical=ET.SubElement(part,'pins')
        for p in sorted(set().union(*units.values())):ET.SubElement(physical,'pin',num=p,type='passive')
        holder=ET.SubElement(comp,'units')
        for name,pins in units.items():
            unit=ET.SubElement(holder,'unit',name=name);pinholder=ET.SubElement(unit,'pins')
            for p in sorted(pins):ET.SubElement(pinholder,'pin',num=p)
    nets=ET.SubElement(root,'nets')
    if groups is None:groups=[set(x) for x in model['groups'].values()]+[{p} for p in model['nc']]
    if nc is None:nc=model['nc']
    for i,members in enumerate(groups):
        net=ET.SubElement(nets,'net',code=str(i+1),name='arbitrary-export-name-'+str(i))
        for ref,p in sorted(members):ET.SubElement(net,'node',ref=ref,pin=p,pintype='passive+no_connect' if (ref,p) in nc else 'passive')
    return ET.tostring(root,encoding='utf-8')


class ConnectivityTests(unittest.TestCase):
    def setUp(self):self.doc=document()
    def compare(self,data=None):return c.compare(self.doc,c.parse_export(data or export_xml(self.doc)))
    def errors(self,report):return {x['type'] for x in report['errors']}

    def test_correct_graph_multiunit_and_nc(self):
        report=self.compare();self.assertTrue(report['passed'],report['errors']);self.assertEqual(report['physical_pins'],8)

    def test_names_and_codes_are_not_connectivity_identity(self):
        root=ET.fromstring(export_xml(self.doc))
        for i,net in enumerate(root.findall('nets/net')):net.set('name','same diagnostic label');net.set('code',str(100-i))
        self.assertTrue(self.compare(ET.tostring(root))['passed'])

    def test_merge_and_barrier_breach(self):
        m=c.validate_intent(self.doc);groups=list(m['groups'].values())
        groups=[groups[0]|groups[1],groups[2]]+[{p} for p in m['nc']]
        kinds=self.errors(self.compare(export_xml(self.doc,groups)))
        self.assertTrue({'merged_nets','barrier_breached'}<=kinds)

    def test_split_net(self):
        m=c.validate_intent(self.doc);groups=list(m['groups'].values());split=[{p} for p in groups[0]]
        groups=split+groups[1:]+[{p} for p in m['nc']]
        self.assertIn('split_net',self.errors(self.compare(export_xml(self.doc,groups))))

    def test_wrong_physical_pin_membership(self):
        m=c.validate_intent(self.doc);groups=[set(pins) for pins in m['groups'].values()]
        groups[0].remove(('U1','1'));groups[0].add(('U1','2'))
        groups[1].remove(('U1','2'));groups[1].add(('U1','1'))
        groups += [{p} for p in m['nc']]
        self.assertTrue({'merged_nets','split_net'}<=self.errors(self.compare(export_xml(self.doc,groups))))

    def test_missing_and_connected_nc(self):
        nc=c.validate_intent(self.doc)['nc'];actual_nc=nc-{('U1','4')}
        self.assertIn('missing_nc_marker',self.errors(self.compare(export_xml(self.doc,nc=actual_nc))))
        m=c.validate_intent(self.doc);groups=list(m['groups'].values())+[nc]
        self.assertIn('connected_nc',self.errors(self.compare(export_xml(self.doc,groups))))

    def test_unexpected_nc_on_intended_net(self):
        nc=c.validate_intent(self.doc)['nc']|{('U1','1')}
        self.assertIn('unexpected_nc',self.errors(self.compare(export_xml(self.doc,nc=nc))))

    def test_omitted_placed_unit_detected_from_library_inventory(self):
        root=ET.fromstring(export_xml(self.doc));holder=root.find('components/comp/units')
        holder.remove(holder.findall('unit')[1])
        kinds=self.errors(self.compare(ET.tostring(root)))
        self.assertTrue({'unit_pin_mismatch','unplaced_unit_pins'}<=kinds)

    def test_library_unit_listing_does_not_prove_all_units_placed(self):
        root=ET.fromstring(export_xml(self.doc))
        root.find('components/comp/tstamps').text='one-instance-only'
        self.assertIn('unit_instance_count_mismatch',self.errors(self.compare(ET.tostring(root))))

    def test_duplicate_json_and_nonrelease_export_tool_rejected(self):
        with self.assertRaises(ValueError):c.loads('{"revision":"1","revision":"2"}')
        with self.assertRaises(ValueError):c.parse_export(export_xml(self.doc).replace(b'Eeschema 10.0.6',b'Eeschema 10.0.6-nightly'))

    def test_exact_ubuntu_packaging_identity_only(self):
        report=c.compare(self.doc,c.parse_export(export_xml(self.doc,version='10.0.6+dfsg-1')))
        self.assertTrue(report['passed'],report['errors'])
        for version in ['10.0.6+dfsg-2','10.0.6+dfsg-1-nightly','10.0.7+dfsg-1']:
            with self.assertRaises(ValueError):c.parse_export(export_xml(self.doc,version=version))

    def test_duplicate_unknown_or_uncovered_intent_pins_rejected(self):
        for mutate in [lambda d:d['nets'][0]['pins'].append({'ref':'U1','pin':'1'}),
                       lambda d:d['nets'][0]['pins'].__setitem__(0,{'ref':'U1','pin':'99'}),
                       lambda d:d['no_connects'].pop()]:
            d=copy.deepcopy(self.doc);mutate(d)
            with self.assertRaises(ValueError):c.validate_intent(d)

    def test_singletons_and_pinless_components_need_rationale(self):
        d=copy.deepcopy(self.doc);d['nets'][0]['pins'].pop()
        with self.assertRaises(ValueError):c.validate_intent(d)
        d=document();d['components'].append({'ref':'H1','units':[]})
        with self.assertRaises(ValueError):c.validate_intent(d)

    def test_stale_or_missing_approval_is_not_waived(self):
        self.doc['basis']='Changed independently reviewed basis'
        self.assertIn('missing_stale_intent_approval',self.errors(self.compare()))
        self.doc.pop('approval')
        self.assertIn('missing_stale_intent_approval',self.errors(self.compare()))

    def test_bad_barrier_and_duplicate_component_rejected(self):
        d=document();d['barriers'][0]['side_b']=['MISSING']
        with self.assertRaises(ValueError):c.validate_intent(d)
        d=document();d['components'].append(copy.deepcopy(d['components'][0]))
        with self.assertRaises(ValueError):c.validate_intent(d)

    def test_xml_schema_version_missing_inventory_and_injected_entity_fail(self):
        raw=export_xml(self.doc)
        for data in [raw.replace(b'version="E"',b'version="F"'),raw.replace(b'10.0.6',b'10.0.7'),
                     b'<!DOCTYPE export>'+raw,raw.replace(b'<units>',b'<unsupported>').replace(b'</units>',b'</unsupported>')]:
            with self.assertRaises(ValueError):c.parse_export(data)

    def test_physical_pin_in_multiple_actual_nets_rejected(self):
        groups=list(c.validate_intent(self.doc)['groups'].values())
        groups.append({('U1','1')})
        with self.assertRaises(ValueError):c.parse_export(export_xml(self.doc,groups))

    def test_intent_and_basis_invalidate_snapshot_and_configuration_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'basis.md').write_text('Independent pin table')
            self.doc['basis_sources'][0]['sha256']=configuration_sha(root/'basis.md');fixture.approve(self.doc)
            rules.write(root/'intent.json',self.doc)
            config=rules.read(ROOT/'templates/project/hardware.json')
            config.update(name='board',source_files=['board'+ext for ext in ['.kicad_pro','.kicad_dru','.kicad_pcb','.kicad_sch']])
            config['product'].pop('requirements_file',None)
            config['fabrication']['vendor']='jlcpcb';config['assembly']['mode']='supplier'
            config['product']['connectivity_file']='intent.json'
            for name in config['source_files']:(root/name).write_text('{}' if name.endswith('.kicad_pro') else 'synthetic')
            before,records=rules.snapshot(root,config)
            self.assertIn('intent.json',records);self.assertIn('basis.md',records)
            plan=rules.configuration_plan(root,config)
            self.doc['approval']['evidence']='Changed recorded decision'
            rules.write(root/'intent.json',self.doc)
            self.assertNotEqual(before,rules.snapshot(root,config)[0])
            self.assertNotEqual(plan['id'],rules.configuration_plan(root,config)['id'])
            intent_snapshot=rules.snapshot(root,config)[0]
            (root/'basis.md').write_text('Independent pin table revised')
            self.assertNotEqual(intent_snapshot,rules.snapshot(root,config)[0])

    def test_export_failure_does_not_consume_cached_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'basis.md').write_text('Independent pin table')
            self.doc['basis_sources'][0]['sha256']=configuration_sha(root/'basis.md');fixture.approve(self.doc)
            (root/'intent.json').write_text(json.dumps(self.doc));(root/'board.kicad_sch').write_text('synthetic')
            output=root/'.work/connectivity-netlist.xml';output.parent.mkdir();output.write_bytes(export_xml(self.doc))
            config={'name':'board','kicad_version':'10.0.6','product':{'connectivity_file':'intent.json'}}
            report=c.verify(root,config,'missing',lambda *args:{'exit_code':1,'stdout':'','stderr':'failed'})
            self.assertFalse(report['passed']);self.assertTrue(report['configuration_error']);self.assertFalse(output.exists())

    def test_source_change_and_basis_mismatch_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);basis=root/'basis.md';basis.write_text('Independent pin table')
            self.doc['basis_sources'][0]['sha256']=configuration_sha(basis);fixture.approve(self.doc)
            (root/'intent.json').write_text(json.dumps(self.doc));(root/'board.kicad_sch').write_text('synthetic')
            config={'name':'board','kicad_version':'10.0.6','product':{'connectivity_file':'intent.json'}}
            def run(*args):
                (root/'.work/connectivity-netlist.xml').write_bytes(export_xml(self.doc,source=str(root/'board.kicad_sch')))
                basis.write_text('changed during export')
                return {'exit_code':0,'stdout':'','stderr':''}
            report=c.verify(root,config,'synthetic-runner',run)
            self.assertFalse(report['passed']);self.assertTrue(any('Input changed' in x['message'] for x in report['errors']))
            report=c.verify(root,config,'unused',run)
            self.assertTrue(any('basis changed' in x['message'] for x in report['errors']))


def configuration_sha(path):return c.configuration.sha(path.read_bytes())


if __name__=='__main__':unittest.main()

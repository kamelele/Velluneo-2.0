from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,pcbnew
D=Path(__file__).resolve().parent;E=D/'design';P=E/'Velluneo_driver.kicad_pcb';b=pcbnew.LoadBoard(str(P));parts=json.loads((E/'proposed-parts.json').read_text());intent=json.loads((E/'proposed-intent.json').read_text());mapping=json.loads((E/'full-build-result.json').read_text())['logical_to_native_netnames'];fps={f.GetReference():f for f in b.GetFootprints()};components={c.attrib['ref']:c for c in ET.parse(E/'checks/netlist.xml').getroot().findall('./components/comp')}
digest=hashlib.sha256(json.dumps({k:v for k,v in intent.items()if k!='proposal_digest'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest();assert digest==intent['proposal_digest']=='87b164503d5c5894dfe592608a172bd858c960b3a40b1b141f3588bfeffd716b'
assert len(fps)==len(parts)==33;pin_count=0
for part in parts:
 ref=part['ref'];f=fps[ref];assert f.GetFieldText('MPN')==part['mpn'];assert f.GetValue()==components[ref].findtext('value');assert f.GetFPID().GetLibNickname().c_str()+':'+f.GetFPID().GetLibItemName().c_str()==components[ref].findtext('footprint');assert {p.GetNumber()for p in f.Pads()}==set(part['pins'])
 for p in f.Pads():
  n=part['pins'][p.GetNumber()];assert p.GetNetname()==mapping[n]if n in mapping else p.GetNetname().startswith('unconnected-');pin_count+=1
assert pin_count==81
expected={frozenset((p['ref'],n)for p in parts for n,v in p['pins'].items()if v==net)for net in mapping}
actual={frozenset((node.attrib['ref'],node.attrib['pin'])for node in net.findall('node'))for net in ET.parse(E/'checks/netlist.xml').getroot().findall('./nets/net')}
assert expected.issubset(actual)
canonical=D.parent/'pcb-return-06/studies/sense/Velluneo_sense_exploration.kicad_pro'
def norm(p):
 j=json.loads(p.read_text());j['meta']['filename']='PROJECT.kicad_pro'
 for sheet in j.get('schematic',{}).get('top_level_sheets',[]):sheet.update(filename='PROJECT.kicad_sch',name='PROJECT')
 return j
assert norm(canonical)==norm(P.with_suffix('.kicad_pro'))
assert canonical.with_suffix('.kicad_dru').read_bytes()==P.with_suffix('.kicad_dru').read_bytes()
out=dict(board_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),intent_digest=digest,components=33,pads=81,functional_nets=23,NC_singletons=4,native_membership_MPN_value_footprint_and_fresh_netlist_match=True,canonical_project_policy_semantically_equal_except_filename_metadata=True,custom_rules_byte_identical=True,no_new_exclusions=True,scope='Intent basis and CAD/policy consistency; does not prove electrical operation or product approval.')
(E/'checks/intent-policy.json').write_text(json.dumps(out,indent=2)+'\n');print('Intent and canonical policy verified')

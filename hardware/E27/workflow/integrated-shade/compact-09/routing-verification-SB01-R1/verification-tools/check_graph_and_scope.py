from pathlib import Path
import argparse,json,hashlib,xml.etree.ElementTree as ET
import pcbnew as k
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--netlist',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();s=a.source;base=a.baseline
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
intent=json.loads((s/'intended-connectivity.SB01.json').read_text());expected={(n['ref'],n['pin']):net['id'].lstrip('/')for net in intent['nets']for n in net['pins']}
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(s/'SC09_compact.kicad_pcb'));native={(f.GetReference(),p.GetNumber()):p.GetNetname().lstrip('/')for f in b.GetFootprints()for p in f.Pads()};xml={(n.get('ref'),n.get('pin')):net.get('name').lstrip('/')for net in ET.parse(a.netlist).findall('./nets/net')for n in net.findall('node')}
diff=[]
for label,actual in [('native',native),('fresh_XML',xml)]:
 for key in sorted(set(expected)|set(actual)):
  if expected.get(key)!=actual.get(key):diff.append({'source':label,'pin':key,'expected':expected.get(key),'actual':actual.get(key)})
identity={}
for name in ['SC09_compact.kicad_pcb','SC09_compact.kicad_sch']:
 old=(base/name).read_text();new=(s/name).read_text();needle='(property "MPN" "LYT1603D-TL"';replacement='(property "MPN" "LYT1603D"'
 identity[name]={'baseline_sha256':sha(base/name),'candidate_sha256':sha(s/name),'exactly_one_metadata_replacement_and_no_other_normalized_text_change':old.count(needle)==1 and old.replace(needle,replacement,1)==new}
manifest=json.loads((s.parent/'baseline-manifest.json').read_text())['files'];other=[n for n,h in manifest.items()if n not in identity and sha(s/n)!=h]
r={'actor':'/root','intent_sha256':sha(s/'intended-connectivity.SB01.json'),'netlist_sha256':sha(a.netlist),'board_sha256':sha(s/'SC09_compact.kicad_pcb'),'expected_pin_memberships':len(expected),'native_physical_contacts':sum(len(list(f.Pads()))for f in b.GetFootprints()),'native_refs':len(list(b.GetFootprints())),'graph_differences':diff,'metadata_only_source_identity':identity,'other_baseline_files_changed':other,'passed':not diff and not other and all(v['exactly_one_metadata_replacement_and_no_other_normalized_text_change']for v in identity.values()),'limits':'Exact independent pin membership and authorized textual scope, not measurements or safety qualification.'};a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'pins':len(expected),'differences':diff,'other_changes':other}));raise SystemExit(0 if r['passed']else 1)

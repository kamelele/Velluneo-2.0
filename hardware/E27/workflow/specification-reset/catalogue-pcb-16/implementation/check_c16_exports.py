from pathlib import Path
import json,subprocess,xml.etree.ElementTree as ET
W=Path(__file__).resolve().parent;P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'catalogue-pcb-16';E=D/'design';C=D/'checks';K=W/'kicad-10.0.6/bin/kicad-cli.exe';C.mkdir(exist_ok=True)
jobs=[('netlist',['sch','export','netlist','--format','kicadxml','--output',C/'C16-netlist.xml',E/'Velluneo_driver.kicad_sch']),('erc',['sch','erc','--format','json','--severity-all','--exit-code-violations','--output',C/'erc.json',E/'Velluneo_driver.kicad_sch']),('drc',['pcb','drc','--schematic-parity','--format','json','--severity-all','--exit-code-violations','--output',C/'drc.json',E/'Velluneo_driver.kicad_pcb']),('schematic-pdf',['sch','export','pdf','--output',D/'Velluneo_C16_schematic.pdf',E/'Velluneo_driver.kicad_sch'])]
commands=[]
for name,args in jobs:
 cmd=[str(K),*map(str,args)];r=subprocess.run(cmd,capture_output=True,timeout=180)
 (C/(name+'.stdout.log')).write_bytes(r.stdout);(C/(name+'.stderr.log')).write_bytes(r.stderr);commands.append(dict(name=name,command=cmd,exit_code=r.returncode))
 if name in('drc','erc'):
  j=json.loads((C/(name+'.json')).read_text());print(name,r.returncode,{k:len(v)for k,v in j.items()if isinstance(v,list)},flush=True)
 else:print(name,r.returncode,flush=True)
(C/'native-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
parts=json.loads((E/'proposed-parts.json').read_text());expected={};NC=set()
for a in parts:
 for pin,net in a['pins'].items():
  if net is None:NC.add((a['ref'],pin))
  else:expected.setdefault(net,set()).add((a['ref'],pin))
root=ET.parse(C/'C16-netlist.xml').getroot();actual={};physical={a['ref']for a in parts}
for n in root.findall('./nets/net'):
 members={(q.attrib['ref'],q.attrib['pin'])for q in n.findall('node')if q.attrib['ref']in physical}
 if members:actual[n.attrib['name']]=members
exp={frozenset(x)for x in expected.values()};act={frozenset(x)for x in actual.values()if not x<=NC}
missing=[sorted(x)for x in exp-act];extra=[sorted(x)for x in act-exp]
report=dict(expected_components=len(parts),actual_components=len([x for x in root.findall('./components/comp')if x.attrib['ref']in physical]),expected_unique_physical_pins=sum(len(a['pins'])for a in parts),expected_connected_nets=len(exp),NC=sorted(NC),missing_groups=missing,extra_groups=extra,passed=not missing and not extra,scope='Independent pre-capture pin intent compared with fresh native netlist; no functional qualification inferred.')
(C/'intent-comparison.json').write_text(json.dumps(report,indent=2)+'\n');print('intent',report['passed'],missing,extra)

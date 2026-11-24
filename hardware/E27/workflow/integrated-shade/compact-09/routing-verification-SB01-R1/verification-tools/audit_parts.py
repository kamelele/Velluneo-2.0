"""Independent actual fields check, separate from native SCH/PCB parity."""
from pathlib import Path
import argparse,hashlib,json,xml.etree.ElementTree as ET
import pcbnew as k
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--netlist',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();s=a.source
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[s/'SC09_compact.kicad_pcb',s/'bom-build.json',a.netlist];before={str(p):sha(p)for p in paths}
b=k.LoadBoard(str(paths[0]));expected={c['ref']:c for c in json.loads(paths[1].read_text())['components']};xml={c.get('ref'):c for c in ET.parse(a.netlist).findall('./components/comp')};native={f.GetReference():f for f in b.GetFootprints()};findings=[];rows=[]
if set(expected)!=set(native)or set(expected)!=set(xml):findings.append({'type':'reference-set-mismatch'})
for ref,c in expected.items():
 if ref not in native or ref not in xml:continue
 f=native[ref];x=xml[ref];field=f.GetField('MPN');mpn=field.GetText()if field else None;sm=x.find("./fields/field[@name='MPN']");smpn=sm.text if sm is not None else None;value=x.findtext('value');electronic=ref not in ['J1','J2']
 row={'ref':ref,'expected_MPN':c['mpn'],'actual_PCB_MPN':mpn,'actual_schematic_MPN':smpn,'PCB_Value':f.GetValue(),'schematic_Value':value,'electronic':electronic,'DNP_PCB':bool(f.GetAttributes()&k.FP_DNP),'DNP_schematic':x.find("./property[@name='dnp']")is not None}
 row['passed']=(not electronic or c['mpn']==mpn==smpn)and f.GetValue()==value and not row['DNP_PCB']and not row['DNP_schematic'];rows.append(row)
 if not row['passed']:findings.append(row)
r={'scope':'Actual MPN property vs canonical selected BOM; human-readable Value parity and populated flag; wire ports have no purchased MPN requirement. No thermal/electrical/land qualification inferred.','inputs':before,'source_unchanged':all(sha(Path(n))==h for n,h in before.items()),'rows':rows,'findings':findings,'passed':not findings};a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'findings':findings}));raise SystemExit(0 if r['passed']else 1)

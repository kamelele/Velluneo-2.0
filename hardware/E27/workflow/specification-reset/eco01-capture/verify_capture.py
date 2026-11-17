#!/usr/bin/env python3
"""Independent contract versus native XML part/footprint/annotation comparison.
Expected parts are pre-CAD approved data, never inferred from native XML.
"""
from pathlib import Path
import argparse,json,hashlib,csv,re,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent.parent;D=P/'eco01-capture'
a=argparse.ArgumentParser();a.add_argument('--netlist',type=Path,default=P/'.work/connectivity-netlist.xml');a.add_argument('--output',type=Path,default=D/'capture-contract-check.json');a.add_argument('--bom',type=Path,default=D/'BOM.csv');args=a.parse_args()
parts=json.loads((P/'electrical-integration/proposed-parts.json').read_text());expected={p['ref']:p for p in parts};assign=json.loads((P/'footprint-study/assignments.json').read_text());root=ET.parse(args.netlist).getroot();actual={c.attrib['ref']:c for c in root.findall('components/comp')};assert set(actual)==set(expected)==set(assign) and len(actual)==31
rows=[]
for ref,p in expected.items():
 c=actual[ref];fields={v.attrib['name']:v.text for v in c.findall('fields/field')};assert fields['MPN']==p['mpn']==assign[ref]['mpn'];assert c.findtext('footprint')==assign[ref]['footprint'];assert {n.attrib['num'] for n in c.findall('units/unit/pins/pin')}==set(p['pins']);assert re.fullmatch('[A-Z]+[1-9][0-9]*',ref),ref
 rows.append({'ref':ref,'mpn':fields['MPN'],'footprint':c.findtext('footprint'),'physical_pins':sorted(p['pins'])})
with args.bom.open(newline='') as f:bom={r['Reference']:r for r in csv.DictReader(f)}
assert set(bom)==set(expected)
for ref,p in expected.items():assert bom[ref]['MPN_or_custom_requirement']==p['mpn'] and bom[ref]['Footprint']==assign[ref]['footprint'] and bom[ref]['Value']==actual[ref].findtext('value')
for ref in ['R2','R3','R14','R15']:assert assign[ref]['footprint']=='Velluneo_Driver:CRCW_2512_NativeReflow'
assert assign['R13']['footprint']=='Velluneo_Driver:CRCW_0603_NativeReflow'
g=json.loads((P/'schematic-intent/intended-connectivity.json').read_text());canonical=json.dumps({k:v for k,v in g.items() if k!='approval'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode();digest=hashlib.sha256(canonical).hexdigest();assert g['approval']['intent_digest']==digest=='5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8'
for b in g['basis_sources']:assert hashlib.sha256((P/b['path']).read_bytes()).hexdigest()==b['sha256']
result={'passed':True,'scope':'pre-CAD approved part/footprint/physical-inventory versus nativeXML and BOM; not function, physical assembly or fullstage acceptance','components':len(actual),'physical_terminals':sum(len(p['pins']) for p in expected.values()),'active_intent_digest':digest,'netlist_sha256':hashlib.sha256(args.netlist.read_bytes()).hexdigest(),'all_regular_references_numeric_suffix':True,'basis_hashes_verified':True,'parts':rows}
args.output.write_text(json.dumps(result,indent=2)+'\n');print('Capture contract pass:',len(actual),'parts,79terminals')

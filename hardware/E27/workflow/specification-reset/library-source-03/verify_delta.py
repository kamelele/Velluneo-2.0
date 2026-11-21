#!/usr/bin/env python3
"""Allowlisted source delta versus immutable parent, independently of generated CAD."""
from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent.parent;D=P/'library-source-03';R=P.parents[3]
BASE='ee9a89a873ff1b9f1546ddf95f0c4764e4823e7c';prefix=P.relative_to(R).as_posix()+'/'
def old(path):return subprocess.check_output(['git','show',BASE+':'+prefix+path],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
unchanged=['schematic-intent/intended-connectivity.json','electrical-integration/proposed-parts.json','requirements.json','Velluneo_specification_reset.kicad_pro','libraries/Velluneo_Driver.kicad_sym','sym-lib-table','fp-lib-table']
unchanged += [(f.relative_to(P)).as_posix() for f in (P/'libraries/Velluneo_Driver.pretty').glob('*.kicad_mod') if f.name!='KEMET_2220_C0G_DensityB_Native.kicad_mod']
for path in unchanged:assert old(path)==(P/path).read_bytes(),path
before=json.loads(old('footprint-study/assignments.json'));after=json.loads((P/'footprint-study/assignments.json').read_text());assert set(before)==set(after)
changed={ref for ref in before if before[ref]!=after[ref]};assert changed=={'C2','C3','F1'},changed
for ref in before:
 assert before[ref]['mpn']==after[ref]['mpn']
 if ref=='F1':assert before[ref]['footprint']==after[ref]['footprint']
expected=old('Velluneo_specification_reset.kicad_sch').decode('utf-8')
for ref in ['C2','C3','F1']:
 for key in ['footprint','status']:
  b=before[ref][key];v=after[ref][key]
  if b!=v:
   # Shared C2/C3 substitutions are applied once with exact count2.
   count=expected.count(json.dumps(b,ensure_ascii=False))
   if count:
    assert count==(2 if ref in ['C2','C3'] else 1),(ref,key,count)
    expected=expected.replace(json.dumps(b,ensure_ascii=False),json.dumps(v,ensure_ascii=False))
assert expected==(P/'Velluneo_specification_reset.kicad_sch').read_text(encoding='utf-8'), 'Schematic delta exceeded exact allowlist'
out={'passed':True,'base':BASE,'unchanged_bytes':{p:sha((P/p).read_bytes()) for p in unchanged},'assignment_changes':sorted(changed),'schematic_delta':'C2/C3 footprint and Library_Status; F1 Library_Status only; all other schematic bytes preserved','graph_values_types_rules_unchanged':True}
(D/'source-delta-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('Source delta allowlist pass')

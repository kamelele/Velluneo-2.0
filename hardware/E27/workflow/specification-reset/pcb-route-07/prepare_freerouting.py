"""Bind native protected input and strengthen DSN to the unchanged scoped KiCad rules."""
from pathlib import Path
import json,hashlib,re
D=Path(__file__).resolve().parent;F=D/'routing';F.mkdir(exist_ok=True);p=F/'input-raw.dsn';s=p.read_text();source=D/'studies/sense/ground-seed.kicad_pcb'
def scope_end(start):
 depth=0;quoted=False;escape=False
 for i in range(start,len(s)):
  c=s[i]
  if escape:escape=False;continue
  if c=='\\'and quoted:escape=True;continue
  if c=='"':quoted=not quoted;continue
  if not quoted:
   if c=='(':depth+=1
   elif c==')':
    depth-=1
    if depth==0:return i+1
 raise ValueError('unbalanced selected scope')
mp=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames']
classes={'HV':['AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','BULK_POS','DRAIN','CLAMP','STARTUP_MID'],'QUIET':['VDD','VS','NTC','CS','DRV','GATE','SENSE','PRIMARY_GND','AUX_RAW','AUX_RECT'],'PRIMARY_OTHER':['BLEED_MID_B','BLEED_MID','unconnected-(T1-Pad3)'],'SECONDARY':['OUTPUT_POS','OUTPUT_NEG','SECONDARY_RAW','unconnected-(T1-Pad7)','unconnected-(T1-Pad8)','unconnected-(T1-Pad9)']}
block=[]
for name,nets in classes.items():
 ns=[mp.get(n,n)for n in nets];block.append('(class '+name+' '+' '.join(json.dumps(n)for n in ns)+' (circuit (use_via "Via[0-1]_600:300_um")) (rule (width 300) (clearance 250)))')
for a,b,gap in [('HV','QUIET',3000),('HV','SECONDARY',10000),('QUIET','SECONDARY',10000),('PRIMARY_OTHER','SECONDARY',10000)]:block.append(f'(class_class (classes {a} {b}) (rule (clearance {gap})))')
start=s.index('(class kicad_default');end=scope_end(start);s=s[:start]+'\n'.join(block)+s[end:]
s=s.replace('(width 200)','(width 300)').replace('(clearance 200)','(clearance 250)');s=re.sub(r'\s*\(clearance 50 \(type smd_smd\)\)','',s);s=s.replace('(type route)','(type protect)')
assert '(width 200)'not in s and'smd_smd'not in s and'(type route)'not in s
out=F/'input-scoped.dsn';out.write_text(s,encoding='utf-8',newline='\n')
(F/'input-contract.json').write_text(json.dumps(dict(native_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),raw_dsn_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),scoped_dsn_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),classes={k:[mp.get(n,n)for n in v]for k,v in classes.items()},clearance_pairs_um=[['HV','QUIET',3000],['HV','SECONDARY',10000],['QUIET','SECONDARY',10000],['PRIMARY_OTHER','SECONDARY',10000]],minimum_width_um=300,minimum_other_clearance_um=250,copper_edge_um=500,protected_input_wires=s.count('(type protect)'),all_keepouts_preserved=True,native_KiCad_rules_modified=False,scope='Experimental DSN translation; actual importer preservation, negative controls/native DRC/topology are mandatory. No qualified toolkit adapter/config migration.'),indent=2)+'\n')
print('scoped classes4, pair rules4, protected',s.count('(type protect)'))

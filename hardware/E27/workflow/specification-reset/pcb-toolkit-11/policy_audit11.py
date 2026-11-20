"""Independent bounded parser/evaluator for the legacy and generated clearance policy."""
from pathlib import Path
import re,json,hashlib,sys,itertools
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-toolkit-11';E=D/'design';OLD=P/'pcb-cleanup-10/design';mode=sys.argv[1]if len(sys.argv)>1 else'baseline'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sexprs(raw):
 raw='\n'.join(line for line in raw.splitlines()if not line.lstrip().startswith('#'));tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',raw);i=0
 def read():
  nonlocal i
  token=tokens[i];i+=1
  if token=='(':
   value=[]
   while tokens[i]!=')':value.append(read())
   i+=1;return value
  if token.startswith('"'):return json.loads(token)
  return token
 out=[]
 while i<len(tokens):out.append(read())
 return out
def condition(text):
 pattern=re.compile(r"\s*(A\.NetName|B\.NetName|==|&&|\|\||\(|\)|'[^'\\]*')");ts=[];at=0
 while at<len(text):
  m=pattern.match(text,at)
  if not m:raise ValueError('Unsupported condition grammar at '+text[at:])
  ts.append(m.group(1));at=m.end()
 i=0
 def atom():
  nonlocal i
  if ts[i]=='(':
   i+=1;node=expr();assert ts[i]==')';i+=1;return node
  field=ts[i];assert field in('A.NetName','B.NetName')and ts[i+1]=='=='and ts[i+2].startswith("'");value=ts[i+2][1:-1];i+=3;return('eq',field[0],value)
 def conjunction():
  nonlocal i
  node=atom()
  while i<len(ts)and ts[i]=='&&':i+=1;node=('and',node,atom())
  return node
 def expr():
  nonlocal i
  node=conjunction()
  while i<len(ts)and ts[i]=='||':i+=1;node=('or',node,conjunction())
  return node
 node=expr();assert i==len(ts);return node
def evaluate(ast,a,b):
 if ast is None:return True
 if ast[0]=='eq':return(a if ast[1]=='A'else b)==ast[2]
 x,y=evaluate(ast[1],a,b),evaluate(ast[2],a,b);return x and y if ast[0]=='and'else x or y
def names(ast,field=None):
 if ast[0]=='eq':return{ast[2]}if field is None or ast[1]==field else set()
 return names(ast[1],field)|names(ast[2],field)
def rules(path):
 out=[]
 for row in sexprs(path.read_text()):
  if row[0]!='rule':continue
  cs=[x for x in row[2:]if isinstance(x,list)and x[0]=='constraint'and x[1]=='clearance']
  if not cs:continue
  assert all(x[0]in('condition','constraint')for x in row[2:]),'Unexpected rule qualifier'
  cond=next((x[1]for x in row[2:]if x[0]=='condition'),None);ast=condition(cond)if cond else None;minimum=next(x for x in cs[0][2:]if x[0]=='min');v=''.join(minimum[1:]);m=re.fullmatch(r'([0-9.]+)mm',v);assert m,v;out.append(dict(id=row[1],min_mm=float(m.group(1)),ast=ast))
 return out
legacy=rules(OLD/'Velluneo_driver.kicad_dru');netnames=sorted(set().union(*(names(r['ast'])for r in legacy)));assert len(netnames)==27
if mode=='baseline':
 pairs=[]
 for r in legacy:
  assert r['ast'][0]=='or'and r['ast'][1][0]=='and';left=r['ast'][1];pairs.append(dict(id=r['id'],side_a=sorted(names(left,'A')),side_b=sorted(names(left,'B')),min_mm=r['min_mm'],legacy_ast=r['ast']))
 result=dict(schema_version=1,source_dru_sha256=sha(OLD/'Velluneo_driver.kicad_dru'),source_project_sha256=sha(OLD/'Velluneo_driver.kicad_pro'),declared_nets=netnames,global_minimums_mm=json.loads((OLD/'hardware.json').read_text())['product']['minimums_mm'],scoped_pairs=pairs,basis='Existing explicit project-scoped numeric rules and strict current source, not inferred from the schematic under test. Preservation audit only, not normative insulation qualification.');(D/'isolation-policy-baseline.json').write_text(json.dumps(result,indent=2)+'\n');print('Baseline27nets',[(len(p['side_a']),len(p['side_b']),p['min_mm'])for p in pairs])
else:
 new=rules(E/'Velluneo_driver.kicad_dru');oldpro=json.loads((OLD/'Velluneo_driver.kicad_pro').read_text());newpro=json.loads((E/'Velluneo_driver.kicad_pro').read_text());base=oldpro['board']['design_settings']['rules']['min_clearance'];differences=[];cases=[]
 def effective(rs,a,b):
  value=base
  for r in rs:
   if evaluate(r['ast'],a,b):value=max(base,r['min_mm'])
  return value
 allnets=netnames+['','__UNKNOWN_NET_NOT_DECLARED__']
 for a,b in itertools.product(allnets,repeat=2):
  before,after=effective(legacy,a,b),effective(new,a,b);cases.append(dict(a=a,b=b,before_mm=before,after_mm=after))
  if before!=after:differences.append(cases[-1])
 assert not differences,differences[:5]
 fields={'clearance':'min_clearance','track_width':'min_track_width','hole_size':'min_through_hole_diameter','annular_width':'min_via_annular_width','edge_clearance':'min_copper_edge_clearance'}
 for key,field in fields.items():assert newpro['board']['design_settings']['rules'][field]>=oldpro['board']['design_settings']['rules'][field]
 ranks={'ignore':0,'warning':1,'error':2};weaker=[key for key,v in oldpro['board']['design_settings']['rule_severities'].items()if ranks.get(newpro['board']['design_settings']['rule_severities'].get(key,v),0)<ranks.get(v,0)];assert not weaker
 result=dict(legacy_dru_sha256=sha(OLD/'Velluneo_driver.kicad_dru'),generated_dru_sha256=sha(E/'Velluneo_driver.kicad_dru'),current_project_sha256=sha(E/'Velluneo_driver.kicad_pro'),declared_nets=27,unknown_categories=2,ordered_net_pairs=len(cases),clearance_differences=differences,global_minima_not_weaker=True,no_severity_downgrade=True,layer_combinations=16,object_type_combinations=16,equivalent_parameter_cases=len(cases)*16*16,cases=cases,scope='Independent restricted-AST evaluation of all ordered27net+empty+unknown pairs including same-net and fallback. Accepted grammar has no object/layer predicates, so equivalence quantifies over4x4layers and track/via/pad/zone pairs. Native positives/negatives and four-layer areas validated separately; no physical isolation certification.');(D/'checks/independent-policy-equivalence.json').write_text(json.dumps(result,indent=2)+'\n');print('Policy equivalent',len(cases),'orderednetpairs/',result['equivalent_parameter_cases'],'layer/objectparametercases')

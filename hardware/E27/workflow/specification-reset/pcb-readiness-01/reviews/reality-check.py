from pathlib import Path
import json,math,ast,hashlib,itertools
R=Path(r'C:/Users/kamil/Documents/Codex/2026-11-17/zo/work/Velluneo-readiness');P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-readiness-01';S=R.parent/'readiness-sources'
import fitz
ti=fitz.open(S/'ucc2871x.pdf')
for i in [4,5]:
 t=ti[i].get_text();print('TI page',i+1,t[t.find('NTC'):t.find('NTC')+1800])
ru=fitz.open(S/'rubycon-technical.pdf');print('Rubycon p24',ru[23].get_text()[-4700:])
vs=(S/'vishay-ntc-calculator.js').read_text();i=vs.index('function getRnom');print('Vishay rnom function',vs[i:i+1700]);i=vs.index('case"SMD1"');print('Vishay SMD1',vs[i:i+1600])
f=json.loads((D/'frozen-files.json').read_text())
for x in f['files']:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
# Independently execute only pure trajectory functions; no source top-level output writes.
tree=ast.parse((D/'startup-protection/calculate.py').read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
wr=json.loads((D/'startup-protection/results-160.json').read_text())['hot_winding_R_ohm']
g={'math':math,'NPS':4.,'NAS':22/30,'R13':979000.,'RBLEED':9790.,'wr':wr}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'pure-model-functions','exec'),g)
cases=json.loads((D/'startup-protection/results-160.json').read_text())['behavioral_model']['cases'];worst=min(cases[:64],key=lambda x:x['VDD_min_V'])
new=g['trajectory'](worst['config'],320)
assert abs(new['VDD_min_V']-worst['VDD_min_V'])<1e-3
print('Independent finer320-step active-case VDD',new['VDD_min_V'],'difference_from160',new['VDD_min_V']-worst['VDD_min_V'])
# Independently solve proposed linear thermal network via node difference relation.
maximum=0.;err=0.
for pd,pl,rx in itertools.product([0,2,4],[0,4,8],[1,5,30,100,math.inf]):
 if math.isinf(rx):td,tl=pd*7,pl*3.5
 else:
  transfer=(pd*7-pl*3.5)/(rx+7+3.5);td=7*(pd-transfer);tl=3.5*(pl+transfer)
 maximum=max(maximum,40+td,40+tl);err=max(err,abs(td/7+tl/3.5-pd-pl))
assert maximum<=68+1e-9
print('Independent thermal network maximum',maximum,'energy residual',err)
life=10000*2**((105-70)/10)*2**(-10/(10-.25*10));print('Independent Rubycon Eq17 no-credit life',life)
assert abs(life-json.loads((D/'thermal/results.json').read_text())['rubycon_eq17_conservative_at_target_h'])<1e-6
# Independently derive selected leakage fraction loss allocation.
ll=20e-6;lp=2.304e-3*.9;v=175.1164;ref=4*(27+1.7+.705633*1.434087)
print('Independent proposed20uH TVS normal allocation',11*ll/lp*v/(v-ref))
print('Read-only review checks complete; no physical or compliance result')

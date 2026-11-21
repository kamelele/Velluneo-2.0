"""Combined proposed winding DCR / backup-bias diagnostic; not native controller validation."""
from pathlib import Path
import json,ast,math,hashlib,itertools
D=Path(__file__).resolve().parent;P=D.parent
prior=json.loads((P/'pcb-readiness-01/startup-protection/results-160.json').read_text())
old=(P/'pcb-readiness-01/startup-protection/calculate.py').read_text()
assert old.count('base=.0035;')==1
tree=ast.parse(old.replace('base=.0035;','base=.0035+cfg.get("extra_bias_A",0.);'))
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
contract=json.loads((D/'transformer/construction-contract.json').read_text())
R20=contract['proposed_DCR20_upper_ohm'];alpha=.00393
ns={'math':math,'NPS':4.,'NAS':22/30,'R13':979000.,'RBLEED':9790.,'wr':prior['hot_winding_R_ohm']}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'source_pinned_pure_trajectory','exec'),ns)
cases=prior['behavioral_model']['cases'][:64];rows=[]
for temp,extra in itertools.product([10,125],[0.,85e-6]):
 ns['wr']={k:v*(1+alpha*(temp-20)) for k,v in R20.items()}
 for case in cases:
  cfg=case['config'].copy();cfg['extra_bias_A']=extra;r=ns['trajectory'](cfg,160);r.pop('trace',None)
  rows.append({'new_cut_length_DCR_temperature_C_screen':temp,'additional_backup_bias_A_screen':extra,**r})
worst=min(rows,key=lambda r:r['VDD_min_V']);finecfg=worst['config'].copy()
ns['wr']={k:v*(1+alpha*(worst['new_cut_length_DCR_temperature_C_screen']-20)) for k,v in R20.items()}
fine=ns['trajectory'](finecfg,320);fine.pop('trace',None)
assert abs(fine['VDD_min_V']-worst['VDD_min_V'])<1e-4
groups=[]
for temp,extra in itertools.product([10,125],[0.,85e-6]):
 rs=[r for r in rows if r['new_cut_length_DCR_temperature_C_screen']==temp and r['additional_backup_bias_A_screen']==extra]
 groups.append({'temperature_C_screen':temp,'backup_bias_A_screen':extra,'cases':len(rs),'minimum_VDD_V':min(r['VDD_min_V'] for r in rs),'maximum_VDD_V':max(r['VDD_max_V'] for r in rs)})
# Reuse only the declared passive clamp formula at selected slab estimate and proposed acceptance ceiling.
clamp=[]
for Lp,leak in itertools.product([.002304*.9,.002304,.002304*1.1],[14.0615e-6,20e-6]):
 lm=Lp-leak;Vr=4*(27+1.7+1.01194);Vc=175.1164
 assert Vc>Vr*(1+leak/lm)
 frac=leak/Lp*Vc/(Vc-Vr);clamp.append({'Lp_H':Lp,'effective_PS_leakage_H_hypothesis':leak,'TVS_normal_W_at11W_magnetic_rate_hypothesis':11*frac,'available0p4W_allocation_W':.4})
out={'kind':'Executed combined design-proposal diagnostic, not real/controller-native/three-winding transient validation','input_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'pcb-readiness-01/startup-protection/calculate.py',P/'pcb-readiness-01/startup-protection/results-160.json',D/'transformer/construction-contract.json']},'cases':len(rows),'case_grid_digest_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'groups':groups,'worst160':worst,'matched320':fine,'refinement_VDD_difference_V':fine['VDD_min_V']-worst['VDD_min_V'],'clamp_screens':clamp,'limits':['New cut-length DCR limits are proposed procurement conditions, not measured or guaranteed actual transformer values.125C is a stress diagnostic beyond110C normal winding target.','This model remains ideal-coupled plus finite winding resistances; new slab leakage/capacitance/leadouts and the full native TI law are absent. Matching a threshold is not a complete startup/fault pass.','85uA is the backup enabledbias screen only; LDO output charging and uniform-source charging sensitivities remain separately in controller report.','11W magnetic-energy rate is a normal hypothesis, not an actual combined input/driver thermal bound or a fault-power limit.','The slab14.0615uH is not a parameter guarantee; the20uH acceptance proposal still requires actual three-winding characterization/source-conditioned equivalent model.']}
(D/'cross-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'groups':groups,'worst160VDD':worst['VDD_min_V'],'matched320VDD':fine['VDD_min_V'],'refinement_V':out['refinement_VDD_difference_V'],'clamp_screens':clamp},indent=2))

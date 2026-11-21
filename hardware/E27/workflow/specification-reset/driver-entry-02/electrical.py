"""Source-bound preparation calculations, never physical qualification."""
from pathlib import Path
import json, hashlib, math
import numpy as np
D=Path(__file__).resolve().parent; P=D.parent
src=P/'design-closure-02/transformer/results.json'; old=json.loads(src.read_text(encoding='utf-8'))
A=np.array(old['selected_balanced_two_coordinate_leakage_matrix_H'],dtype=float)
assert A.shape==(2,2) and np.allclose(A,A.T) and np.linalg.eigvalsh(A).min()>0
n=np.array([1,22/120,30/120]); rows=[]
for scale in(1,20e-6/A[0,0]):
 for lp in(2.304e-3*.9,2.304e-3,2.304e-3*1.1):
  air=np.zeros((3,3));air[:2,:2]=A*scale;mat=(lp-air[0,0])*np.outer(n,n)+air
  eig=np.linalg.eigvalsh(mat);assert eig.min()>0 and abs(mat[0,0]-lp)<1e-15
  k=mat/np.sqrt(np.outer(np.diag(mat),np.diag(mat)));assert np.all(np.abs(k)<=1+1e-12)
  # Schur complements correspond to one shorted port with third port open.
  sc={i+j:float(mat[a,a]-mat[a,b]**2/mat[b,b])for a,i in enumerate('PAS')for b,j in enumerate('PAS')if a!=b}
  # Independent energy identity in the magnetically balanced subspace.
  errors=[]
  for ip,ia in((1,0),(0,1),(.2,-.5),(-1,2)):
   currents=np.array([ip,ia,-(120*ip+22*ia)/30]);ab=np.array([ip,ia]);errors.append(abs(currents@mat@currents-ab@(A*scale)@ab))
  assert max(errors)<1e-16
  rows.append({'Lp_H':lp,'air_model_scale':scale,'inductance_matrix_H':mat.tolist(),'coupling_matrix':k.tolist(),'eigenvalues_H':eig.tolist(),'determinant_H3':float(np.linalg.det(mat)),'one_shorted_port_other_open_H':sc,'balanced_energy_residual_H':max(errors),'qualified_transformer_model':False})
nom=rows[1];m=np.array(nom['inductance_matrix_H']);k=np.array(nom['coupling_matrix'])
net=['* Constructed C2 three-port sensitivity surrogate, not a validated transformer or UCC28711 model.',
 '* Nominal Lp maintained; P/A slab energy embedded with a zero S leakage gauge.',
 '* No core saturation, winding DCR/capacitance, frequency dependence or temperature model.',
 '.subckt T1_C2_SURROGATE P1 P5 A2 A4 S6 S10',f'LP P1 P5 {m[0,0]:.14g}',f'LA A2 A4 {m[1,1]:.14g}',f'LS S6 S10 {m[2,2]:.14g}',f'KPA LP LA {k[0,1]:.14g}',f'KPS LP LS {k[0,2]:.14g}',f'KAS LA LS {k[1,2]:.14g}','.ends T1_C2_SURROGATE']
(D/'T1-C2-surrogate.cir').write_text('\n'.join(net)+'\n',encoding='utf-8',newline='\n')
protection=[]
for vac in(207,230,253):
 c=18e-6;r=47*.95;v=math.sqrt(2)*vac
 protection.append({'Vac':vac,'Rmin_ohm':r,'Cmax_F':c,'stored_and_ideal_charge_resistor_energy_J':.5*c*v*v,'peak_charge_A':v/r,'charge_integral_A2s':c*vac*vac/r,'RC_s':r*c,'equivalent_peak_power_duration_s':r*c/2,'initial_nominal_hard_short_current_A':vac/47,'initial_nominal_hard_short_power_W':vac*vac/47,'initial_hard_short_power_tolerance_W':[vac*vac/(47*1.05),vac*vac/(47*.95)]})
sources=[]
# Source files are external to the design repository. Do not redistribute PDFs.
# This optional argument is explicit to avoid relying on a machine-specific path.
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path);args=ap.parse_args()
required={'acxxcs.pdf':('https://www.vishay.com/docs/28909/acxxcs.pdf','bbe53d35ac9f13a184a8f28f40b08d5836e6b0f0794f893939eee57f4613c0fc',[2,7,8]),'ac0xcsenrgymet.pdf':('https://www.vishay.com/docs/28897/ac0xcsenrgymet.pdf','ff50ffda647058b93c0de17ea0e2df748a0e941a3c27b3c5930b65f883e39310',[2,3])}
for name,(url,sha,pages)in required.items():
 if args.source_dir:assert hashlib.sha256((args.source_dir/name).read_bytes()).hexdigest()==sha,name
 sources.append({'name':name,'url':url,'sha256':sha,'pages':pages,'native_bytes_verified_this_run':bool(args.source_dir)})
result={'base':'f0216041fc47fef993e24939c6f31727fe409a14','scope':'Calculated preparation evidence; no changed circuit, manufacturer confirmation, physical measurement, validated dynamic converter or stage approval.',
 'magnetic_input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'balanced_air_matrix_H':A.tolist(),'three_port_surrogate_cases':rows,
 'protection_screen':protection,'R1_candidate':{'proposed_mpn':'AC05000004709J6BCS','ordering_code_status':'Derived from manufacturer ordering table; exact order identity remains to confirm','body_max_mm':[17,10],'not_drop_in':True,'source_fusing_test_Vac':230,'source_fusing_max_s':2,'source_post_fuse_R_lower_ohm':100000,'accepted_for_253Vac':False,'charge_endurance_qualified':False,'applied':False},
 'sources':sources,'remaining':['Actual bounded controller startup/short/open/VS/CS/NTC state and pulse-energy model.','Finished magnetic construction/parameter/loss contract and insulation coordination.','Input charge endurance and R1/F1/BR1 fault coordination at actual supply/source conditions.','Local component temperatures and sensor response versus driver mounting boundary.'],'PCB_entry_ready':False}
(D/'electrical-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'magnetic_surrogate_cases':len(rows),'SPD_and_balanced_energy_checks':True,'source_bytes_checked':bool(args.source_dir),'protection_cases':len(protection),'PCB_entry_ready':False}))

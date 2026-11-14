#!/usr/bin/env python3
"""Independent ideal DCM/PFC feasibility witness, not a LYTSwitch-5 simulator.
Run beside earlier results.json: python dcm.py > dcm-results.json
No programmed frequency law, transformer winding instruction or safe limit is selected.
"""
import hashlib, itertools, json, math
from pathlib import Path

upstream=Path(__file__).with_name('results.json').read_bytes()
assert hashlib.sha256(upstream).hexdigest()=='6435677103247ad888ab1bdf2078409f8a5ecadcf165749fc70191534f4addb3'
A={
 'mains_rms_V':[207,230,253], 'line_Hz':50,
 'Vo_V':[18,21,24,27], 'I_load_A':[.228,.25,.2835+27/9900],
 'equivalent_extra_secondary_budget_W':[0,.3],
 'Lp_nom_H':.0005, 'Lp_factors':[.9,1.1],
 'Np':96,'Ns':24,'Na_exploratory':12,'Ae_m2':31e-6,
 'Vdiode_assumed_V':.8,'bias_diode_assumed_V':.7,
 'frequency_witness_floor_Hz':42000,'frequency_witness_Hz_per_W':9500,
 'frequency_jitter_factors':[.96,1.04],
 'phase_degrees':[5,15,30,45,60,75,85,90],
 'LYT_frequency_min_typ_Hz':40000,'LYT_fmax_min_at25C_Hz':115300,
 'LYT_Ton_min_max_at25C_s':1.15e-6,'LYT_Ton_max_min_at25C_s':5.75e-6,
 'LYT5225_ILIM_min_at25C_A':1.232,'LYT5225_ILIM_max_at25C_A':1.418,
 'LYT5225_Rds_max_at100C_ohm':6.55,
 'drain_overshoot_assumed_V':100,
}
n=A['Np']/A['Ns']
rows=[]
phase_count=0
for vac,vo,io,extra,ltol,jit in itertools.product(A['mains_rms_V'],A['Vo_V'],A['I_load_A'],A['equivalent_extra_secondary_budget_W'],A['Lp_factors'],A['frequency_jitter_factors']):
 lp=A['Lp_nom_H']*ltol
 # ALL extra budget is assigned to an equivalent secondary load for this witness.
 # It is NOT an actual loss calculation or additional required LED output.
 pmag=io*(vo+A['Vdiode_assumed_V'])+extra
 f_nom=max(A['frequency_witness_floor_Hz'],A['frequency_witness_Hz_per_W']*pmag)
 f=f_nom*jit
 vp=vac*math.sqrt(2)
 vr=n*(vo+A['Vdiode_assumed_V'])
 ip=math.sqrt(4*pmag/(lp*f))
 ton=lp*ip/vp
 demag=lp*ip/vr
 kdp=(1/f-ton)/demag
 zero=1/f-ton-demag
 # Primary RMS: mean sin^2=1/2. Secondary RMS: mean |sin|^3=4/(3*pi).
 prms=ip*math.sqrt(ton*f/6)
 srms=n*ip*math.sqrt(demag*f*4/(9*math.pi))
 secondary_avg=n*ip*demag*f/4
 assert math.isclose(.25*lp*ip**2*f,pmag,rel_tol=1e-12)
 assert math.isclose(secondary_avg,pmag/(vo+A['Vdiode_assumed_V']),rel_tol=1e-12)
 for deg in A['phase_degrees']:
  sine=math.sin(math.radians(deg))
  instantaneous_vin=vp*sine
  instantaneous_ip=ip*sine
  instantaneous_ton=lp*instantaneous_ip/instantaneous_vin
  instantaneous_demag=lp*instantaneous_ip/vr
  assert math.isclose(instantaneous_ton,ton,rel_tol=1e-12)
  assert 1/f-instantaneous_ton-instantaneous_demag>=zero-1e-15
  phase_count+=1
 rows.append(dict(vac_rms_V=vac,vo_V=vo,io_A=io,extra_equivalent_secondary_W=extra,
  lp_H=lp,f_nom_Hz=f_nom,jitter_factor=jit,f_Hz=f,ton_s=ton,
  demag_crest_s=demag,zero_interval_crest_s=zero,KDP_crest=kdp,
  primary_peak_crest_A=ip,secondary_peak_crest_A=n*ip,
  primary_rms_line_A=prms,secondary_rms_line_A=srms,
  equivalent_secondary_average_A=secondary_avg,
  flux_swing_crest_T=lp*ip/(A['Np']*A['Ae_m2']),
  magnetic_transfer_average_W=pmag,
  drain_plateau_crest_V=vp+vr,drain_assumed_spike_V=vp+vr+A['drain_overshoot_assumed_V'],
  rectifier_reverse_before_ringing_V=vo+vp/n,
  switch_conduction_hot100C_proxy_W=prms**2*A['LYT5225_Rds_max_at100C_ohm'],
  rectifier_fixed_drop_proxy_W=A['Vdiode_assumed_V']*secondary_avg))

keys=['f_Hz','ton_s','zero_interval_crest_s','KDP_crest','primary_peak_crest_A','secondary_peak_crest_A','primary_rms_line_A','secondary_rms_line_A','flux_swing_crest_T','magnetic_transfer_average_W','drain_plateau_crest_V','drain_assumed_spike_V','rectifier_reverse_before_ringing_V','switch_conduction_hot100C_proxy_W','rectifier_fixed_drop_proxy_W']
bounds={k:{'min':min(r[k] for r in rows),'max':max(r[k] for r in rows)} for k in keys}
screen={'frequency_above_typical_40k':all(r['f_Hz']>=A['LYT_frequency_min_typ_Hz'] for r in rows),
 'frequency_below_25C_minimum_fmax':all(r['f_Hz']<=A['LYT_fmax_min_at25C_Hz'] for r in rows),
 'ton_at_least_25C_max_minimum':all(r['ton_s']>=A['LYT_Ton_min_max_at25C_s'] for r in rows),
 'ton_below_25C_minimum_maximum':all(r['ton_s']<=A['LYT_Ton_max_min_at25C_s'] for r in rows),
 'KDP_gt_1p2':all(r['KDP_crest']>1.2 for r in rows),
 'peak_below_25C_min_ILIM':all(r['primary_peak_crest_A']<A['LYT5225_ILIM_min_at25C_A'] for r in rows)}
# Store analysis with hypothetical constant output load and sinusoidal unity-PF input power.
# Vc is sqrt(mean(V^2)), not an asserted average output voltage of a real LED load.
cap=[]
for vo,io,cnom in itertools.product([18,21,27],[.25,.2835],[220e-6,470e-6,1000e-6]):
 c=cnom*.8
 p=vo*io
 energy_swing=p/(2*math.pi*A['line_Hz']) # peak-to-peak cap energy
 amp_v_squared=p/(2*math.pi*A['line_Hz']*c)
 vmin=math.sqrt(vo**2-amp_v_squared) if vo**2>=amp_v_squared else None
 vmax=math.sqrt(vo**2+amp_v_squared)
 # 10k +1% bleed / cap +20% discharge example. No safety delay is chosen.
 discharge=10000*1.01*cnom*1.2*math.log(30/5)
 cap.append(dict(center_sqrt_mean_square_V=vo,constant_load_A=io,cap_nom_F=cnom,cap_min_F=c,
  stored_energy_swing_pp_J=energy_swing,Vmin_ideal_V=vmin,Vmax_ideal_V=vmax,
  voltage_pp_V=None if vmin is None else vmax-vmin,
  estimated_100Hz_cap_ripple_rms_A=io/math.sqrt(2),
  illustrative_bleed_30to5_s_Cplus20_Rplus1=discharge,
  not_a_flicker_or_safe_access_result=True))

# Pure sensitivity, NOT a validated current-limited fault waveform (table is at25C).
flux_limit=A['Lp_nom_H']*1.1*A['LYT5225_ILIM_max_at25C_A']/(A['Np']*A['Ae_m2'])
print(json.dumps({'model':'Ideal sinusoidal-power DCM witness; not IC control/line/fault simulation',
 'upstream_results_SHA256':hashlib.sha256(upstream).hexdigest(),'assumptions':A,
 'electrical_cases':len(rows),'phase_samples':phase_count,'bounds':bounds,
 'algebraic_checks_against_limited_table_values':screen,
 'minimum_on_time_case':min(rows,key=lambda r:r['ton_s']),
 'maximum_flux_case':max(rows,key=lambda r:r['flux_swing_crest_T']),
 'maximum_secondary_RMS_case':max(rows,key=lambda r:r['secondary_rms_line_A']),
 'transformer_candidate':{'Lp_H':A['Lp_nom_H'],'Np':A['Np'],'Ns':A['Ns'],'Na_exploratory':A['Na_exploratory'],
  'required_AL_nH':A['Lp_nom_H']/A['Np']**2*1e9,'AL_is_custom_unconfirmed':True,
  'normal_bias_V_assuming_drops':[(vo+A['Vdiode_assumed_V'])*A['Na_exploratory']/A['Ns']-A['bias_diode_assumed_V'] for vo in [18,27]],
  'flux_at_25C_table_ILIM_max_and_Lpmax_T_linear':flux_limit,
  'propagation_delay_not_added_to_measured_current_limit':True,
  'winding_fill_losses_and_insulation_unverified':True},
 'output_storage_screen':cap,
 'verification':'Dependency hash, magnetic energy/current identities and phase-sample comparisons executed. No controller, fault, CAD or physical validation.'},indent=2))

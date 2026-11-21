#!/usr/bin/env python3
"""Ideal single-cycle CrM feasibility screen, not a controller/circuit simulation.
Run: python calculate.py > results.json
All numeric inputs below are analyst assumptions unless source is identified.
"""
import itertools, json, math

ASSUMPTIONS = {
    'bulk_V': [200, 260, 253 * math.sqrt(2)],
    'output_V': [18, 21, 24, 27],
    'total_secondary_average_A': [.228, .25, .2835 + 27/9900],
    'Lp_nominal_H': [0.0040, 0.0047, 0.0056],
    'Lp_tolerance_factors': [.9, 1.1],
    'ratio_Np_Ns': 4,
    'secondary_diode_assumed_V': .8,
    'dead_time_s': [.5e-6, 1.5e-6],
    'Np': 200,
    'Ae_m2': 31e-6,  # TDK EFD20/10/7 datasheet, effective AND minimum area
    'MOSFET_conduction_proxy_R_ohm': 4.5, # ST max at Vgs10V/Tj25C ONLY
    'switching_overlap_assumed_s': 50e-9,
    'drain_overshoot_assumed_V': 100,
}

def cycle(vin, vo, io, lp, td):
    n = ASSUMPTIONS['ratio_Np_Ns']
    vr = n*(vo+ASSUMPTIONS['secondary_diode_assumed_V'])
    # io = .5*n*ip*toff/T ; T=ton+toff+td
    a = .5*n*lp/vr
    b = -io*lp*(1/vin+1/vr)
    c = -io*td
    ip = (-b+math.sqrt(b*b-4*a*c))/(2*a)
    ton, toff = lp*ip/vin, lp*ip/vr
    period = ton+toff+td
    irms = ip*math.sqrt(ton/(3*period))
    srms = n*ip*math.sqrt(toff/(3*period))
    power = .5*lp*ip*ip/period
    # Energy balance is an invariant of this idealized triangular model.
    assert math.isclose(power, io*(vo+ASSUMPTIONS['secondary_diode_assumed_V']), rel_tol=1e-12)
    assert math.isclose(.5*n*ip*toff/period, io, rel_tol=1e-12)
    return dict(vin_V=vin, vo_V=vo, total_secondary_A=io, lp_H=lp,
        dead_time_s=td, primary_peak_A=ip, secondary_peak_A=n*ip,
        primary_rms_A=irms, secondary_rms_A=srms, frequency_Hz=1/period,
        ton_s=ton, toff_s=toff, flux_swing_T=lp*ip/(ASSUMPTIONS['Np']*ASSUMPTIONS['Ae_m2']),
        ideal_magnetic_transfer_W=power,
        mosfet_conduction_25C_10V_proxy_W=irms**2*ASSUMPTIONS['MOSFET_conduction_proxy_R_ohm'],
        diode_fixed_drop_proxy_W=ASSUMPTIONS['secondary_diode_assumed_V']*io,
        drain_flat_V=vin+vr,
        drain_assumed_overshoot_V=vin+vr+ASSUMPTIONS['drain_overshoot_assumed_V'],
        diode_reverse_before_ringing_V=vo+vin/n,
        hard_switching_overlap_proxy_W=.5*(vin+vr)*ip*ASSUMPTIONS['switching_overlap_assumed_s']/period)

def bounds(rows, keys):
    return {k:{'min':min(r[k] for r in rows),'max':max(r[k] for r in rows)} for k in keys}

keys=['primary_peak_A','secondary_peak_A','primary_rms_A','secondary_rms_A',
      'frequency_Hz','ton_s','flux_swing_T','ideal_magnetic_transfer_W',
      'mosfet_conduction_25C_10V_proxy_W','diode_fixed_drop_proxy_W',
      'drain_flat_V','drain_assumed_overshoot_V','diode_reverse_before_ringing_V',
      'hard_switching_overlap_proxy_W']
variants=[]
for nominal in ASSUMPTIONS['Lp_nominal_H']:
    rows=[cycle(v,vout,io,nominal*tol,td) for v,vout,io,tol,td in itertools.product(
        ASSUMPTIONS['bulk_V'],ASSUMPTIONS['output_V'],ASSUMPTIONS['total_secondary_average_A'],
        ASSUMPTIONS['Lp_tolerance_factors'],ASSUMPTIONS['dead_time_s'])]
    variants.append({'nominal_Lp_H':nominal,'corners':len(rows),'bounds':bounds(rows,keys),
        'max_flux_case':max(rows,key=lambda r:r['flux_swing_T']),
        'max_frequency_case':max(rows,key=lambda r:r['frequency_Hz'])})

# Transformer candidate on a published AL100 +-10% gapped core; NOT a winding recipe.
al=100e-9
np=ASSUMPTIONS['Np']
lp=al*np*np
# No-lower bound is inferred for hard current limit, which is not chosen.
hard_limit_flux=[{'assumed_primary_limit_A':i,'flux_T_at_Lp_max':lp*1.1*i/(np*ASSUMPTIONS['Ae_m2'])} for i in [.25,.30,.35]]
# Simplified air gap neglects ferrite reluctance and fringing, not the TDK mechanical gap.
gap=4*math.pi*1e-7*ASSUMPTIONS['Ae_m2']*np*np/lp
# Rectifier-capacitor hold-up upper droop screen, not a line waveform/PF model.
cmin=10e-6*.8
lowpeak=207*math.sqrt(2)
bulk_min=math.sqrt(lowpeak**2-2*10*.010/cmin)
# OVP senses raw auxiliary winding plateau = Vo+0.8 (Ns=Na), before rectifier.
# k includes ratio/divider; +1V load dump overshoot is a hypothetical budget.
normal_aux=27+ASSUMPTIONS['secondary_diode_assumed_V']
ovp={}
for proposed_cap in [30,33,36]:
    max_k=4.1/(normal_aux*1.10)
    min_k=4.5/(proposed_cap-1+ASSUMPTIONS['secondary_diode_assumed_V'])
    ovp[str(proposed_cap)]={'cap_V_assumption':proposed_cap,'load_dump_allowance_V_assumption':1,
        'normal_headroom_factor_assumption':1.10,'max_k_avoid_normal_trip':max_k,
        'min_k_limit_trip':min_k,'ideal_interval_exists':min_k<=max_k,
        'divider_tolerance_included':False}

print(json.dumps({'model':'ideal single-cycle CrM / no control loop, parasitics or fault simulation',
    'assumptions':ASSUMPTIONS,'variants':variants,
    'published_AL100_core_candidate':{'Np':np,'Ns':50,'Na_exploratory':50,'nominal_Lp_H':lp,
        'effective_gap_approx_m':gap,'published_mechanical_gap_m':.00049,
        'note':'Calculated effective gap is NOT a machining instruction; insulation/fill/core loss unverified.',
        'hard_limit_flux_sensitivity':hard_limit_flux},
    'bulk_hold_up_screen':{'cap_nominal_F':10e-6,'cap_min_F':cmin,'power_W':10,'discharge_s':.010,'low_line_peak_V':lowpeak,'calculated_min_V':bulk_min},
    'auxiliary_supply':{'Na_Ns_assumption':1,'normal_aux_range_V':[18+.3,27+.3],
        'startup_UVLO_max_V_from_TI':29,'running_UVLO_max_V_from_TI':15.7,
        'startup_UVLO_min_V_from_TI':23,
        'conservative_threshold_only_energy_screen_J_8uF':.5*8e-6*(23**2-15.7**2),
        'threshold_extremes_not_correlated':True,
        'hold_up_s_if_10mA_constant_draw_example':8e-6*(23-15.7)/.010,
        'not_a_selected_cap_or_draw':True},
    'OVP_tolerance_screen':ovp,
    'verification':'Energy and secondary-current identities checked at every enumerated corner. No SPICE, CAD or physical tests.'},indent=2))

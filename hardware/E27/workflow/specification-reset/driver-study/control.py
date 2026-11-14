#!/usr/bin/env python3
"""Startup/current-programming sensitivity calculations, NOT schematic or fault simulation.
Run beside the prior frozen results.json: python control.py > control-results.json
"""
from pathlib import Path
import hashlib, itertools, json, math

source=Path(__file__).with_name('results.json')
raw=source.read_bytes()
digest=hashlib.sha256(raw).hexdigest()
assert digest == '6435677103247ad888ab1bdf2078409f8a5ecadcf165749fc70191534f4addb3', 'Review upstream model before changing this dependency'
prior=json.loads(raw)
a=prior['assumptions']
n=a['ratio_Np_Ns']
vref=.14  # TI typical design equation, not a guaranteed tolerance
sense_tolerance=.01
sense_rows=[]
for r in [2.21,2.24,2.26]:
    total=vref*n/r
    row={'R_ohm':r,'ideal_total_secondary_A':total,
         'LED_A_assuming_10kohm_bleed':{str(v):total-v/10000 for v in [18,21,24,27]},
         'ideal_total_A_resistor_tolerance_only':[vref*n/(r*1.01),vref*n/(r*.99)]}
    sense_rows.append(row)

# Deliberately use 2.21 ohm only as a programming comparison, not a selected resistor.
r=2.21
ocp=[]
for label,thresholds in [('isolated-mode comparator',[3.2,3.6]),('lower comparator reference configuration',[.59,.68])]:
    cases=[]
    for vth,rtol,lp,vbulk in itertools.product(thresholds,[.99,1.01],[.004*.9,.004*1.1],[200,253*math.sqrt(2)]):
        trip=vth/(r*rtol)
        # 210 ns is typical at TI test conditions, NOT guaranteed worst-case delay.
        peak=trip+vbulk/lp*210e-9
        cases.append({'trip_A':trip,'delay_proxy_peak_A':peak,
                      'linear_flux_at_trip_T':lp*trip/(a['Np']*a['Ae_m2']),
                      'linear_flux_with_typical_delay_proxy_T':lp*peak/(a['Np']*a['Ae_m2'])})
    ocp.append({'configuration_label':label,'thresholds_V':thresholds,
                'bounds':{key:{'min':min(c[key] for c in cases),'max':max(c[key] for c in cases)} for key in cases[0]},
                'interpretation':'Linear extrapolation only; not physical saturation waveform or a safe threshold.'})

# Analyst startup proposal: series resistance from RECTIFIED/SMOOTHED DC bus, not the TI AC-connected example.
startup=[]
for rstart in [430000,680000,1000000]:
    lowbus,highbus=200,253*math.sqrt(2)
    rmax,rmin=rstart*1.01,rstart*.99
    cmax,cmin=10e-6*1.2,10e-6*.8
    istartmax=14.75e-6
    target=29
    veq=lowbus-istartmax*rmax
    tcharge=rmax*cmax*math.log(veq/(veq-target)) if veq>target else None
    feedmax=(highbus-10.4)/rmin
    feedmin=(lowbus-target)/rmax
    # For dropout bound, intentionally ignore helpful feed current.
    hold={str(draw):cmin*(23-15.7)/draw for draw in [.002,.005,.010]}
    startup.append({'startup_R_nom_ohm':rstart,'bus_assumed_V':[lowbus,highbus],
        'cap_nom_F':10e-6,'cap_tolerance':.2,'R_tolerance':.01,
        'startup_source_min_A_at29V':feedmin,'startup_sink_max_A':istartmax,
        'min_source_exceeds_startup_sink':feedmin>istartmax,
        'source_max_A_at10p4V':feedmax,'not_switching_sink_min_A':.0009,
        'net_discharge_min_A_not_switching_screen':.0009-feedmax,
        'source_below_not_switching_sink':feedmax<.0009,
        'charge_0_to29V_s_at_lowbus_and_maxRC':tcharge,
        'R_loss_W_upper_at_highbus_VCC0':highbus**2/rmin,
        'R_loss_W_at_highbus_VCC18p3':(highbus-18.3)**2/rmin,
        'hold_23_to15p7V_s_ignoring_feed_assumed_draw_A':hold,
        'unmodeled':'Bridge waveform, initial bus rise, load startup, bias transfer, tolerances outside table, temperature/leakage, actual gate draw, faults.'})
    assert feedmin>istartmax

# Independent ideal bucketing of additional load from the former illustrative bleeder.
panel250=[{'Vo_V':v,'total_for_250mA_LED_A':.25+v/10000,
           'R_ideal_for_250mA_LED_ohm':vref*n/(.25+v/10000)} for v in [18,21,24,27]]

print(json.dumps({'study':'current programming / DC-fed startup / limit sensitivity',
    'dependency_SHA256':digest,'upstream_model':'VEL-FLYBACK-01 r2 results.json',
    'sense_equation':'R = 0.14 * (Np/Ns) / I_total_secondary; no controller-accuracy guarantee',
    'sense_rows':sense_rows,'bleeder_offset':panel250,'OCP_screen':ocp,
    'startup_rows':startup,
    'verification':'Executed arithmetic and dependency hash check only; no controller, SPICE, CAD, physical or fault pass.'},indent=2))

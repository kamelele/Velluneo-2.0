#!/usr/bin/env python3
"""Conservative conditional budgets; no switched-controller or physical validation."""
from pathlib import Path
import json,math,hashlib
D=Path(__file__).resolve().parent;P=D.parent
inp=json.loads((D/'input-corners-results.json').read_text())['summary']['proposed_two_series_pairs']['bounds']
# Source-bound previous peak current, conditional ordinary DCM magnetizing model.
Vmin=inp['bulk_min_V'][0];Ipk=.358521767;Pmag=11.
Irms=math.sqrt(2*Pmag*Ipk/(3*Vmin));tri=inp['line_rms_A'][1]+Irms
out={'scope':'conditional steady-state DCM model; inherited peak bound and same11W maximum bus power; not startup/fault/transient or actual waveform','bulk_min_V':Vmin,'maximum_bus_power_bound_W':Pmag,'inherited_primary_peak_bound_A':Ipk,'primary_rms_from_energy_bound_A':Irms,'derivation':'Ip_rms^2=f*Ip^2*ton/3; Pmag=f*Lp*Ip^2/2; ton=Lp*Ip/V. Therefore <=2*Pmag*Ip/(3*Vmin). Assumes ideal linear fully-reset triangular magnetizing current, bounded power and peak.','capacitor_total_rms_triangle_bound_A':tri,'triangle_note':'Ic=Ibridge-Ip; RMS(Ic)<=RMS(Ibridge)+RMS(Ip), combining separate maxima conservatively. Averaged line-current model is not a proven switching-current bound.','native15uF_120Hz_rating_A':.190,'conservative_low_frequency_factor':.8,'all_band_conservative_rating_A':.190*.8,'ratio_of_conservative_bound_to_rating':tri/(.190*.8),'conclusion':'This conservative screen does not establish15uF ripple acceptance; it does not prove actual capacitor fails. Need actual/sufficiently bounded current spectrum, thermal/ripple assessment before accepting input stage. No capacitance ECO selected.','transformer_propagation':'Measured/guaranteed hot winding resistances and AC/core/aux loss must be propagated through real regulation, auxiliary takeover and thermal model; ideal transformer sweeps are not silently upgraded to physical results.'}
(D/'integration-limits.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

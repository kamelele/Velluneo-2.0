# Coupled post-unplug energy screen

This extends a simple output RC estimate to total stored energy, conditional on a complete passive energy-decay contract. It does not establish an approved user waiting time or single-fault product compliance.

For a capacitor with its permanent shunt R, resistor power is2E/(RC). For a passive coupled magnetic matrix L, stored energy is0.5*iT*L*i; if L is positive semidefinite, trace(L)<=3mH and every winding resistance>=1mohm, dissipation is at least2E/3s. If every additional stored-energy mode has an equally strong decay bound, internal passive conversion merely redistributes energy. Therefore Etotal(t)<=E0*exp(-2t/tau_max). The permanent base output capacitor minimum8uF gives Vout<=sqrt(2Etotal/8uF), irrespective of transfers between included stores.

The script uses deliberately loose capacitor-rating initial voltage ceilings450/50/63V, not circuit operating ratings. Maximum18uF bulk,0.989961uF bias and20.592uF total output plus<=1mJ other initial storage give E0=1.865602275J. Additional panel capacitance or another energy source must be added, not ignored. All omitted reactive modes must meet the decay contract; trace(L) and resistance are acceptance conditions, not measured transformer properties. Semiconductor conduction must remain passive and no external backfeed/reinsertion is allowed.

With all bias/output shunts intact, the slowest tau is9.170622s for both bulk branches,18.341244s if one complete bulk branch opens,6.113748s for the selected single-bleeder-short equivalent. The energy target100uJ implies both Vout<=5V and totalenergy<=0.5mJ. Corresponding times are45.092/90.183/30.061s. A100s electrical design screen is conditional on those cases and assumptions only. It does not cover a missing R13, output shunt failure, arbitrary controller faults or unbounded external storage.

Cooling can be slower than electrical discharge. A hypothetical68C surface cooling toward40C with60s time constant takes103.37s to45C;120s takes206.73s. Actual thermal time constants are unknown. The eventual user wait must cover independently verified complete-assembly electrical discharge and cooling, with uncertainties and all selected conditions. No “100s is safe” user instruction is issued.

Run `python service-energy.py`; service-energy.json/log retain the actual result. Later physical validation requires an approved matched-assembly plan, qualified personnel/setup and explicit fault conditions. This packet authorizes none of those physical activities.

# Clamp and finite-winding commutation constraints

ELEC-REFINE-02,/root. Algebraic design frontiers only. No MOS/TVS value change, diode upgrade, native-controller simulation or closed RC-COMP-002 claim.

The prior directclamp sensitivity includes bus357.796V,hotTVS plateau286.972V and clampdiode1.7V, giving646.468V before commutation. The700V **engineering screen**,distinct from the MOS800V absolute rating, leaves53.532V total extra overshoot allocation. The old50V assumed allowance therefore leaves only3.532V to that engineering screen. The hotplateau was obtained using a VBRtemperaturecoefficient onVCL, so it is explicitly a *proxy*,not a guaranteed hot dynamicI-V limit. No drainwaveform was measured or validated by this algebra.

For one added loopinductance alone, deltaV=L*deltaI/deltat. The savedtable gives the maximumL conditional on the chosen edge/current and no other overshoot mechanism. At a1ns edge this is~149nH,at10ns~1493nH. These are derived budgets,not an approvedlayout limit, measurededge/inductance or proof of a diode/TVS/gate transition. Actualreturnloop, gateMiller behavior, diode/TVS recovery and strayC/L must be bounded together before accepting that allocation. The exactMOS nativeQg/Coss/timing data are typical under different testconditions and do not supply this bound automatically.

The125°C/60mm winding screen gives secondaryR~.70563ohm and separate-normal-peakI~1.43409A, a1.01194V secondarydrop. A conservative allocation that ignores a potentially reducingprimaryIRterm keeps that drop in reflectedsecondaryvoltage:

    Vref_proxy = 4*(Vo + VFout + Isec*Rs)
    Vref_proxy < VTVSmin_proxy + Vclampdiode_min_assumed

With inherited175.1164V minimumTVSproxy and.7V diode assumption, the corresponding outputfrontier is~41.742V rather than~42.754V when windingdrop is omitted. This is a clamp-exclusion frontier for these hypotheses,not a guaranteedOVP threshold. Tablepoints27/37.4784/40/41.2266/42V are sensitivities. In particular41.2266V is an auxiliarysamplecurrent sensitivity from startup-protection,not a guaranteed/observed or physicallycoincidentOVPcorner. At42V this mixed-cornerallocation no longer excludes TVSconducting beyond leakage reset; reusing the normalleakage-only heatmodel there would be unjustified.

The separately maximizedcurrent, hotsecondarywire and coldTVSproxy are conservative spatial/time combinations,not oneassertedphysicaltrajectory.40V remains an illustrative unapproved engineering faultceiling; no ownerrequirement or contact safety limit is inferred. A validatedactualOVP/VSsampling envelope and actualclampcurve must be consistent with the finitewinding/drop budget. If the resulting margin is inadequate, prepare a specific protection/MOS/clamp ECO; silently reducing a clamp voltage could divert magnetizing energy and harmstart/CV/OVP behavior.

The normal-onlyTVSpowerproxy.23856W requires Rtheta<=~167.7K/W for the assumedlocal85°C/target125°C thermalbudget. No currentPCBoractualthermalresistance is available and this proxydoesnot coverfaulttrains/surge. Singlepulse600W TVSrating is not a repeatedpower/lifetime pass.

Replay `python calculate.py`. Exact independent priorresult/winding hashes are recorded in results.json. Native sourceregister locations: earlier clamp-study sources (SMBJ160A,US1M), component-study STN1NK80Z DS14259Rev2July2026, and electrical-integration/magnetics. Source originals remain external; this packet adds no vendorpublication. All earlier electrical/model/thermal majors retain their affectedgates.

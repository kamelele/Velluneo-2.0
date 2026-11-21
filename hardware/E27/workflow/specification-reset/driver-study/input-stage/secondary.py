#!/usr/bin/env python3
"""Source-conditioned rectifier and NTC calculations, not a transient/thermal pass."""
import json,math,itertools
ratio=4;bus=253*math.sqrt(2);ovp=37.861 # Existing startup upper25C OVP sensitivity, rounded upward.
ip=.345;dd=.425
avg=ratio*ip*dd/2;rms=ratio*ip*math.sqrt(dd/3)
nomr=.95/105e-6;rtrip=[.9/125e-6,1/90e-6]
def temp(r,r25,beta):return 1/(1/298.15+math.log(r/r25)/beta)-273.15
trips=[temp(r,100000*f,4100*b) for r,f,b in itertools.product(rtrip,[.99,1.01],[.99,1.01])]
print(json.dumps({'study':'VEL-INPUT-01-SECONDARY','date':'2026-11-17','assumptions':{'turns_Np_Ns_Na':[120,30,22],'upper_input_peak_V':bus,'OVP25_upper_rounded_sensitivity_V':ovp,'primary_peak_A_assumed':ip,'demag_duty_assumed':dd,'VDD_upper_example_V':35,'dynamic_spikes_not_bounded':True},'output_candidate':{'MPN':'STTH2R02A','reverse_rating_V':200,'ideal_reverse_V':ovp+bus/4,'ideal_reverse_arithmetic_headroom_V':200-ovp-bus/4,'pulse_peak_A':ratio*ip,'average_triangular_A':avg,'RMS_triangular_A':rms,'source_equation_conduction_estimate_W':.68*avg+.06*rms*rms,'not_recovery_or_temperature_or_physical_loss':True},'aux_candidate':{'MPN':'STTH1R02A','reverse_rating_V':200,'ideal_reverse_at35V_VDD_V':35+bus*22/120,'all_energy_to_aux_initial_current_A_proxy':ip*120/22,'actual_current_sharing_not_verified':True},'NTC_candidate':{'MPN':'NTCS0603E3104FXT','R25_ohm':100000,'R25_tolerance':.01,'B25_85_K':4100,'B_tolerance':.01,'trip_resistance_ohm':rtrip,'nominal_beta_trip_C':temp(nomr,100000,4100),'constant_beta_trip_sensitivity_C':[min(trips),max(trips)],'constant_beta_is_not_guaranteed_full_RT_curve':True,'near_trip_self_heat_K_proxy':1*125e-6/.003,'installed_sensor_lag_unverified':True,'open_sensor_fault':'External thermal cutoff may be lost; do not claim fail-safe coverage','short_sensor_fault':'LowNTC is documented shutdown command; actual fault/restart behavior pending'}},indent=2))

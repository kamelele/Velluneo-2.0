from pathlib import Path
import json,math,itertools,sys,copy
S=Path(__file__).resolve().parent;B=S/'reference'
sys.dont_write_bytecode=True;sys.path.insert(0,str(S));from current_model import screen
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
g=.003;rb=1000.;rh=243000.;rt=320000.
def vc(v,top,bottom,hys,vdrive,ib):return v*(1+top/bottom+top/hys)-vdrive*top/hys+ib*top
def bounds(vs,ds):
 vals=[vc(v,rt*e1,rb*e2,rh*e3,d,ib) for v,e1,e2,e3,d,ib in itertools.product(vs,[1-g,1+g],[1-g,1+g],[1-g,1+g],ds,[-15e-9,15e-9])]
 return [min(vals),max(vals)]
rise=bounds([.396,.404],[0,.5]);fall=bounds([.387,.400],[10.90,12.75]);window=rise[0]-fall[1]
rail=[11.55,12.75];rlo=.99*.97;rhi=1.01*1.03
feed=6*845;feedmin=(fall[0]-rail[1])/(feed*rhi)
# Use ZERO forward voltage on BOTH LEDs as a conservative load upper bound; no invented minVF.
loads={'two_LED_paths_A':2*rail[1]/(1780*rlo),'base_drive_total_A':rail[1]/(11000*rlo),'OPTO_pulldown_A':rail[1]/(47000*rlo),'hysteresis_A':rail[1]/(243000*.997),'rail_divider_A':rail[1]/(48300*.9965),'reference_input_extra_conservative_A':6.5e-6,'comparator_A':13e-6}
loadmax=sum(loads.values());led_min=(rail[0]-.65-1.5)/(1780*rhi);led_short_power=rail[1]**2/(1780*rlo)
colmax=loads['two_LED_paths_A']+loads['OPTO_pulldown_A']+loads['hysteresis_A']
base_min=(rail[0]-.9-.4)/(11000*rhi)-.9/(10000*rlo)
# R20 current must be subtracted from R19 sink current to obtain actual transistor base current.
base_input_min=(rail[0]-.9-.4)/(11000*rhi)
off=(135-rail[0])/(feed*rlo)+2*135/(56000*rlo)+135/(321000*.997)+.00145
toff=120e-6*window/off
nomfeed=(120-12.15)/feed
normalmax=.0605+(123-rail[0])/(feed*rlo)+2*123/(56000*rlo)+123/(321000*.997)+.00145
current=[]
for L,f,ilim,vth in itertools.product([.0024,.0033],[62000.,70000.],[.350,.504],[1.54,1.76]):
 args=dict(R=28.7*(.99 if vth>1.65 else 1.01),L=L,f=f,ilim=ilim,vth=vth,vout=123.,vac=253.,tmin=.675e-6)
 current.append({'inputs':args,'results':screen(**args)})
checks={
 'at_least5mA_each_input_under_explicit_drop_budgets':led_min>=.005,
 'reference_ge1mA_even_zero_VF_conservative_load':feedmin-loadmax>=.001,
 'feed_each_below_HP100C_power_limit':(135-rail[0])**2*(845*rhi)/(845*(rhi+5*rlo))**2<1.5*55/85,
 'LED_input_short_below_HP0805_125C_power_limit':led_short_power<.5*30/85,
 'min_independent_hysteresis_positive':window>0,
 'conditional_retry_upper_below25Hz':1/toff<25,
 'proposed90mA_sufficient_for_total_load_budget':normalmax<=.09,
 'conditional_full10ms_droop_below123V':84.5+.0605*(470*1.05*1.03)+.09*.01/120e-6<123,
 '25C_sense_power_below_HP125C_rating':1.76**2/(28.7*.99)<.75*30/85,
 'conditional_forced_beta_no_more20':colmax/base_min<=20
}
old=json.loads((B/'electrical-calculations.json').read_text(encoding='utf-8'))
r={'revision':'SC07-C','kind':'Calculated targeted design response with explicit conditional budgets, NOT measurement or full safety acceptance',
 'actuator_fault_response':{'LED_open_U4':'R26/U5 and R27 remain a complete driven SOURCE-referenced BP shunt','output_open_U4':'R27/U5 retains same single-path function; do not credit current sharing','LED_open_U5':'R21/U4 and R6 remain complete shunt','output_open_U5':'R6/U4 retains same single-path function','one_LED_short':'Own1.78k resistor prevents shared drive hardshort; load upper bound deliberately assumes bothVFzero','one_output_terminal_short':'Commands persistent driver shutdown through its own100ohm; dark failure, no direct C5 dump','not_covered':['SharedU2/U3/Q2/divider/feed/trace failures','PhotoMOS interterminal insulation failure or arbitrary partialinternalshort','LYT power switch failedshort or loss ofcurrentregulation','Productwide singlefault qualification']},
 'OVP':{'rising_V':rise,'falling_V':fall,'independent_window_min_V':window,'external_hysteresis_R_ohm':243000,'VOPTO_on_budget_V':[10.90,12.75],'meaning':'Recomputed using full-temp comparator thresholds and0.3%perprecisionarm budgets. PNP/rail bounds remain required design conditions.'},
 'auxiliary':{'feed_parts':6,'each_ohm':845,'total_ohm':feed,'exact_grade':'CRCW2512845RFKEGHP1.5W','min_feed_at_worst_falling_threshold_A':feedmin,'max_load_breakdown':loads,'max_load_A':loadmax,'remaining_shunt_A':feedmin-loadmax,'required_operating_shunt_A':.001,'normal120V_feed_A':nomfeed,'previous_normal120V_feed_A':(120-12.075)/10000,'normal120V_aux_input_W':120*nomfeed,'added_normal120V_aux_input_W':120*(nomfeed-(120-12.075)/10000),'each_feed_max135V_W':(135-rail[0])**2*(845*rhi)/(845*(rhi+5*rlo))**2,'each_feed_allowed100C_W':1.5*55/85,'temperature_interpretation':'100C is local ambient for rated dissipation, not achieved resistor body or film temperature. Proper land/thermalboardconditions and actual temperature still need verification.'},
 'input_branches':{'each_R_ohm':1780,'grade':'CRCW08051K78FKEAHP0.5W','LED_min_A':led_min,'LED_max_conservative_zeroVF_A':rail[1]/(1780*rlo),'short_fault_each_W':led_short_power,'HP0805_allowed125C_W':.5*30/85,'original_ordinary0805_allowed125C_W':.125*30/85,'reason_for_HP_change':'Ordinary0805can exceed its hot derated power in an LED-short fault. HPgrade deliberately selected.','PNP_VCE_budget_V':.65,'LED_VFmax_budget_V':1.5,'qualification_limits':'VFmax, PhotoMOSRon/timing andPNP saturation test conditions are not relabelled fulltemperature guarantees.'},
 'Q2_drive':{'R19_ohm':11000,'R20_ohm':10000,'base_feed_min_A':base_input_min,'R20_current_subtracted_base_min_A':base_min,'collector_max_A':colmax,'worst_forced_beta':colmax/base_min,'allowed_budget_VCE_V':.65,'note':'SubtractR20current; 10mA/0.5mAand100mA/5mA25Ctestpoints do not prove a full-temperature saturation bound at new condition. Qualification remains OPEN.'},
 'open_load_retry_conditional':{'max_drain_A':off,'off_interval_min_s':toff,'frequency_upper_Hz':1/toff,'target_Hz':25,'old330k_hysteresis_not_reused':True,'conditions':'Successful surviving-actuator shutdown and statedrail/dropbounds. Includes capacitor leakage. No AC-reset-only behavior is added.'},
 'normal_headroom_conditional':{'load_max_derived_A':normalmax,'proposed_driver_charge_window_max_A':.09,'delivery_window_s':.01,'Cmin_F':120e-6,'full10ms_droop_V':.09*.01/120e-6,'peak_requirement_V':84.5+.0605*(470*1.05*1.03)+.09*.01/120e-6,'peak_limit_V':123,'critical_note':'Full10ms deliverygap is a steadyhealthy-operation ASSUMPTION requiring actualmodel/benchcorrelation.90mAover20msdoesNOTgive thisdroopbound;20msgapwouldrequire130.25VandFAIL. No changeofsiliconlimit silentlyinferred.'},
 'current_seed_and_sensitivity':{'R2_ohm':28.7,'part':'CRCW120628R7FKEAHP','grade_W70C':.75,'nominal_fixed110V':screen(R=28.7),'cases':current,'case_count':len(current),'min_A':min(x['results']['Iout'] for x in current),'max_A':max(x['results']['Iout'] for x in current),'limits':'Ownfixed-output/idealsource/sampleholdmodel,16illustrative25Csensitivitycases; no actualpi,currentfulltempguarantees,reversecurrent,startup,ESR/DCR/nonlinearL,jitter orswitchingloss. NotPIXls. No guarantee90mA.'},
 'samplehold':{'part':'CL21A226MOCLRNC','required_Ceff_F':20/(62000*28.7*.99),'nominal_tol_temp_C_F':22e-6*.8*.85,'allowed_fraction_remaining_after_bias_and_aging_min':(20/(62000*28.7*.99))/(22e-6*.8*.85),'local_temperature_limit_C':85,'status':'OPEN effectiveC/hot qualification. Localboundaryspecified, notmeasured.'},
 'BP_each_surviving_path':dict(old['BP_shutdown'],claim='Each branch independently must satisfy the single-path limit. Two parallel paths are NOT credited for safety or responsebudget.'),
 'passive_discharge_unchanged':old['passive_discharge'],
 'output_energy_and_R7_unchanged':old['output_energy'],
 'RF_temperature_correction':{'TCR_abs_per_K':.0004,'Rmin100C_ohm':220*.95*(1-.0004*75),'Rmin125C_ohm':220*.95*(1-.0004*100),'Rmin155C_ohm':220*.95*(1-.0004*130),'scope':'Explicittemperature-dependentcornerequations,notachievedtemperatures.'},
 'dynamic135V_screen':{'trip_max_V':rise[1],'imposed_Ipeak_A':.7,'imposed_latency_s':.0006,'calculated_peak_V':math.sqrt((rise[1]+.7*.0006/120e-6)**2+.003*.7**2/120e-6),'limit_V':135,'status':'Conditional only; fulltemperaturecurrent/delaybounds missing.'},
 'checks':checks,
 'not_closed':['ActualLYTfulltemperatureIpeak/charge/currentlimit','InputnonlinearL/inrush/reversedrain and windinginsulation','HotTVS+loopovershoot below700V','PhotoMOShotoperation/delay/PNPsaturation/startup','C4effectivecapacitance and localtemperature','Standards/domainagreement and completephysicalfaultqualification']}
save(S/'electrical-checks.json',r)
print(json.dumps({'rise':rise,'fall':fall,'window':window,'shunt_margin_mA_above_required':1000*(feedmin-loadmax-.001),'input_min_mA':led_min*1000,'feed_power_each_W':r['auxiliary']['each_feed_max135V_W'],'base_current_A':base_min,'forced_beta':colmax/base_min,'retry_Hz':1/toff,'headroom_V':r['normal_headroom_conditional']['peak_requirement_V'],'conditional_checks':checks,'sensitivity_mA':[r['current_seed_and_sensitivity']['min_A']*1000,r['current_seed_and_sensitivity']['max_A']*1000]},indent=2))

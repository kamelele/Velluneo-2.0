"""Reproducible controller fault/reset and proposed backup-ECO screens.
No native UCC28711 model, physical measurement or stage approval is inferred.
"""
from pathlib import Path
import argparse,ast,hashlib,itertools,json,math,zipfile
a=argparse.ArgumentParser();a.add_argument('--source-dir',type=Path,required=True);arg=a.parse_args()
D=Path(__file__).resolve().parent;P=D.parent.parent;S=arg.source_dir.resolve()
BASE='ea3b23fced193861c94637524d482b7c0e96d33e'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
register=[]
urls={'slum538.zip':'https://www.ti.com/lit/zip/SLUM538','slum464.zip':'https://www.ti.com/lit/zip/SLUM464','slum539.tsc':'https://www.ti.com/lit/tsc/SLUM539','tmp302.pdf':'https://www.ti.com/lit/ds/symlink/tmp302.pdf','tmp708.pdf':'https://www.ti.com/lit/ds/symlink/tmp708.pdf','tps7a16.pdf':'https://www.ti.com/lit/ds/symlink/tps7a16.pdf','mcp1799.pdf':'https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP1799-Data-Sheet-20006248B.pdf'}
for n,u in urls.items():
 b=(S/n).read_bytes();register.append({'file':n,'url':u,'bytes':len(b),'sha256':h(S/n)})
# The existing source-pinned file is external; require its declared identity.
ti_source=S.parent/'readiness-sources/ucc2871x.pdf';assert h(ti_source)=='762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248'
register.append({'file':'../readiness-sources/ucc2871x.pdf','url':'https://www.ti.com/lit/ds/symlink/ucc28711.pdf','bytes':ti_source.stat().st_size,'sha256':h(ti_source),'pages':[3,4,5,6,9,12]})
native=[]
for archive,member,marker in [('slum538.zip','UCC28710_TINA_TRANS/UCC28710_TRANS.LIB',b'<Encrypted Library>'),('slum464.zip','UCC28710_PSPICE_TRANS/UCC28710.lib',b'**$ENCRYPTED_LIB')]:
 z=zipfile.ZipFile(S/archive);b=z.read(member);assert b.startswith(marker)
 native.append({'archive':archive,'member':member,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'encrypted':True,'visible_model_part':'UCC28710','NTC_UCC28711_model_available':False})
inputs={n:h(P/n) for n in ['schematic-intent/intended-connectivity.json','electrical-integration/proposed-parts.json','pcb-readiness-01/startup-protection/calculate.py','pcb-readiness-01/startup-protection/results-160.json']}
(D/'sources.json').write_text(json.dumps({'base':BASE,'fresh_sources':register,'native_model_inventory':native,'repository_inputs_SHA256':inputs,'no_vendor_publications_or_encrypted_models_redistributed':True},indent=2)+'\n',encoding='utf-8',newline='\n')
Cmax=.94e-6*1.05*1.003;Rmax=1e6*1.021;Rmin=1e6*.979
def discharge(v0,off,ifault,inj):
 eq=Rmax*(inj-ifault)
 if eq>=off:return None
 return Rmax*Cmax*math.log((v0-eq)/(off-eq))
reset=[]
for v0,off,ifr,inj in itertools.product([9,10,19,23,35],[7.7,8.5],[0,95e-6,125e-6],[0,2e-6,5e-6,7e-6,7.5e-6,8e-6,20e-6]):
 reset.append({'initial_VDD_V':v0,'off_threshold_V':off,'uniform_fault_draw_A_hypothesis':ifr,'uniform_injection_A_hypothesis':inj,'time_to_off_s':discharge(v0,off,ifr,inj)})
critical=7.7/Rmax
assert discharge(35,7.7,0,0)>discharge(23,7.7,0,0)>0
assert discharge(35,7.7,0,8e-6) is None
# One-pulse quantities are diagnostics or proposed acceptance ceilings, not actual bounds.
energy=[];Lpmax=.002304*1.1;Coutmin=8e-6
for ip,n in itertools.product([.35852176738964415,.4,.75],[1,3,9,100]):
 E=.5*Lpmax*ip*ip*n
 energy.append({'Ipk_A_assumption':ip,'pulse_count_assumption':n,'stored_energy_train_J':E,'minimum_repeat_interval_s_for0p4W_average_allocation':E/.4,'worst_Vout_from37p4784V_all_energy_to8uF':math.sqrt(37.4784**2+2*E/Coutmin)})
ovp=[]
for rtop,rbot,thr,vf in itertools.product([.979,1.021],[.979,1.021],[4.55,4.71],[0,1.7]):
 ratio=(80600*rtop+17400*rbot)/(17400*rbot);vo=thr*ratio*(30/22)-vf
 ovp.append({'Rtop_factor':rtop,'Rbottom_factor':rbot,'VS_OVP_25C_V':thr,'VF_assumed_V':vf,'static_secondary_V':vo})
# TMP708 formula invert, including explicit extra R tolerance rather than hiding it.
def temp(r_k):return (.9308-math.sqrt(.9308**2-4*.0012*(96.147-r_k)))/(.0024)
tlo=temp(25.5*1.021)-3;thi=temp(25.5*.979)+3;tnom=temp(25.5)
assert 80<tlo<tnom<thi<90
bleed_min=4.9/(475e3*1.021);bleed_max=5.1/(475e3*.979)
assert bleed_min>=10e-6
backup={'part':'TMP708AIDBVR','regulator':'TPS7A1650DGNR','Rset_ohm':25500,'Rset_initial_tolerance':.01,'Rset_total_temperature_screen_fraction':.021,'formula_nominal_trip_C':tnom,'device_error_plus_extra_resistor_screen_C':[tlo,thi],'hysteresis_nominal_C':10,'hysteresis_min_max_guarantee_available':False,'proposed_additional_bias_screen_A':85e-6,'bias_screen_is_not_full_device_model_or_uniform_max_current_guarantee':True,'LDO_bleeder_475k_min_load_A':bleed_min,'LDO_bleeder_475k_max_load_A':bleed_max,'latest_trip_gradient_plus_lag_budget_to105C_K':105-thi,'earliest_trip_above70C_target_K':tlo-70,'OT_absmax_V':6,'UCC_NTC_absmax_V':5,'OT_min_sink_at0p3V_A':.005,'UCC_NTC_max_source_at25V_A':125e-6,'required_Cout_effective_min_F':2.2e-6,'Cout_nominal_F':4.7e-6,'Cout_plus_bypass_upper_F':6.10e-6}
# Extract only pure, source-pinned functions. Top-level old output writes never run.
oldsource=(P/'pcb-readiness-01/startup-protection/calculate.py').read_text()
assert oldsource.count('base=.0035;')==1
edited=oldsource.replace('base=.0035;','base=.0035+cfg.get("extra_bias_A",0.);')
tree=ast.parse(edited);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
prior=json.loads((P/'pcb-readiness-01/startup-protection/results-160.json').read_text());cases=prior['behavioral_model']['cases'][:64];worst=min(cases,key=lambda x:x['VDD_min_V'])
ns={'math':math,'NPS':4.,'NAS':22/30,'R13':979000.,'RBLEED':9790.,'wr':prior['hot_winding_R_ohm']}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'source_pinned_pure_functions','exec'),ns)
start=[]
for extra,steps in itertools.product([0.,85e-6],[160,320]):
 cfg=worst['config'].copy();cfg['extra_bias_A']=extra;r=ns['trajectory'](cfg,steps);r.pop('trace',None);start.append(r)
assert abs(start[0]['VDD_min_V']-worst['VDD_min_V'])<1e-9
# Ideal source-port charge bookkeeping, NOT a measured/native HV I-V law.
def poweron(ihv,extra):
 # At3V assume auxiliary electronics starts drawing; regulator tracking earlier
 # is only an explicit mathematical charge allocation, not TPS startup waveform.
 segments=[(0,.5,Cmax,False),(.5,3,Cmax+6.10e-6,False),(3,5.6,Cmax+6.10e-6,True),(5.6,19,Cmax,True)]
 total_t=0.;Qhv=Qload=Qres=Qstore=0.;Esource=Eloads=Estoredport=0.;rows=[]
 for lo,hi,cap,on in segments:
  draw=30e-6+(extra if on else 0);i=ihv-draw
  if i*Rmin<=hi:return {'IHV_A_hypothesis':ihv,'extra_bias_A_hypothesis':extra,'reaches19V':False,'stall_or_unreachable_segment_V':[lo,hi],'equilibrium_V':i*Rmin,'time_before_failed_segment_s':total_t,'uniform_source_values_not_guaranteed_by_TI':True}
  dt=Rmin*cap*math.log((i*Rmin-lo)/(i*Rmin-hi));q=cap*(hi-lo);qr=i*dt-q;vdt=Rmin*qr;v2dt=Rmin*(i*vdt-.5*cap*(hi*hi-lo*lo))
  Qhv+=ihv*dt;Qload+=draw*dt;Qres+=qr;Qstore+=q
  Esource+=ihv*vdt;Eloads+=draw*vdt+v2dt/Rmin;Estoredport+=.5*cap*(hi*hi-lo*lo)
  rows.append({'VDD_segment_V':[lo,hi],'effective_charge_capacitance_F':cap,'duration_s':dt,'backup_bias_applied':on});total_t+=dt
 assert abs(Qhv-Qload-Qres-Qstore)<1e-16
 assert abs(Esource-Eloads-Estoredport)<1e-12
 # cap-input charge includes the linear-regulator charge transfer, not just energy.
 return {'IHV_A_hypothesis':ihv,'extra_bias_A_hypothesis':extra,'reaches19V':True,'time_s':total_t,'segments':rows,'source_charge_C':Qhv,'load_charge_C':Qload,'R13_charge_C':Qres,'capacitor_charge_port_C':Qstore,'charge_residual_C':Qhv-Qload-Qres-Qstore,'VDD_port_energy_residual_J':Esource-Eloads-Estoredport,'regulator_output_capacitor_energy_at5p1V_J':.5*6.10e-6*5.1**2,'capacitor_charge_port_energy_J':Estoredport,'uniform_source_values_not_guaranteed_by_TI':True}
charge=[poweron(i,85e-6) for i in [100e-6,250e-6,500e-6]]
out={'base':BASE,'scope':'Executed source-conditioned reset/energy/charge and behavioral coupled-startup diagnostics; NOT functional native-controller or physical proof','reset':{'case_count':len(reset),'rows':reset,'passive_no_injection_35_to7p7_upper_s':discharge(35,7.7,0,0),'max_constant_injection_for_passive_reset_A_strictly_less_than':critical,'guarantee_conditions':['R13 remains intact within its selected tolerance; CDD<=stated maximum.','Fault has actually stopped switching; all other VDD loads are passive.','External/auxiliary injected current is zero for no-injection upper bound, or below the explicitly selected uniform bound.','IFAULT95/125uA entries used uniformly are sensitivities; TI specifies atVDD25V. No IRUN/IFAULT minimum is invented.'],'R13open':'Without a positive lower bound on actual internal discharge current, this passive reset proof is lost.'},'fault_energy_screens':energy,'static_OVP_25C_screens':ovp,'backup_ECO_candidate':backup,'matched_old_worst_startup_comparisons':start,'new_global_worst_corner_claim':False,'initial_output_capacitor_charge_sensitivity':charge,'limitations':['Official available encrypted model is28710 and CBC is not modeled; no28711NTC native model is supplied.','ActualHV I-V over the charging trajectory and controller states is not specified by100/250/500uA atVDD0. Fixed100uA stall is a diagnostic, not established actual failure.','Backup supply power-up/reset/output-off leakage, regulator dynamic input current and capacitor effective bias/temperature/ESR must be established before ECO acceptance.','Pulse count and Ipk assumptions are not measured or guaranteed dynamic fault maxima; no11W fault power cap is used.']}
(D/'results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
summary={'reset_cases':len(reset),'passive_35_to7p7_upper_s':out['reset']['passive_no_injection_35_to7p7_upper_s'],'injection_ceiling_uA':critical*1e6,'backup_trip_C':[tlo,tnom,thi],'startup_min_VDD_by_extra_steps':[(x['config']['extra_bias_A'],x['integration_steps_per_demag'],x['VDD_min_V']) for x in start],'charge_sensitivities':charge}
print(json.dumps(summary,indent=2))

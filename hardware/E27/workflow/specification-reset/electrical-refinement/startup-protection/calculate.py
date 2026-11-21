"""ELEC-REFINE-02 finite-resistance/source envelope; no controller simulation."""
from pathlib import Path
import math,json,hashlib,itertools
from scipy.integrate import quad
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir',type=Path,required=True,help='External nativePDF directory; originals are not redistributed.')
parser.add_argument('--ucc-pdf',type=Path,help='Optional separate UCCPDF location.')
parser.add_argument('--diode-source-dir',type=Path,help='Optional separate directory for stth1r02.pdf/stth2r02.pdf.')
args=parser.parse_args()
B=P.parents[1]
register=json.loads((P/'sources.json').read_text())
sha={}
for entry in register['primary_sources']:
 filename=entry['filename']
 if filename=='ucc2871x.pdf' and args.ucc_pdf:path=args.ucc_pdf
 elif filename.startswith('stth') and args.diode_source_dir:path=args.diode_source_dir/filename
 else:path=args.source_dir/filename
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest!=entry['sha256']:raise ValueError('Native source hash differs: '+filename)
 sha['native/'+filename]=digest
for entry in register['repository_inputs']:
 digest=hashlib.sha256((B/entry['path']).read_bytes()).hexdigest()
 if digest!=entry['sha256']:raise ValueError('Repository input hash differs: '+entry['path'])
 sha[entry['path']]=digest
mag=json.loads((B/'electrical-integration/magnetics/winding-results.json').read_text())
hot=next(x for x in mag['loss_cases'] if x['MLT_mm']==60 and x['temperature_C']==125)
wr={x['winding']:x['R_ohm'] for x in hot['windings']}
rp,ra,rs=wr['P'],wr['A'],wr['S']
n=4;nas=22/30;npa=120/22;Raux=4.7*1.021;Rpath=ra+Raux
Cdd=.890321e-6;Cmax=.989961e-6;Cout=20.592e-6;draw=.0035;Qg=16e-9;R13min=979000;R13max=1021000;IR13=35/R13min;Ib=draw+IR13
freq=106000;Ibpeak=Ib+Qg*freq
factors=[.979,1.021];Icc=.318*4*.85/(2*2.37*1.021)
fcoef=max(vcc*4*2.37*rf/(.002304*lf*vcs*vcs) for vcc,rf,lf,vcs in itertools.product([.318,.343],factors,[.9,1.1],[.738,.810]))
vt=8.617333262145e-5*298.15

def led(v):
 def residual(i):return 7*(1.5601*vt*math.log1p(i/9.8487e-31)+.86341*i-.3)-v
 return 0 if residual(1e-16)>0 else brentq(residual,1e-16,2,xtol=1e-15)
def current(v):return Icc-led(v)-v/(10000*.979)
veq=brentq(current,16,20)
avail=Cdd*9;fixed=Ib*3/92000+3*Qg+.0001*(Ib+Qg*106000)
def charge(v):return quad(lambda x:(Ib+Qg*fcoef*(x+1.2))*Cout/current(x),0,v,epsabs=1e-13)[0]
def ramp(v):
 if v>=veq:return {'reaches_in_inherited_CC_witness':False,'CC_equilibrium_output':veq}
 q=charge(v);t=quad(lambda x:Cout/current(x),0,v,epsabs=1e-12)[0]
 return {'reaches_in_inherited_CC_witness':True,'ramp_time':t,'ramp_charge':q,'VDD_at_takeover':19-(q+fixed)/Cdd,'above10V':q+fixed<=avail}
maxvo=brentq(lambda v:charge(v)+fixed-avail,16,veq-1e-5)
scenarios=[]
for raux,delta,voutdiode_min,vauxmax in itertools.product([4.7,2.2,1.0],[.425,.1,.05,.02],[0,.5],[1,1.2]):
 ia=Ibpeak/delta;path=ra+raux*1.021;drop=ia*path
 takeover=(10+vauxmax+.5+drop)/nas-voutdiode_min
 scenarios.append({'RAUX_nom':raux,'charge_fraction_RECTANGULAR_HYPOTHESIS':delta,'mean_pulse_current_HYPOTHESIS':ia,'VFout_min_assumed':voutdiode_min,'VFaux_max_assumed':vauxmax,'hot_path_ohm':path,'path_drop':drop,'takeover_output':takeover,**ramp(takeover)})
# Source25CstaticOVP, zeroDoutdrop andzeroIs duringsample conservativelymaximizeVo.
ovp=[]
for top,bottom,bias,th,ia,isec in itertools.product(factors,factors,[-.25e-6,.25e-6],[4.55,4.71],[0,.05,.1,.2,.5,1.0,1.9555732766707863],[0]):
 r1=80600*top;r2=17400*bottom;k=r2/(r1+r2);rt=r1*r2/(r1+r2)
 va=(th+bias*rt)/k
 vo=(va+ia*ra)/nas-isec*rs
 ovp.append({'Rtop':r1,'Rbottom':r2,'bias':bias,'VOVP_25C':th,'Ia_sample_assumed':ia,'Is_sample_assumed':isec,'Va_raw_threshold':va,'Vo_threshold_withVFout0':vo})
baseovp=max(x['Vo_threshold_withVFout0'] for x in ovp if x['Ia_sample_assumed']==0)
ia40=(40-baseovp)*nas/ra
# Normal/shortsource: allmagnetizingcurrenttosecondary is deliberately anupperIsillustration.
short=[]
for vcs in [.81,1.6]:
 ip=vcs/(2.37*.979);isec=4*ip;ea=nas*(1.2+isec*rs)
 short.append({'CS_threshold':vcs,'primary_I_ignoring_delay':ip,'all_secondary_peak':isec,'aux_emf_if_Vout0_and_VFout1p2':ea,'below_min_runVDD8p5':ea<8.5})
# PassiveVDDreset assumingauxHVsourcesoff; IFAULT addsdischarge butno minimum is assumed.
reset={'R13max':R13max,'Cddmax':Cmax,'35to7p7_passive_s':R13max*Cmax*math.log(35/7.7),'23to7p7_passive_s':R13max*Cmax*math.log(23/7.7),'19to8p5_RUN3p5_plusR13_s':R13max*Cdd*math.log((19+draw*R13max)/(8.5+draw*R13max)),'source_off_condition_required':True}
startupcharge=[]
for ihv,istart,von in itertools.product([100e-6,250e-6],[18e-6,30e-6],[19,23]):
 i=ihv-istart;eq=i*R13min
 startupcharge.append({'constant_IHV_assumed':ihv,'constant_ISTART_assumed':istart,'VDDon':von,'fixed_point':eq,'charge_time_s_if_currents_hold':-R13min*Cmax*math.log(1-von/eq),'endpoint_source_specs_not_fulltrajectory_guarantee':True})
# ExactRLonrisewithfiniteRp, selectedRDSon onlya sensitivityat25Cnot125Cbound.
on=[]
for bus,lf,rf,vcs,Rmos in itertools.product([240,253*math.sqrt(2)],[.9,1.1],factors,[.215,.81],[16,32,48]):
 lp=.002304*lf;r=rp+2.37*rf+Rmos;ip=vcs/(2.37*rf)
 ton=-lp/r*math.log1p(-ip*r/bus)
 on.append({'bus':bus,'Lp':lp,'Rcs':2.37*rf,'VCS':vcs,'Rmos_assumed':Rmos,'ton_RL':ton})
# Openload: minimumcurrent/frequencyenergy is belowactual10kbleedpowerin30Vrange.
emax=.5*(.002304*1.1)*(.215/(2.37*.979))**2
out={'scope':'Finite-resistanceanalytical envelope/hypotheses, not a TIcontroller/fullconverter/thermalmodel','baseline_commit_from_task':'36ad2f243d36d592228304b26c27188da0d46c4d','input_SHA256':sha,'proposed_hot_R_at125C_60mm':{'Rp':rp,'Ra':ra,'Rs':rs,'source':'parent magnetics proposal, not measured'},'active_R13':{'nominal':1e6,'minimum':R13min,'maximum':R13max,'extra35Vdraw':IR13},'native_CC_formula':'IOCC=VCCR*Nps*eta_XFMR/(2Rcs); eta_XFMR includescore/winding/leakage/bias, notarbitraryoverallconverterefficiency','aux_equation':'VDD=Na/Ns*(Vo+VFout+Is*Rs)-VFaux-Ia*(Ra+RAUX); ignorepositiveIsRsforlowerVDD','hot_aux_path_Rmax':Rpath,'old16p272_target_combined0p8drop_current':.8/Rpath,'old16p272_target_zeroVFout_drop_current':((16.272727272727273*nas)-(10+1+.5))/Rpath,'full_mean_bias_budget':Ibpeak,'original_target':{'Vo':16.272727272727273,**ramp(16.272727272727273)},'zero_VFout_old_reserves_target':{'Vo':16.772727272727273,**ramp(16.772727272727273)},'minimum_charge_fraction_for0p8_combined_drop':Ibpeak/(.8/Rpath),'conditional_charge_limited_takeover_Vo':maxvo,'RAUX_nom_max_vs_rectangular_chargefraction_given_charge_limit':{str(d):((maxvo*nas-11.5)*d/Ibpeak-ra)/1.021 for d in [.02,.05,.1]},'scenarios':scenarios,'OVP25C_baseline_zeroDout_zeroIa':baseovp,'OVP25C_NONCOINCIDENT_global_peak_current_sensitivity':max(x['Vo_threshold_withVFout0'] for x in ovp),'Ia_at_sample_to_keep_staticOVPthreshold_le40_IFotherassumptions':ia40,'OVP_conditions':'25Cthresholds; Ia_sample=1.9556A is an explicit NONCOINCIDENTglobalpeak sensitivity, NOTactualsamplecurrent or physicallycoincidentcorner/guaranteedOVPbound; nearsecondaryendsampleandauxconductionmustbeestablished; no dynamic/tempstop-latency/ringing ceiling;40Visillustrationnotguarantee','short_aux_emf_witnesses':short,'secondary_current_required_for8p5V_aux_emf_atshort_VFout1p2':(8.5/nas-1.2)/rs,'VDD_reset_witness':reset,'constant_HV_current_charge_sensitivities':startupcharge,'line_sense_min_current_withRpIp0p36_and_VSclamp0p325':((240-.36*rp)*22/120-.325)/(80600*1.021),'onrise_RL_witness':{'max_first_min_current_ton':max(x['ton_RL'] for x in on if x['VCS']==.215),'max_normal_ton':max(x['ton_RL'] for x in on if x['VCS']==.81),'Rmos16_32_48_not_guaranteed_hot_limits':True},'aux_cycle_charge_frontier':{'required_charge_at106k_HYPOTHESIS':Ib/freq+Qg,'mean_bias':Ibpeak,'flat_fraction_to_meet10Vcharge_limit_VFaux1':Ibpeak*Rpath/(maxvo*nas-11.5),'flat_fraction_to_meet10Vcharge_limit_VFaux1p2':Ibpeak*Rpath/(maxvo*nas-11.7),'peak_or_sample_Ia_not_bounded_by_mean_duty':True},'openload_min_energy_proxy':{'f_required_if_minpulse_energy_and_nootherloss':(30**2/(10000*1.021))/emax,'VDD_hold_droop_ifallRUN_at_that_frequency':(Ib/((30**2/(10000*1.021))/emax)+Qg)/Cdd,'not_actualCV_frequency_orbiasstate':True,'max_minpulse_energy':emax,'times_fmin_max755_power':emax*755,'bleed_power30V_atRmax':30**2/(10000*1.021),'not_control_or_OVP_pass':True},'no_shared_changes':True,'not_measured_not_selfclosed':True}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

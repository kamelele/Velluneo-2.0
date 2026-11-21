"""ELEC-CLOSE-01 startup audit. Analytical hypotheses; not an IC simulation."""
from pathlib import Path
import math,itertools,json,hashlib
from scipy.integrate import quad
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir',required=True,type=Path,help='External directory containing sluaac5.pdf, slua783.pdf and ucc2871x.pdf (PDFs are not redistributed).')
parser.add_argument('--ucc-pdf',type=Path,help='Optional override for the external ucc2871x.pdf location.')
args=parser.parse_args()
base=P.parents[1]
source_dir=args.source_dir.resolve()
register=json.loads((P/'sources.json').read_text())
sha={}
for entry in register['primary_sources']:
 path=(args.ucc_pdf.resolve() if entry['filename']=='ucc2871x.pdf' and args.ucc_pdf else source_dir/entry['filename'])
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual!=entry['sha256']:
  raise ValueError(f"Native source hash differs: {entry['filename']}: {actual}")
 sha['native/'+entry['filename']]=actual
for rel in ['requirements.json','requirements-and-plan.md','finalization/support-study.md','finalization/support-results.json']:
 sha[rel]=hashlib.sha256((base/rel).read_bytes()).hexdigest()
source=json.loads((base/'finalization/support-results.json').read_text())
Cdd=.890321e-6;Vstart=19;Vtarget=10;Qavail=Cdd*(Vstart-Vtarget)
nps=4;nas=22/30;factors=[.979,1.021]
Icc=.318*nps*.85/(2*2.37*1.021)
Vtake=(10+1+.5+.5+.3)/nas-.5
fcoef=max(vcc*nps*2.37*rf/(.002304*lf*vcs*vcs) for vcc,rf,lf,vcs in itertools.product([.318,.343],factors,[.9,1.1],[.738,.810]))
vt=8.617333262145e-5*298.15

def led(v,n,shift):
 def f(i):return n*(1.5601*vt*math.log1p(i/9.8487e-31)+.86341*i+shift)-v
 return 0 if f(1e-16)>0 else brentq(f,1e-16,.48,xtol=1e-15)
rows=[]
for cap,esr,n,shift,qg,draw in itertools.product([4.032e-6,12e-6,17.16e-6,20.592e-6],[0,.24],[7,8],[0,-.3],[12e-9,16e-9],[.0032,.0035]):
 def cur(v):return Icc-led(v,n,shift)-v/(10000*.979)
 vc=Vtake-esr*cur(Vtake)
 def rates(v):
  vo=v if esr==0 else brentq(lambda vo:vo-v-esr*cur(vo),v,v+esr*Icc)
  return cur(vo),fcoef*(vo+1.2)
 t=quad(lambda v:cap/rates(v)[0],0,vc,epsabs=1e-12)[0]
 q=quad(lambda v:(draw+qg*rates(v)[1])*cap/rates(v)[0],0,vc,epsabs=1e-13)[0]
 qpost=.0001*(draw+qg*106000)+3*qg
 tlim=(Qavail-q-qpost)/draw
 row={'Cout':cap,'ESR':esr,'LEDs':n,'LEDshift':shift,'Qg':qg,'base_draw':draw,'ramp_time':t,'ramp_charge':q,'settling_and_first3_gate_charge':qpost,'first3_allowance':tlim,'source_cadence_witness_t3':3/92000,'VDD_if_3periods_at_slowest_fSWmax':Vstart-(q+qpost+draw*3/92000)/Cdd,'VDD_if_t3_0p3ms':Vstart-(q+qpost+draw*.0003)/Cdd}
 rows.append(row)
worst=min(rows,key=lambda r:r['first3_allowance'])
assert abs(worst['first3_allowance']-source['stress_min_first3_time_s_proxy'])<1e-12
assert abs(Vtake-source['aux_takeover_output_target_V_proxy'])<1e-12
# Native SLUA783 firston-time screen, not propagation/gate/demag timing guarantee.
on=[]
for bus,lf,rf,vcs in itertools.product([240,253*math.sqrt(2)],[.9,1.1],factors,[.175,.215]):
 lp=.002304*lf;ip=vcs/(2.37*rf);ton=lp*ip/bus
 on.append({'bus':bus,'Lp':lp,'Rcs':2.37*rf,'VCSTmin':vcs,'Ip':ip,'ideal_ton':ton})
# Zero-load isolated LC energy-transfer diagnostic, fullyreset beforeeach pulse.
# It demonstrates why fSWmax alone is not proof of actual percycle completion.
reset=[]
for cap,lf,rf,vcs,vd in itertools.product([4.032e-6,12e-6,20.592e-6],[.9,1.1],factors,[.175,.215],[.5,1.2]):
 lp=.002304*lf;ls=lp/16;ip=vcs/(2.37*rf);isec=4*ip;vo=0.;times=[]
 for k in range(3):
  tdm=math.sqrt(ls*cap)*math.atan(isec*math.sqrt(ls/cap)/(vo+vd))
  vo=math.sqrt((vo+vd)**2+ls*isec**2/cap)-vd
  times.append(tdm)
 reset.append({'Cout':cap,'Lp':lp,'Ip_first':ip,'Vdiode_assumed':vd,'individual_demag':times,'sum_demag':sum(times),'Vo_after3_ideal':vo,'first_pulse_demag':times[0]})
# Conditionalwhole-startup current/gate-charge frontier at sourceintendedcadence.
for x in rows:
 N_ramp=(x['ramp_charge']-x['base_draw']*x['ramp_time'])/x['Qg']
 Ntot=N_ramp+106000*.0001+3
 Ttot=x['ramp_time']+.0001+3/92000
 x['source_cadence_total_base_time']=Ttot;x['total_gate_events_proxy']=Ntot
 x['base_max_if_Qg16nC']=(Qavail-16e-9*Ntot)/Ttot
 x['Qg_max_if_base3p5mA']=(Qavail-.0035*Ttot)/Ntot
# Timing-free firstthree chargecondition:120*T +2530*R +ancillary =uC whenT/R inseconds.
residual=Qavail-worst['ramp_charge']-worst['settling_and_first3_gate_charge']
# Extra continuous budget beyond2.65mAIRUN is not a source guarantee.
anc=worst['base_draw']-.00265
capchoices=[]
for maxcap in [12e-6,14.4e-6,20.592e-6,20.592e-6*.47]:
 scale=maxcap/worst['Cout'];qr=worst['ramp_charge']*scale
 capchoices.append({'Cout_max':maxcap,'ramp_time_if_same_rates':worst['ramp_time']*scale,'first3_allrun_allowance':(Qavail-qr-worst['settling_and_first3_gate_charge'])/worst['base_draw'],'conditional_only_no_newpart_or_ripple_acceptance':True})
# A passive resistor that alone supportsfullVDDbudget independentT3 is thermallycostly.
full=.0035+16e-9*106000
Rmax=(240-23)/full;Phigh=(253*math.sqrt(2)-23)**2/Rmax
r={'purpose':'Analytical/sourcewitness, not controller/model/measurement pass','input_SHA256':sha,'first3_source_witness':'SLUAAC5p5 says3pulses atfSWmax; familyincludesUCC28711p2; parametersdifferp3. No guaranteedUVLOtofirstedge/waitextension specified.','Q_available_to10V':Qavail,'Q_available_to8p5V':Cdd*(19-8.5),'Vtake':Vtake,'cases':len(rows),'worst_case':worst,'main_min_allowance':min(x['first3_allowance'] for x in rows if x['base_draw']==.0032 and x['Qg']==12e-9),'source_cadence_witness_worst_VDD':min(x['VDD_if_3periods_at_slowest_fSWmax'] for x in rows),'native_first_on_time_fault_period_fastest':1/106000,'ideal_firston_range':[min(x['ideal_ton'] for x in on),max(x['ideal_ton'] for x in on)],'worst_firston':max(on,key=lambda x:x['ideal_ton']),'ideal_demag_range':[min(x['first_pulse_demag'] for x in reset),max(x['first_pulse_demag'] for x in reset)],'longest_first_demag':max(reset,key=lambda x:x['first_pulse_demag']),'three_fullyreset_demag_sum_max':max(x['sum_demag'] for x in reset),'residual_first3_total_bias_charge_budget':residual,'source_cadence_frontier':{'minimum_constant_base_allowance_if16nC':min(x['base_max_if_Qg16nC'] for x in rows),'minimum_Qg_allowance_if3p5mA':min(x['Qg_max_if_base3p5mA'] for x in rows),'worst_total_base_time':worst['source_cadence_total_base_time'],'worst_total_gate_events_proxy':worst['total_gate_events_proxy'],'extra_unmodelled_charge_allowance':Qavail-worst['ramp_charge']-worst['settling_and_first3_gate_charge']-.0035*3/92000,'condition':'Ibase*Ttotal+Qg*Nequivalent+Qextra<=8.012889uC; physicaltiming/current/rampboundsnotyetguaranteed'},'first3_envelope_A_times_seconds':{'Iwait':.00012,'Irun_minus_wait':.00253,'ancillary_extra':anc,'condition':'(Iwait+ancillary_extra)*Ttotal + (Irun-Iwait)*Trun <= residual; first3gatealreadyallocated; sourcecurrentsonly25Vconditions'},'capacitance_candidates':capchoices,'timing_independent_passive_feed':{'required_mean_bias':full,'R_max':Rmax,'loss_at_highline_withVDD23':Phigh,'rejected_as_default':'~2.7Wconstantloss is poor fit to6-10Wlamp; not aselectedchange'},'remaining_exact_bounds':['maximum netstartupbiascharge or actualstartupcurrentenvelope across9-23V','UVLOon-tofirstpulse latency + any startupclock/demag/waitextension','actualMOSgatechargeatdrive','minimumoutputchargingcurrentandauxtransferbounds atlowVo'],'no_shared_changes':True}
# OptionalUNAPPROVEDECO,RVDD1Mohm acrossVDD, conservative35Vmaxdraw.
eco_i=35/(1e6*.979);eco=[]
for x in rows:
 newbase=x['base_draw']+eco_i;qr=x['ramp_charge']+eco_i*x['ramp_time'];qp=x['settling_and_first3_gate_charge']+eco_i*.0001
 eco.append({'original_base':x['base_draw'],'original_Qg':x['Qg'],'VDD_sourcecadence':19-(qr+qp+newbase*3/92000)/Cdd,'VDD_0p3ms':19-(qr+qp+newbase*.0003)/Cdd,'first3_limit':(Qavail-qr-qp)/newbase})
r['optional_UNAPPROVED_RVDD_ECO']={'Rnom':1e6,'Rmin':1e6*.979,'voltage_for_extra_draw':35,'extra_draw':eco_i,'worst_source_cadence_VDD':min(x['VDD_sourcecadence'] for x in eco),'worst_0p3ms_VDD':min(x['VDD_0p3ms'] for x in eco),'stress_min_first3_allowance':min(x['first3_limit'] for x in eco),'main_min_first3_allowance':min(x['first3_limit'] for x in eco if x['original_base']==.0032 and x['original_Qg']==12e-9),'not_folded_into_approved_baseline':True}
(P/'results.json').write_text(json.dumps(r,indent=2)+'\n');(P/'rows.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(r,indent=2))

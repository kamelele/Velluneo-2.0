"""ECO22 startup-feed comparisons. Stdlib only; NOT a controller transient model.
Run: python calculate.py. Only results.json beside this script is written.
"""
from pathlib import Path
import hashlib,itertools,json,math

D=Path(__file__).resolve().parent
DESIGNS={
 'C16':dict(R16_R17_each_ohm=402000.,R13_ohm=80600.,Rstart_fraction=.021,R13_fraction=.021),
 'ECO22':dict(R16_R17_each_ohm=422000.,R13_ohm=84500.,Rstart_fraction=.021,R13_fraction=.0065),
 'rejected_2x':dict(R16_R17_each_ohm=806000.,R13_ohm=162000.,Rstart_fraction=.021,R13_fraction=.021)}

def dc_cases(d):
 rows=[]
 for vac,rf,bf,cf,leak,drop in itertools.product([207.,253.],[-1,1],[-1,1],[.95,1.05],[3e-6,20e-6],[0.,5.]):
  rs=2*d['R16_R17_each_ohm']*(1+rf*d['Rstart_fraction'])
  rb=d['R13_ohm']*(1+bf*d['R13_fraction']);cap=.94e-6*cf
  bulk=vac*math.sqrt(2)-drop;rp=1/(1/rs+1/rb)
  inf=rp*(bulk/rs-1.5e-6-leak)
  t=-rp*cap*math.log1p(-23/inf) if inf>23 else None
  rows.append(dict(Vac=vac,bulk_drop_V=drop,Rstart_ohm=rs,R13_ohm=rb,
   Cdd_F=cap,D2_leak_A=leak,TI_start_A=1.5e-6,equilibrium_V=inf,
   net_current_at23_A=(bulk-23)/rs-23/rb-1.5e-6-leak,
   reaches23=t is not None,time_to23_s=t))
 return rows

def witness(d,hz,phase,ramp,cb,dt=1e-5,worst_resistors=True):
 """Coupled ideal-sine rectifier/Cbulk/Cdd midpoint witness to FIRST UVLO23V.
 No switching, gate load, active control, optical startup or fault recovery.
 """
 rs=2*d['R16_R17_each_ohm']*(1+d['Rstart_fraction'] if worst_resistors else 1)
 rb=d['R13_ohm']*(1-d['R13_fraction'] if worst_resistors else 1)
 cdd=.94e-6*1.05;v=0.;w=0.;series=47*1.05+6.;bleed=499000*.979
 def deriv(t,v,w):
  amp=min(1.,t/ramp) if ramp else 1.
  src=max(0.,207*math.sqrt(2)*amp*abs(math.sin(2*math.pi*hz*t+phase))-2.)
  ib=max(0.,(src-v)/series);ist=(v-w)/rs
  return (ib-v/bleed-ist-246.5e-6)/cb,(ist-w/rb-21.5e-6)/cdd
 for k in range(round(1/dt)):
  t=k*dt;dv,dw=deriv(t,v,w)
  vm=max(0.,v+.5*dt*dv);wm=max(0.,w+.5*dt*dw)
  dv,dw=deriv(t+.5*dt,vm,wm);v=max(0.,v+dt*dv);w=max(0.,w+dt*dw)
  if w>=23:
   return dict(hz=hz,phase_rad=phase,amplitude_ramp_s=ramp,Cbulk_F=cb,
    dt_s=dt,worst_resistor_corners=worst_resistors,reaches23=True,
    time_to23_s=t+dt,bulk_at23_V=v)
 return dict(hz=hz,phase_rad=phase,amplitude_ramp_s=ramp,Cbulk_F=cb,
   dt_s=dt,worst_resistor_corners=worst_resistors,reaches23=False,time_to23_s=None)

def bounds(d):
 rs=2*d['R16_R17_each_ohm'];rb=d['R13_ohm']
 rsmin=rs*(1-d['Rstart_fraction']);rsmax=rs*(1+d['Rstart_fraction'])
 rbmin=rb*(1-d['R13_fraction']);rbmax=rb*(1+d['R13_fraction'])
 bulk=253*math.sqrt(2);rparmax=1/(1/rsmax+1/rbmax)
 # Zero-positive-startup-feed hold-up lower screen ignores available feed in BOTH.
 # Full-time RUN/gate/current assumptions are deliberately additive sensitivities.
 cmin=.94e-6*.95;gate=20e-9*140000;pulldown=10/47000
 ihold=.00265+gate+pulldown+23/rbmin
 # A hypothetical single short in one startup resistor puts the full bus on the
 # other. This checks its voltage/power only; it is NOT a full single-fault pass.
 lone=d['R16_R17_each_ohm']*(1-d['Rstart_fraction'])
 vbus=310.36319233213163;vdd=11.131062002740011
 return dict(
  startup_feed_only_normal_line_zero_controller_draw_ceiling_V=bulk*rbmax/(rsmin+rbmax),
  net_feed_at35V_A=(bulk-35)/rsmin-35/rbmax,
  minimum_required_OTHER_sink_at8p45_highline_A=(bulk-8.45)/rsmin-8.45/rbmax,
  R13_max_heat_at35_W=35**2/rbmin,
  passive_forced_bulk0_Cmax_Rmax_35to8p45_s=rparmax*.94e-6*1.05*math.log(35/8.45),
  passive_forced_bulk0_Cmax_Rmax_35to5_s=rparmax*.94e-6*1.05*math.log(35/5),
  hold_screen_Cmin_F=cmin,hold_screen_load_A=ihold,
  hold_screen_assumptions=dict(IRUN_A=.00265,Qg_C=20e-9,fs_Hz=140000,
   gate_pulldown_A=pulldown,R13_current_bound_23V_A=23/rbmin,positive_startup_feed_credit_A=0.),
  no_positive_feed_hold_lower_19to8p45_s=cmin*(19-8.45)/ihold,
  no_positive_feed_hold_lower_19to9p45_s=cmin*(19-9.45)/ihold,
  single_startup_resistor_short_other_resistor_voltage_screen_V=bulk,
  single_startup_resistor_short_other_heat_atVDD0_W=bulk**2/lone,
  retained_CRCW2512_Umax_V=500.,retained_CRCW2512_P125_screen_W=(155-125)/(155-70),
  nominal_startup_resistor_heat_W=(vbus-vdd)**2/rs,
  nominal_startup_branch_input_W=(vbus-vdd)*vbus/rs,
  nominal_R13_heat_W=vdd*vdd/rb,
  nominal_net_startup_feed_after_R13_A=(vbus-vdd)/rs-vdd/rb)

def main():
 dc={k:dc_cases(d) for k,d in DESIGNS.items()}
 summary={k:dict(count=len(rows),failed_cases=sum(not x['reaches23']for x in rows),
  minimum_equilibrium_V=min(x['equilibrium_V']for x in rows),
  minimum_current_at23_A=min(x['net_current_at23_A']for x in rows),
  worst_time_to23_s=max(x['time_to23_s']for x in rows if x['reaches23'])) for k,rows in dc.items()}
 cases=list(itertools.product([49.,50.,51.],[0.,math.pi/4,math.pi/2,3*math.pi/4],[0.,.05,.1],[12e-6,18e-6]))
 wr={k:[witness(d,*case) for case in cases]for k,d in DESIGNS.items()if k!='rejected_2x'}
 wsummary={k:dict(count=len(rows),all_reach23=all(x['reaches23']for x in rows),
  time_to23_range_s=[min(x['time_to23_s']for x in rows),max(x['time_to23_s']for x in rows)])for k,rows in wr.items()}
 refinement={k:[witness(d,50.,0.,0.,15e-6,dt=dt,worst_resistors=False)for dt in [1e-5,5e-6,2.5e-6]]for k,d in DESIGNS.items()if k!='rejected_2x'}
 bb={k:bounds(d) for k,d in DESIGNS.items()if k!='rejected_2x'}
 assert summary['C16']['failed_cases']==summary['ECO22']['failed_cases']==0
 assert summary['rejected_2x']['failed_cases']==4
 assert summary['ECO22']['worst_time_to23_s']<summary['C16']['worst_time_to23_s']
 assert summary['ECO22']['minimum_current_at23_A']>summary['C16']['minimum_current_at23_A']
 assert bb['ECO22']['startup_feed_only_normal_line_zero_controller_draw_ceiling_V']<bb['C16']['startup_feed_only_normal_line_zero_controller_draw_ceiling_V']<35
 assert bb['ECO22']['no_positive_feed_hold_lower_19to9p45_s']>=bb['C16']['no_positive_feed_hold_lower_19to9p45_s']
 assert bb['ECO22']['single_startup_resistor_short_other_heat_atVDD0_W']<bb['ECO22']['retained_CRCW2512_P125_screen_W']
 assert all(v['all_reach23']for v in wsummary.values())
 for rows in refinement.values():assert max(x['time_to23_s']for x in rows)-min(x['time_to23_s']for x in rows)<=2e-5
 result=dict(scope='Conditional pre-UVLO charge/feed/hold comparisons; no full startup, optical response, fault-retry or physical qualification',
  designs=DESIGNS,DC_summary=summary,DC_cases=dc,bounds=bb,
  rectifier_witness_summary=wsummary,rectifier_witness_cases=wr,
  max_ECO22_minus_C16_corresponding_witness_time_s=max(n['time_to23_s']-o['time_to23_s']for o,n in zip(wr['C16'],wr['ECO22'])),
  rectifier_witness_conditions=dict(line_Vac=207.,R1_ohm=47*1.05,fuse_resistance_assumed_ohm=6.,bridge_drop_assumed_V=2.,
   bulk_bleed_ohm=499000*.979,bulk_leak_selected_A=246.5e-6,Cdd_F=.94e-6*1.05,
   D2_plus_TI_draw_A=21.5e-6,dt_s=1e-5,no_switching_before23V=True),
  nominal_resistor_witness_timestep_refinement=refinement,
  unchanged_functions=['R1/inrush','two independent bulk-bleed branches','output preload/bleeders','R9 current/OCP programming','R4/R5/R6 voltage/line/current compensation'],
  resistor_only_nominal_heat_saving_W=bb['C16']['nominal_startup_resistor_heat_W']+bb['C16']['nominal_R13_heat_W']-bb['ECO22']['nominal_startup_resistor_heat_W']-bb['ECO22']['nominal_R13_heat_W'],
  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),all_self_checks_passed=True)
 (D/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({k:result[k]for k in ['DC_summary','rectifier_witness_summary','max_ECO22_minus_C16_corresponding_witness_time_s','resistor_only_nominal_heat_saving_W','all_self_checks_passed']},indent=2))

if __name__=='__main__':main()

"""POWER20 conditional accounting model. Stdlib only; not a switched-circuit model.
Replay from any cwd: python calculate.py. See README for unmeasured assumptions.
"""
from pathlib import Path
import bisect, csv, hashlib, itertools, json, math

D = Path(__file__).resolve().parent
P = D.parents[1]

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def put(name, obj):
    (D/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')

curves = read(P/'led-compatibility-19/native-curve-data.json')
vs = curves['voltage_curve']['samples_A_V']

def interp(x, pairs):
    j = bisect.bisect_right([q[0] for q in pairs], x)
    assert 0 < j < len(pairs)
    a,b = pairs[j-1:j+1]
    return a[1]+(x-a[0])/(b[0]-a[0])*(b[1]-a[1])

def output(itotal, tj):
    # Controller regulates TOTAL secondary current, including 10k output bleeder.
    iled = itotal-.0021
    for _ in range(20):
        vo = 7*(interp(iled, vs)-.0009*(tj-25))
        iled = itotal-vo/10000
    return vo, iled

def line(vac, cap, rseries, bridge_drop, pfixed, vdd, leak, dt, rstart=804000):
    """Midpoint C-input rectifier, six line cycles; average final two cycles.
    Ideal sine50Hz, no line impedance except declared Rseries; no EMI/filter model.
    Load = fixed converter power + actual-voltage bleeders/startup/leakage.
    """
    hz=50.; duration=6/hz; start=4/hz
    n=round(duration/dt); dt=duration/n
    v=vac*math.sqrt(2)-bridge_drop
    sums=[0.]*10; lo=1e9; hi=0.; last=v; initial=None
    for k in range(n):
        t=(k+.5)*dt
        src=max(0.,vac*math.sqrt(2)*abs(math.sin(2*math.pi*hz*t))-bridge_drop)
        ib=max(0.,(src-v)/rseries)
        load=pfixed/v+v/499000+(v-vdd)/rstart+leak
        mid=v+.5*dt*(ib-load)/cap
        ib=max(0.,(src-mid)/rseries)
        il=pfixed/mid+mid/499000+(mid-vdd)/rstart+leak
        ic=ib-il
        v+=dt*ic/cap
        if t>=start:
            if initial is None: initial=last
            vals=(ib*ib,ib,mid,mid*mid,1/mid,ic*ic,il*il,
                  mid*il,ib*(src+bridge_drop),ic)
            for j,x in enumerate(vals): sums[j]+=x*dt/(duration-start)
            lo=min(lo,mid); hi=max(hi,mid)
        last=v
    return dict(zip(['ib2','ib','v','v2','invv','iclf2','load2','pbus','pline','icmean'],sums)),lo,hi,.5*cap*(v*v-initial*initial)/(duration-start)

PRESETS={
    'low': dict(rds=8., esw=0.5e-6, cap=18e-6, brdrop=1.0, fuse=3.,
                c1_hf_esr=1., c1_lf_esr=10., leak=10e-6, irun=.0021, reverse=.001, clamp_fraction=.20),
    'central':dict(rds=12., esw=2e-6, cap=15e-6, brdrop=1.4, fuse=4.48,
                c1_hf_esr=3., c1_lf_esr=22., leak=50e-6, irun=.0021, reverse=.005, clamp_fraction=.35),
    'high':dict(rds=16., esw=5e-6, cap=12e-6, brdrop=2.0, fuse=6.,
                c1_hf_esr=8., c1_lf_esr=30., leak=246.5e-6, irun=.00265, reverse=.02, clamp_fraction=.50)}

def row(vac=230, eta=.9, corner='nom', preset='central', tj=85, dt=4e-6, revision='new'):
    a=PRESETS[preset]
    rstart,rbias=(844000,84500) if revision=='new' else (804000,80600)
    # These corners retain the existing C16 VCCR/Rcs allocation, not a full MC bound.
    vccr,rcs,vcst,lp={'min':(.310,1.8*1.021,.775,.00121),
                     'nom':(.319,1.8,.750,.0011),
                     'max':(.329,1.8*.979,.715,.00099)}[corner]
    itotal=vccr*eta*4/(2*rcs)
    ip=vcst/rcs; ispk=eta*4*ip
    demag=2*itotal/ispk
    ir = ({'low':5e-6,'central':100e-6,'high':.0025}[preset] if revision=='new' else 0.)
    output_net=itotal-ir*(1-demag)
    vo,iled=output(output_net,tj)
    ip=vcst/rcs; ispk=eta*4*ip
    is2=2/3*ispk*itotal
    ic42=is2+ir*ir*(1-demag)-output_net**2
    pc4=.12*ic42  # 100kHz/20C source condition; other conditions unqualified.
    pd_forward=(.58*itotal+.03*is2 if revision=='new' else .68*itotal+.06*is2)
    pd3=pd_forward+a['reverse']
    E=.5*lp*ip**2
    # Primary-on reverse exposure Vbus/N. Dpri=f*LP*Ip/Vbus.
    # Output leakage charge is subtracted from LED current, not counted twice.
    freq=(vo*itotal+pd3+pc4)/(eta*E-ir*lp*ip/4)
    pd_reverse=ir*(vo*(1-demag)+freq*lp*ip/4)
    pd3+=pd_reverse
    psecondary=vo*output_net+pd3+pc4
    G=freq*E
    demag=2*itotal/ispk
    # This effective triangle is algebraically charge/energy-consistent ONLY.
    vdeff=(pd3+pc4-vo*ir*(1-demag))/itotal
    td=lp*ip/(4*(vo+vdeff))
    vdd=(vo+(pd_forward/itotal if revision=='new' else .75))*10/18-.75
    extra_esw=({'low':0.,'central':.10e-6,'high':.30e-6}[preset] if revision=='new' else 0.)
    qswitch=freq*(a['esw']+extra_esw)  # inclusive residual Coss/turnoff/ringing sensitivity.
    pfixed=G+qswitch+.1
    for _ in range(8):
        s,lo,hi,storage=line(vac,a['cap'],47+a['fuse'],a['brdrop'],pfixed,vdd,a['leak'],dt,rstart)
        ip2=freq*lp*ip**3/3*s['invv']
        qcond=ip2*a['rds']; sense=ip2*rcs
        hf2=max(0.,ip2-s['load2'])
        c1hf=hf2*a['c1_hf_esr']; c1lf=s['iclf2']*a['c1_lf_esr']
        updated=G+qswitch+qcond+sense+c1hf+c1lf
        if abs(updated-pfixed)<1e-9: break
        pfixed=updated
    # Loss allocation WITHIN eta allowance; actual T1/clamp split unpublished.
    startup_i=(s['v']-vdd)/rstart
    gate_i=10e-9*freq
    pulldown_i=10/47000*(freq*lp*ip*s['invv'])
    load_i=a['irun']+gate_i+vdd/rbias+pulldown_i
    aux_i=max(0.,load_i-startup_i)
    aux_network=(vdd+.75)*aux_i+.005  # .005W selected R10/VS pulse allowance.
    residual=(1-eta)*G-aux_network
    assert residual>0
    clamp=residual*a['clamp_fraction']; transformer=residual-clamp
    startup_input=(s['v2']-vdd*s['v'])/rstart
    startup_heat=(s['v2']-2*vdd*s['v']+vdd*vdd)/rstart
    losses={
      'R1':47*s['ib2'], 'F1':a['fuse']*s['ib2'], 'BR1':a['brdrop']*s['ib'],
      'C1':c1hf+c1lf+a['leak']*s['v'], 'bulk_bleeders_R2_R3_R14_R15':s['v2']/499000,
      'startup_R16_R17':startup_heat, 'Q1':qcond+qswitch, 'R9':sense,
      'T1_assumed_allocation':transformer, 'D1_TVS1_assumed_allocation':clamp,
      'U1_aux_gate_R10_R13_VS_network':aux_network+vdd*startup_i,
      'D3':pd3, 'C4':pc4, 'output_bleeders_R11_R12':vo*vo/10000}
    pled=vo*iled; heat=sum(losses.values()); pin=pled+heat
    rms=math.sqrt(s['ib2'])
    balance=pin-s['pline']
    assert abs(balance)<.002, (balance,preset,vac)
    assert abs(.5*ispk*td*freq-itotal)<1e-12
    assert abs(eta*G-psecondary)<1e-12
    assert demag+freq*lp*ip/lo<1
    return dict(Vac=vac, eta_XFMR_assumed=eta, corner=corner, preset=preset,
       Vf_model_Tj_C=tj, flux_model_used=False,
       revision=revision, total_secondary_A=itotal, net_output_A=output_net, diode_reverse_assumed_A=ir, diode_forward_W=pd_forward, diode_reverse_W=pd_reverse, extra_switch_energy_assumed_J=extra_esw, LED_current_A=iled, Vo_V=vo,
       LED_power_W=pled, total_DC_output_W=vo*output_net, input_W=pin,
       driver_heat_W=heat, efficiency_to_LEDs=pled/pin,
       efficiency_to_total_output=vo*output_net/pin,
       line_current_RMS_A=rms, PF_model=pin/(vac*rms),
       bus_min_V=lo,bus_mean_V=s['v'],bus_max_V=hi,
       primary_RMS_surrogate_A=math.sqrt(ip2),secondary_RMS_surrogate_A=math.sqrt(is2),
       C1_LF_RMS_A=math.sqrt(s['iclf2']),C1_HF_RMS_surrogate_A=math.sqrt(hf2),
       C4_RMS_surrogate_A=math.sqrt(ic42),frequency_surrogate_Hz=freq,
       demag_duty_surrogate=demag, primary_peak_assumed_A=ip, VDD_surrogate_V=vdd,
       aggregate_G_W=G, aggregate_loss_W=(1-eta)*G, net_aux_allocation_W=aux_network,
       startup_branch_input_W=startup_input, losses_W=losses,
       line_energy_residual_W=balance, capacitor_storage_rate_W=storage,
       charge_residual_A=.5*ispk*td*freq-itotal,dt_s=dt)

def main():
    rows=[row(v,e,c,p) for v,e,c,p in itertools.product([207,230,253],[.85,.9,.93],['min','nom','max'],PRESETS)]
    nominal=row()
    refinement=row(dt=2e-6)
    coldhot=[row(v, e, c, 'high', t) for v,e,c,t in itertools.product([207,253],[.85,.93],['min','max'],[10,115])]
    allrows=rows+coldhot
    def span(key):return [min(r[key] for r in allrows),max(r[key] for r in allrows)]
    # Explicit illustrative thermal star: ALL driver heat goes through board node;
    # all driver heat plus fLED*electrical LED power heats an effective cavity node.
    # No optical heat credit; R values are assumed goals, not measured properties.
    thermal=[]
    local={'Q1_junction':('Q1',24.2), 'D3_junction':('D3',20.),
      'U1_aux_junction_upper_allocation':('U1_aux_gate_R10_R13_VS_network',44.4),
      'T1_hotspot_UNCALIBRATED':('T1_assumed_allocation',40.),
      'C1_internal_UNCALIBRATED':('C1',80.), 'C4_internal_UNCALIBRATED':('C4',120.),
      'R1_hotspot_UNCALIBRATED':('R1',25.), 'BR1_junction_UNCALIBRATED':('BR1',30.),
      'TVS_D1_hotspot_UNCALIBRATED':('D1_TVS1_assumed_allocation',50.)}
    cases={'target_path':(3.,8.,0.),'weak_closed_path':(8.,18.52,.25),'poor_closed_path':(15.,30.,.5)}
    for rlabel,r in [('central',nominal),('max_heat_selected',max(allrows,key=lambda r:r['driver_heat_W']))]:
      for ta,(name,(ra,rb,coupling)) in itertools.product([10,25,40],cases.items()):
        air=ta+ra*(r['driver_heat_W']+coupling*r['LED_power_W'])
        board=air+rb*r['driver_heat_W']
        temps={k:board+res*r['losses_W'][ref] for k,(ref,res) in local.items()}
        thermal.append(dict(electrical_case=rlabel,ambient_C=ta,scenario=name,
          R_cavity_effective_K_W=ra,R_board_to_cavity_K_W=rb,LED_heat_coupling_fraction=coupling,
          cavity_air_C=air,board_node_C=board,component_scenario_C=temps,
          transformer_air_50C_condition_met_in_scenario=air<=50))
    maxheat=max(r['driver_heat_W'] for r in allrows)
    maxled=max(r['LED_power_W'] for r in allrows)
    cooling=[dict(ambient_C=ta,LED_heat_fraction=f,
        R_cavity_max_K_W=(50-ta)/(maxheat+f*maxled))
        for ta,f in itertools.product([10,25,40],[0,.25,.5,1.])]
    results=dict(scope='Conditional unmeasured accounting and thermal scenarios; no hard loss/temperature bounds',
       nominal=nominal,scenario_count=len(allrows),ranges_selected_cases={k:span(k) for k in
       ['input_W','driver_heat_W','LED_power_W','efficiency_to_LEDs','line_current_RMS_A','PF_model','LED_current_A','Vo_V']},
       refinement={'dt_coarse_s':4e-6,'dt_fine_s':2e-6,
       'input_delta_W':refinement['input_W']-nominal['input_W'],
       'Irms_delta_A':refinement['line_current_RMS_A']-nominal['line_current_RMS_A']},
       cooling_requirements=cooling,thermal_scenarios=thermal)
    assert abs(results['refinement']['input_delta_W'])<.002
    assert abs(results['refinement']['Irms_delta_A'])<.0002
    put('results.json',results);put('electrical-cases.json',allrows)
    with (D/'electrical-cases.csv').open('w',newline='',encoding='utf-8') as f:
      keys=[k for k in nominal if k!='losses_W'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
      w.writerows({k:r[k] for k in keys} for r in allrows)
    print(json.dumps({'nominal':{k:nominal[k] for k in ['input_W','LED_power_W','driver_heat_W','efficiency_to_LEDs','line_current_RMS_A','PF_model']},'ranges':results['ranges_selected_cases'],'refinement':results['refinement']},indent=2))

if __name__=='__main__':
    main()
    old=row(revision='old');new=row(revision='new')
    prior=read(P/'power-thermal-20/results.json')['nominal']
    assert abs(old['input_W']-prior['input_W'])<1e-9
    assert abs(old['driver_heat_W']-prior['driver_heat_W'])<1e-9
    cases=read(D/'electrical-cases.json');pairs=[]
    for n in cases:
        o=row(n['Vac'],n['eta_XFMR_assumed'],n['corner'],n['preset'],n['Vf_model_Tj_C'],revision='old')
        pairs.append(dict(case={k:n[k]for k in ['Vac','eta_XFMR_assumed','corner','preset','Vf_model_Tj_C']},input_change_W=n['input_W']-o['input_W'],heat_change_W=n['driver_heat_W']-o['driver_heat_W'],LED_power_change_W=n['LED_power_W']-o['LED_power_W'],efficiency_change_pp=100*(n['efficiency_to_LEDs']-o['efficiency_to_LEDs'])))
    put('comparison.json',dict(old_nominal=old,new_nominal=new,
        nominal_input_change_W=new['input_W']-old['input_W'],nominal_heat_change_W=new['driver_heat_W']-old['driver_heat_W'],nominal_efficiency_change_pp=100*(new['efficiency_to_LEDs']-old['efficiency_to_LEDs']),
        all_selected_cases_improved=all(p['heat_change_W']<=0 and p['efficiency_change_pp']>=0 for p in pairs),paired_cases=pairs,
        caveat='Source conduction envelopes at different hot-reference conditions; IR and incremental switching energy are sensitivities. Not measured same-temperature performance or guaranteed gain.'))
    print('Paired central result',new['input_W'],new['driver_heat_W'],new['efficiency_to_LEDs'], 'baseline replay PASS')


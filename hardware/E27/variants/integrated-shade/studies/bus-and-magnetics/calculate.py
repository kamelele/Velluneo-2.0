from pathlib import Path
import json,math,hashlib,sys

def simulate(vrms,c_uf,cfg,dt):
    p=cfg['led_power_w']/cfg['assumed_efficiency'];c=c_uf*1e-6*cfg['capacitance_multiplier']
    f=cfg['line_hz']; peak=vrms*math.sqrt(2);drop=cfg['bridge_drop_v']
    # At t=0, sine phase is pi/2 and the capacitor starts charged. No cold start.
    v=max(0,peak-drop);period=1/f
    n=round(cfg['simulation_duration_s']/dt);n_window=round(cfg['analysis_duration_s']/dt)
    mins=[];energy_in=0.;energy_out=0.;vstart=None;trace=[]
    low_count={str(vled):0 for vled in cfg['led_voltage_v']}
    for k in range(1,n+1):
        t=k*dt;old=v
        demanded=p*dt;energy_before=.5*c*v*v
        free=math.sqrt(max(0,v*v-2*demanded/c))
        source=max(0,peak*abs(math.cos(2*math.pi*f*t))-drop)
        v=max(free,source)
        # If capacitor cannot support demanded energy, mark the deficit, do not hide it.
        served=min(demanded,energy_before)
        input_energy=max(0,.5*c*v*v-max(0,energy_before-demanded))
        # With ideal clamping, source can also supply demanded power when free update exhausted.
        # Difference between demanded and available cap energy is not a valid regulated solution.
        if k>n-n_window:
            if vstart is None:vstart=old
            mins.append(v);energy_in+=input_energy;energy_out+=served
            for vled in cfg['led_voltage_v']:
                if v<vled/cfg['hv9961']['max_ideal_duty']:low_count[str(vled)]+=1
            if k%max(1,round(.0001/dt))==0:trace.append([round((t-(cfg['simulation_duration_s']-cfg['analysis_duration_s']))*1000,5),v])
    stored_delta=.5*c*(v*v-vstart*vstart)
    return dict(mains_vrms=vrms,capacitance_nominal_uf=c_uf,capacitance_screen_uf=c*1e6,time_step_s=dt,min_bus_v=min(mins),max_bus_v=max(mins),
      headroom_failure_fraction={s:v/len(mins) for s,v in low_count.items()},
      interpretation='Constant-demand screening only; any nonzero headroom-failure fraction invalidates continuous-regulation inference for that LED scenario.',
      input_energy_j=energy_in,served_sink_energy_j=energy_out,demanded_sink_energy_j=p*cfg['analysis_duration_s'],
      numerical_unserved_energy_j=p*cfg['analysis_duration_s']-energy_out,
      stored_energy_delta_j=stored_delta,energy_balance_error_j=energy_in-energy_out-stored_delta,
      periodic_end_minus_start_v=v-vstart,trace_ms_v=trace)

def main(folder):
    cfg=json.loads((folder/'inputs.json').read_text());rows=[];convergence=[];traces={}
    for line in cfg['mains_vrms']:
        for cap in cfg['capacitor_nominal_uf']:
            runs=[simulate(line,cap,cfg,dt) for dt in cfg['steps_s']]
            fine=runs[-1];trace=fine.pop('trace_ms_v')
            if line==207 and cap in [2.2,4.7,10]:traces[str(cap)]=trace
            convergence.append(dict(line_vrms=line,cap_nominal_uf=cap,min_bus_delta_v=abs(runs[0]['min_bus_v']-fine['min_bus_v']),
              max_dropout_fraction_delta=max(abs(runs[0]['headroom_failure_fraction'][s]-fine['headroom_failure_fraction'][s]) for s in fine['headroom_failure_fraction'])))
            rows.append(fine)
    h=cfg['hv9961'];mag=[]
    busmax=max(r['max_bus_v'] for r in rows)
    for vled in cfg['led_voltage_v']:
        i=cfg['led_power_w']/vled;toff=h['off_time_typ_us']*1e-6;hi=h['off_time_max_us']*1e-6;lo=h['off_time_min_us']*1e-6
        l_nom=vled*hi/(h['ripple_pp_fraction']*i*h['inductance_multiplier'])
        t_on=lo*vled/(busmax-vled);fs=(1-vled/busmax)/lo
        l_crm=vled*(1-vled/300)/(2*i*60000)
        mag.append(dict(led_voltage_v=vled,current_ma=i*1000,ideal_required_min_bus_v=vled/h['max_ideal_duty'],
          ccm_l_nominal_mh_for_40pct_pp_worst_timer_and_minus10pctL=l_nom*1000,
          ccm_min_current_ma=(i-.5*vled*hi/(l_nom*h['inductance_multiplier']))*1000,
          estimated_min_on_us=t_on*1e6,estimated_max_frequency_khz=fs/1000,
          min_on_boundary_screen=t_on*1e6>=h['min_on_boundary_us'],
          approximate_chip_input_current_ma=h['approximate_bias_current_ma']+h['illustrative_mosfet_gate_charge_nc']*1e-9*fs*1000,
          approximate_chip_total_input_power_w=busmax*(h['approximate_bias_current_ma']/1000+h['illustrative_mosfet_gate_charge_nc']*1e-9*fs),
          generic_critical_mode_l_mh_at300v60khz=l_crm*1000,
          generic_critical_mode_peak_energy_mj=.5*l_crm*(2*i)**2*1000))
    output=dict(revision=cfg['revision'],kind='idealized_numerical_screening_not_qualified_simulation',input_sha256=hashlib.sha256((folder/'inputs.json').read_bytes()).hexdigest(),
      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),bus_results=rows,convergence=convergence,magnetic_sensitivity=mag,
      maximum_minbus_step_difference_v=max(x['min_bus_delta_v'] for x in convergence),
      max_abs_periodic_endpoint_v=max(abs(x['periodic_end_minus_start_v']) for x in rows),
      max_abs_energy_balance_error_j=max(abs(x['energy_balance_error_j']) for x in rows),
      limitations=cfg['assumptions']+['Approximate chip input power includes external gate-drive power, is not die dissipation or a complete thermal model;6nC gate charge and1mA bias are illustrative.','Generic critical-mode inductor comparison is topology sensitivity, not a BP2863XJ implementation or timing guarantee.','No actual magnetic core/winding/saturation/DCR rating, capacitor, bridge or controller is selected.'])
    (folder/'results.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    (folder/'traces.json').write_text(json.dumps(dict(x_unit='ms',y_unit='V',mains_vrms=207,series_cap_nominal_uf=traces),indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['maximum_minbus_step_difference_v','max_abs_periodic_endpoint_v','max_abs_energy_balance_error_j']}))
    for r in rows:
        if r['mains_vrms']==207:print(json.dumps({k:r[k] for k in ['capacitance_nominal_uf','min_bus_v','headroom_failure_fraction','numerical_unserved_energy_j']}))
    print(json.dumps(mag))
if __name__=='__main__':main(Path(sys.argv[1]))

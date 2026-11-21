"""Source-conditioned engineering screen, NOT a guaranteed device/circuit model.
Replay: python calculate.py (no command-line arguments; see README).
No third-party libraries except numpy/numba for numerical integration.
"""
from pathlib import Path
import math, json, hashlib
import numpy as np
from numba import njit

HERE=Path(__file__).resolve().parent

@njit
def bridge(vac,hz,cap,r,vd,power,dt):
    # Averaged constant-power load: resolves line-frequency current only.
    # Switching ripple added analytically with covariance explicitly neglected.
    duration=10/hz; start=8/hz
    v=vac*math.sqrt(2)-vd; s=np.zeros(9); vmin=1e6; vmax=0.
    n=int(round(duration/dt)); dt=duration/n
    for j in range(n):
        t=(j+.5)*dt
        src=vac*math.sqrt(2)*abs(math.sin(2*math.pi*hz*t))-vd
        # Midpoint integration; cap time constant is >= 0.5 ms.
        ib=max(0.,(src-v)/r); load=power/v+v/499000.
        mid=v+.5*dt*(ib-load)/cap
        ib=max(0.,(src-mid)/r); il=power/mid; bl=mid/499000.; ic=ib-il-bl
        v+=dt*ic/cap
        if t>=start:
            vals=(ib*ib,ib,mid*mid,mid*il,ic*ic,il*il,ib*mid,mid,ic)
            for k in range(9): s[k]+=vals[k]*dt/(duration-start)
            vmin=min(vmin,mid); vmax=max(vmax,mid)
    return s,vmin,vmax

def offcycle(vo,ipk,lp,lk,temp):
    factor=1+.00393*(temp-20)
    rp,rs,ra=np.array([3.78378,.381205,.665665])*factor
    lm=lp-lk; vr=4*(vo+.68); rr=16*(rs+.06)
    k=rr/lm; c=vr/rr
    td=math.log1p(ipk/c)/k
    jm=(ipk+c)**2*(-math.expm1(-2*k*td))/(2*k)-2*c*(ipk+c)*(-math.expm1(-k*td))/k+c*c*td
    return rp,rs,ra,td,16*jm

def row(vo,io,vac,hz,cap,r1,rds,coreac,esw,dt=1e-6):
    lp=.002304; lk=.000020; ipk=.810/(2.37*.979)
    rp,rs,ra,td,js=offcycle(vo,ipk,lp,lk,110)
    emag=.5*lp*ipk**2
    vc=175.1164; vr=4*(vo+.68)
    eclamp=.5*lk*ipk**2*vc/(vc-vr)
    # Solve off-time energy ledger, not an assumed conversion efficiency.
    freq=50000.
    for _ in range(40):
        iaux=.0035+freq*16e-9
        vdd=(22/30)*(vo+.68)-1
        aux=(vdd+1)*iaux+(ra+4.7)*(120/22)*ipk*iaux
        diode=.68*(io+vo/10000)+.06*freq*js
        sec=rs*freq*js
        fixed=vo*io+vo*vo/10000+aux+diode+sec+coreac
        freq=fixed/(emag-eclamp)
    ron=rds+rp+2.37
    # First iterate input on loss at representative bus, then actual line-average.
    pin=freq*emag+.2
    for _ in range(8):
        s,vmin,vmax=bridge(vac,hz,cap,r1+4.48,1.2,pin,dt)
        vb=s[7]
        ton=-lp/ron*math.log1p(-ipk*ron/vb)
        ebus=vb/ron*(vb*ton-lp*ipk)
        ji=(ebus-emag)/ron
        pin=freq*(ebus+esw)
    switched_primary_ms=freq*ji
    # Triangle approximation of input switching variance; line-averaged base removed.
    # This is a spectral split screen, not FFT or the earlier switched RK4 model.
    hf_variance=max(0.,switched_primary_ms-s[5])
    lf_cap_ms=s[4]
    c1_lf=lf_cap_ms*(.25/(2*math.pi*120*12e-6))
    c1_hf=hf_variance*3.0
    c1_leak=3e-6*math.sqrt(15*450)*s[7]
    losses={
        'R1':s[0]*r1, 'fuse_typical_only':s[0]*4.48,
        'bridge_constant_drop':s[1]*1.2,'bulk_bleed':s[2]/499000,
        'C1_LF_20C_120Hz_screen':c1_lf,'C1_HF_3ohm_sensitivity':c1_hf,
        'C1_leak_20C_rated_test_screen':c1_leak,
        'MOS_conduction':freq*ji*rds,'primary_copper':freq*ji*rp,
        'sense':freq*ji*2.37,'MOS_switching_sensitivity':freq*esw,
        'clamp':freq*eclamp,'secondary_copper':sec,'output_diode':diode,
        'aux_total':aux,'output_bleed':vo*vo/10000,
        'core_AC_sensitivity':coreac,
        'C4_ESR_100kHz_screen':.12*max(0.,freq*js-io*io),
    }
    # Ripple/ESR/leak losses are diagnostic add-ons; input engine does not feed them back.
    return dict(Vo=vo,Io=io,Vac=vac,Hz=hz,C_uF=cap*1e6,R1=r1,
       Rds_hot_sensitivity=rds,core_AC_W=coreac,Eswitch_uJ=esw*1e6,
       frequency_Hz=freq,demag_duty=freq*td,on_duty=freq*ton,
       Vbus_min=vmin,Vbus_mean=vb,Vbus_max=vmax,
       bridge_rms_A=math.sqrt(s[0]),primary_rms_A=math.sqrt(switched_primary_ms),
       C1_LF_rms_A=math.sqrt(lf_cap_ms),C1_HF_rms_A=math.sqrt(hf_variance),
       losses_W=losses,total_screen_W=sum(losses.values()),
       energy_ledger_residual_W=freq*emag-(vo*io+vo*vo/10000+aux+diode+sec+coreac+freq*eclamp))

def main():
    rows=[]
    # Source-derived earlier CC screen endpoints retained, not just nominal 250mA.
    for vo in (18.,24.,27.):
      for vac in (207.,253.):
       for hz in (50.,60.):
        for r1 in (22.,33.,47.):
         for io in (.2234,.25,.2809):
          rows.append(row(vo,io,vac,hz,12e-6,r1,32.,.15,2.5e-6))
    sensitivity=[row(24.,.25,253.,50.,12e-6,47.,rds,core,sw)
       for rds in (16.,32.,48.) for core in (.05,.15,.3) for sw in (.5e-6,2.5e-6,5e-6)]
    convergence=[]
    for dt in (2e-6,1e-6,.5e-6):
        rr=row(27.,.25,207.,50.,12e-6,47.,32.,.15,2.5e-6,dt)
        convergence.append(dict(dt_s=dt,total_W=rr['total_screen_W'],R1_W=rr['losses_W']['R1'],Vmin=rr['Vbus_min']))
    surge=[]
    for r in (22.,33.,47.):
        v=253*math.sqrt(2); cap=18e-6; rmin=r*.95
        surge.append(dict(R1_nominal=r,R1_min=rmin,Vstep=v,Cmax_uF=18.,
           peak_A=v/rmin,energy_J=.5*cap*v*v,I2t_A2s=cap*v*v/(2*rmin),
           rc_time_ms=cap*rmin*1000,
           qualification='Cold ideal step only: no mains impedance credited; compare exact pulse duration/rating, not typical fuse I2t alone.'))
    result=dict(status='Conditional design sensitivity; NOT guaranteed maximum loss or physical qualification',
      rows=rows,sensitivity=sensitivity,convergence=convergence,cold_step=surge)
    assert max(abs(r['energy_ledger_residual_W']) for r in rows+sensitivity)<1e-8
    assert abs(convergence[-1]['R1_W']-convergence[-2]['R1_W'])<1e-4
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(rows=len(rows),sensitivity=len(sensitivity),
      nominal_R47_range_W=[min(r['total_screen_W'] for r in rows if r['R1']==47),max(r['total_screen_W'] for r in rows if r['R1']==47)],
      sensitivity_range_W=[min(r['total_screen_W'] for r in sensitivity),max(r['total_screen_W'] for r in sensitivity)],
      convergence=convergence),indent=2))

if __name__=='__main__': main()

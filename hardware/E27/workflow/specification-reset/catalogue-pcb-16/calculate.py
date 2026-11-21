"""Recompute the declared C16 analytical screens; no simulation or measurements."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent;f=D/'calculations.json';j=json.loads(f.read_text())
R=1.8;rt=.021;Lp=.0011;NPS=4;NPA=7.2;RS1=53600;RLC=2000;KLC=25;eta=.9
bulk=253*math.sqrt(2);rmin=R*(1-rt);lmin=Lp*.9
j['fault'].update(Rcs_min_ohm=rmin,static_ocp_a=1.6/rmin,additional_ramp_a=bulk/lmin*400e-9,peak_at_allocated_delay_a=1.6/rmin+bulk/lmin*400e-9,absolute_delay_frontier_ns=(1.1-1.6/rmin)*lmin/bulk*1e9)
j['normal'].update(output_nom_a=.319*eta*NPS/(2*R),output_screen_min_a=.310*eta*NPS/(2*R*(1+rt)),output_screen_max_a=.329*eta*NPS/(2*rmin),normal_average_peak_max_a=.775/rmin,frequency_22v_conservative_hz=.329*NPS*(22+1.7)*R*(1+rt)/(lmin*.715**2))
# TI SLUSB41A Eq4: RLC = KLC*RCS*RS1*TD*NPA/LP.
delay=RLC*Lp/(KLC*R*RS1*NPA)
j['dependent_screens']['RLC_equivalent_delay_ns']=delay*1e9
j['equations']={'Iout':'VCCR*eta*NPS/(2*RCS)','fault_peak':'1.6/RCSmin + Vbulkmax*allocated_delay/LPmin','frequency_sensitivity':'VCCR*NPS*(Vo+Vf)*RCS/(LP*VCST^2)','RLC_inverse_TI_Eq4':'TD = RLC*LP/(KLC*RCS*RS1*NPA)'}
assert abs(RLC-KLC*R*RS1*delay*NPA/Lp)<1e-9
assert 120<delay*1e9<135
assert j['fault']['peak_at_allocated_delay_a']<1.1
f.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('C16 screens recomputed; inverse Eq4 roundtrip PASS; delay_ns',delay*1e9)

# Run with Python3. No libraries, CAD or network required.
from pathlib import Path
import json,math
p=Path(__file__).resolve().parent
C=68e-6*1.2;V=135.;rlo=470*.95*.97;rhi=470*1.05*1.03
expected={"r_min_ohm":rlo,"r_max_ohm":rhi,"healthy_reconnect_a":(V-64)/rlo,"one_led_short_reconnect_a":(V-62)/rlo,"full_short_a":V/rlo,"full_short_peak_w":V*V/rlo,"series_loss_max_w":.0605**2*rhi,"normal_reservoir_max_v":90+.0605*rhi,"rc_time_to_5v_s":rhi*C*math.log(V/5)}
stored=json.loads((p/"calculation-results.json").read_text(encoding="utf-8"))
for k,v in expected.items():assert math.isclose(v,stored["additional_3pct_resistance_budget"][k],rel_tol=1e-12),k
assert math.isclose(.5*C*V**2,stored["tolerance_only"]["stored_energy_j"],rel_tol=1e-12)
assert all(stored["checks"].values())
fit=json.loads((p/"fit-study.json").read_text(encoding="utf-8"));w,h=fit["board_experiment_mm"]
for i,a in enumerate(fit["items"]):
 assert a["x"]>=1 and a["y"]>=1 and a["x"]+a["packed_w"]<=w-1 and a["y"]+a["packed_d"]<=h-1
 for b in fit["items"][i+1:]:
  assert a["x"]+a["packed_w"]<=b["x"] or b["x"]+b["packed_w"]<=a["x"] or a["y"]+a["packed_d"]<=b["y"] or b["y"]+b["packed_d"]<=a["y"]
print(json.dumps({"arithmetic":"passed","rectangle_bounds_nonoverlap":"passed","physical_qualification":False,"size_mm":[w,h],"results":expected},indent=2))

# Independently reproduce the saved fixed-L posttrip screens.
def rlc(R):
 L=.0015;disc=math.sqrt(R*R-4*L/C)
 slow=-2/(C*(R+disc));fast=-(R+disc)/(2*L)
 aa=-V*fast/(slow-fast);bb=V*slow/(slow-fast)
 tp=math.log(fast/slow)/(slow-fast)
 curr=lambda z:-C*(aa*slow*math.exp(slow*z)+bb*fast*math.exp(fast*z))
 volt=lambda z:aa*math.exp(slow*z)+bb*math.exp(fast*z)
 lo,hi=0.,1.
 for _ in range(100):
  mid=(lo+hi)/2
  if volt(mid)>5:lo=mid
  else:hi=mid
 return dict(peak_a=curr(tp),peak_time_s=tp,time_to_5v_s=hi,peak_resistor_w=R*curr(tp)**2,energy_j=.5*C*V*V)
for label,r in [("minimum_resistance",rlo),("maximum_resistance",rhi)]:
 for k,v in rlc(r).items():assert math.isclose(v,stored["posttrip_rlc_ideal"][label][k],rel_tol=1e-10),k
ov=json.loads((p/"ovp-screen.json").read_text(encoding="utf-8"));top=254000;bot=4990
reflo=2.487-.034-.0027*7.5-.002*4;refhi=2.512+.034
for key,drift in [("tolerance_and_reference_only_static_v",0),("with_independent25ppm165c_divider_drift_screen_v",25e-6*165)]:
 a=.999*(1-drift);b=1.001*(1+drift)
 expected=[reflo*(1+top*a/(bot*b)),refhi*(1+top*b/(bot*a))+200e-9*top*b]
 for a,b in zip(expected,ov[key]):assert math.isclose(a,b,rel_tol=1e-12)
print("Fixed-L RLC and OVP reference-screen arithmetic: passed; physical qualification absent")

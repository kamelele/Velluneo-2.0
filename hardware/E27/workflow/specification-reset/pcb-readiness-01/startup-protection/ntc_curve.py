"""Active NTC interval using actual Vishay tool coefficients/tolerance algorithm.

Vendor JavaScript is inspected as data, never executed. These calculations reproduce
the source tool's continuous formula before its table-display rounding.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math
D=Path(__file__).resolve().parent
a=argparse.ArgumentParser();a.add_argument('--source-dir',required=True,type=Path);arg=a.parse_args()
S=arg.source_dir
raw=(S/'vishay-ntc-100k.json').read_bytes();part=json.loads(raw)
assert part['sap_ordering_number']=='NTCS0603E3104FXT' and part['components_type']=='SMD1'
assert float(part['rnom'])==100000 and float(part['tol'])==1 and float(part['ceramics']['b25'])==4100
js=(S/'vishay-ntc-calculator.js').read_bytes();txt=js.decode()
assert 'case"SMD1"' in txt and '39.77' in txt and '358.15' in txt and 'function getRnom' in txt
rows=[];c=part['ceramics'];coeff={side:[float(c['steinhart_'+side+'_'+k]) for k in ['a','b','c','d']] for side in ['less','greater']}
def poly(t):
 aa,bb,cc,dd=coeff['less' if t<25 else 'greater'];k=t+273.15
 return aa+bb/k+cc/k**2+dd/k**3
def rnom(t):return float(part['rnom'])*math.exp(poly(t)-poly(25))
def tol(t):
 # SMD1's source-specific tolerance contains a second high-temperature term.
 q=1+float(part['tol'])/100;d=39.77*abs(1/(273.15+t)-1/298.15)
 if t<25:return q*(1+d)**2-1
 if t<85:return q*(1+d)-1
 return q*(1+d)*(1+39.77*abs(1/(273.15+t)-1/358.15))-1
def rbounds(t):r=rnom(t);d=tol(t);return r*(1-d),r*(1+d)
def solve(fn):
 lo=25.;hi=140.
 for _ in range(80):
  mid=(lo+hi)/2
  if fn(mid)>0:lo=mid
  else:hi=mid
 return (lo+hi)/2
early=solve(lambda t:rbounds(t)[0]-1/90e-6)
late=solve(lambda t:rbounds(t)[1]-.9/125e-6)
nom=solve(lambda t:rnom(t)-.95/105e-6)
for t in range(10,121,5):
 mn,mx=rbounds(t);rows.append({'T_C':t,'Rnom_ohm':rnom(t),'Rmin_ohm':mn,'Rmax_ohm':mx,'fractional_tolerance':tol(t)})
b2585=math.log(rnom(25)/rnom(85))/(1/298.15-1/358.15)
assert abs(rnom(25)-100000)<1e-8 and abs(b2585-4100)<1
assert rbounds(early)[0]>rbounds(late)[1] # distinct threshold resistance endpoints
sources=[('vishay-ntc-100k.json','https://www.vishay.com/api/designtools/calculator-ntc-rt/ntc-calculator-type?type=ntcComponents&code=NTCS0603E3104FXT'),('vishay-ntc-calculator.js','https://www.vishay.com/static/js/min/calculator-ntc-rt.min.js?v=2'),('vishay-ntc-calculator.html','https://www.vishay.com/en/thermistors/ntc-rt-calculator/')]
register=[{'filename':n,'url':u,'bytes':len((S/n).read_bytes()),'sha256':hashlib.sha256((S/n).read_bytes()).hexdigest()} for n,u in sources]
out={'scope':'Activepart nativeVishayRTtool formula/tolerance envelope and TI electrical threshold endpoints; not measured assembly trip or finished protection qualification','part':part['sap_ordering_number'],'components_type':part['components_type'],'curve':part['curve'],'native_coefficients_R_over_R25_exponent':coeff,'R25_ohm':100000,'R25_tolerance_percent':1,'native_B25_85_K':4100,'reconstructed_B25_85_K':b2585,'native_tool_SMD1_tolerance_rule':'q=1+R25tol/100; d1=39.77*abs(1/(T+273.15)-1/298.15); T<25:q*(1+d1)^2-1;25<=T<85:q*(1+d1)-1;T>=85:q*(1+d1)*(1+39.77*abs(1/(T+273.15)-1/358.15))-1','source_table_display_rounding_not_applied':True,'nominal_electrical_trip_C':nom,'electrical_trip_interval_C':[early,late],'engineering_outward_0p1C_screen':[math.floor(early*10)/10,math.ceil(late*10)/10],'resistance_threshold_endpoints_ohm':[.9/125e-6,1/90e-6],'remaining_gradient_lag_budget_after_latest_trip_K':{str(limit):limit-late for limit in [85,105,110,125]},'normal_sensor68C_margin_to_earliest_trip_K':early-68,'normal_sensor70C_margin_to_earliest_trip_K':early-70,'source_derived_RT_rows':rows,'sources':register,'not_cold_pin_compliance_or_physical_sensor_lag_proof':True}
(D/'ntc-native-curve.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:out[k] for k in ['reconstructed_B25_85_K','nominal_electrical_trip_C','electrical_trip_interval_C','engineering_outward_0p1C_screen','remaining_gradient_lag_budget_after_latest_trip_K','normal_sensor68C_margin_to_earliest_trip_K']},indent=2))

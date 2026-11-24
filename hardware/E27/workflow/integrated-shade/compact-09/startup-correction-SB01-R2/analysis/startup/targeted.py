from screen import run,summarize,H
import json,itertools
out={}
for name,ln,extra in [('retained_47_3m3',.0033,0),('series_330_3m3',.0033,330),('series_100_330u',330e-6,100)]:
 cases=[dict(R=47*rs,L=ln*ls,C1=47e-9*cs1,C4=150e-9*cs4,DCR=extra*ds+dcr,a0=a0,b0=b0,phase_deg=ph)for rs,ls,cs1,cs4,ds,dcr,a0,b0,ph in itertools.product([.95,1.05],[.9,1.1],[.95,1.05],[.9,1.1],[.95,1.05],[0.],[0,357.8],[0,357.8],[0,45,90,135])]
 rows=run(cases,dt=1e-7,source='sine');out[name]={'maxima':summarize(rows),'rows':rows,'note':'DCR includes proposed added series resistor; initialcharges independent engineering envelope0..357.8V; allLvalueslinear sensitivitiesnotvalidated saturation models'}
 # Numerical convergence on each independently controlling corner.
 worst=[]
 for key in ['C1_peak_V','C4_peak_V','L1_peak_A']:
  c=max(rows,key=lambda c:c[key]);small=run([c],dt=2.5e-8,source='sine')[0];worst.append({'key':key,'coarse_value':c[key],'fine_value':small[key],'abs_difference':abs(c[key]-small[key]),'fine':small})
 out[name]['convergence']=worst
(H/'targeted.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{'maxima':v['maxima'],'convergence':[{a:b for a,b in r.items()if a!='fine'}for r in v['convergence']]}for k,v in out.items()},indent=2))

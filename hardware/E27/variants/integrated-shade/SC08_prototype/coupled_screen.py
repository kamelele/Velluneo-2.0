"""Executed own averaged-RC/samplehold sensitivity model; not manufacturer SPICE/PIXls."""
from pathlib import Path
import json,itertools,hashlib
R=Path(__file__).parent;src=(R/'input_screen.py').read_text(encoding='utf-8');fn=src[src.index('def normal('):src.index('# Double-exponential')]
fn=fn.replace("duration=1.):", "duration=2.,Rs=28.7,Cfb=44e-6,L=.003,f=66000.,ilim=.375,vth=1.65,tmin=.5e-6):")
fn=fn.replace('f=66000.;T=1/f;Rs=28.7;L=.003;ilim=.375;vth=1.65;tau=Rs*22e-6;', 'T=1/f;tau=Rs*Cfb;')
fn=fn.replace('5070','4290')
fn=fn.replace('max(.5e-6,','max(tmin,').replace('duration=duration,Coutmax=', 'duration=duration,Rsense=Rs,Cfb=Cfb,L=L,f=f,ilim=ilim,vth=vth,Coutmax=')
import math
exec(fn)
cases=[]
for vac in [207.,230.,253.]:
 for Cfb in [18e-6,44e-6,52.8e-6]:cases.append(normal(vac=vac,Cfb=Cfb))
 for high,L in itertools.product([False,True],[.0024,.0033]):
  cases.append(normal(vac=vac,Cfb=18e-6,L=L,Rs=28.7*(.99 if high else 1.01),f=70000. if high else 62000.,ilim=.504 if high else .350,vth=1.76 if high else 1.54,tmin=.675e-6))
out={'kind':'Own executedSC08approximateRC/sampleholdnormal-loadmodel','source_research_script_sha256':hashlib.sha256((R/'input_screen.py').read_bytes()).hexdigest(),'normal_source_function':fn,'cases':cases,'summary':{'cases':len(cases),'LEDaverage_mA':[1000*min(x['LEDavg'] for x in cases),1000*max(x['LEDavg'] for x in cases)],'Cout_peak_V':max(x['Coutmax'] for x in cases),'RF_pair_loss_max_W':max(x['RFtotalW'] for x in cases)},'limitations':['Allcontrollercornersremainillustrative25C/sensitivityinputs,nofulltemperaturesiliconenvelope.','Cycle-averageinputchargeisnotexactHFsourcecurrentormagnetic/recovery/ESR/DCRmodel.','NoOVP/auto-restart,LEDIV/selfheating,thermal,EMC,faultsurge coupling.','Do nottransferSC07ideal-sourcecalibrationnumbersasSC08predictions. Actualcalibrationandcold/hotlinechecksrequired.']}
(R/'coupled-results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out['summary']))

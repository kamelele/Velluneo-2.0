from pathlib import Path
import subprocess,itertools,json,hashlib,math,time,argparse,tempfile,numpy as np
P=Path(__file__).resolve().parent
SPEC=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description='Conditional64-corner bulk RMS diagnostic; external pinned native PDF required for provenance, no native-controller/physical qualification.')
parser.add_argument('--bulk-pdf',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,default=P)
args=parser.parse_args()
expected='9fb3a22e969e8244e135b7204aa46baa7b8a99d68803a6408fca20c3d8fd5fa6'
if hashlib.sha256(args.bulk_pdf.read_bytes()).hexdigest()!=expected:
 raise ValueError('Native Rubycon source SHA256 mismatch; review new source rather than bypassing check')
OUT=args.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
build=tempfile.TemporaryDirectory(prefix='velluneo-cap-model-')
exe=Path(build.name)/'model'
subprocess.run(['g++','-O3','-std=c++17',str(P/'model.cpp'),'-o',str(exe)],check=True)
cases=[dict(zip(['Vac_rms_V','line_Hz','cap_F','series_R_ohm','bridge_drop_V','Lp_H','remaining_load_W'],r))for r in itertools.product([207.,253.],[49.,51.],[12e-6,18e-6],[44.65,59.35],[1.6,2.2],[.002304*.9,.002304*1.1],[11.])]
text=''.join(' '.join(str(x)for x in c.values())+'\n' for c in cases)
keys=['index','frequency_Hz','Vmin','Vmax','Ib_rms','Ip_rms','Idraw_rms','Ic_rms','Ib_Idraw_cross_A2','primary_mean_W','Ic_mean_A','rms_identity_residual_A2','bridge_peak_A','capacitor_mean_energy_delta_W']
def run(dt,wave=-1):
 start=time.monotonic();args=[str(exe),str(dt)]+([str(wave),str(OUT/'wave.csv')]if wave>=0 else [])
 out=subprocess.run(args,input=text,text=True,capture_output=True,check=True).stdout
 rows=[]
 for line in out.splitlines():
  z=dict(zip(keys,map(float,line.split(','))));z.update(cases[int(z['index'])]);rows.append(z)
 print('run',dt,'cases',len(rows),'s',round(time.monotonic()-start,2),flush=True);return rows
coarse=run(200e-9);fine=run(100e-9)
errors={k:max(abs(a[k]-b[k])for a,b in zip(coarse,fine))for k in ['Vmin','Vmax','Ib_rms','Ip_rms','Idraw_rms','Ic_rms','primary_mean_W','bridge_peak_A']}
assert errors['Ic_rms'] < 1e-6 and errors['Vmax'] < .001
assert max(abs(r['rms_identity_residual_A2']) for r in fine) < 1e-10
assert all(r['Ib_Idraw_cross_A2'] >= 0 for r in fine)
worst=max(fine,key=lambda r:r['Ic_rms']);idx=int(worst['index'])
# Capture only worstcase at100ns; execute onecase via same input contract.
fulltext=text;text=fulltext.splitlines()[idx]+'\n';single=run(100e-9,0)[0];text=fulltext
wave=np.genfromtxt(OUT/'wave.csv',delimiter=',',names=True)
x=wave['Ic'];N=len(x);delta=np.median(np.diff(wave['t']));y=np.fft.rfft(x);power=abs(y/N)**2;power[1:-1 if N%2==0 else None]*=2;freq=np.fft.rfftfreq(N,delta)
bands=[]
for lo,hi in [(0,50),(50,120),(120,500),(500,1000),(1000,10000),(10000,100000),(100000,float('inf'))]:
 mask=(freq>=lo)&(freq<hi);bands.append(dict(lo_Hz=lo,hi_Hz=None if math.isinf(hi)else hi,RMS_A=float(np.sqrt(sum(power[mask])))))
result=dict(task='ELEC-REFINE-02',base_commit='36ad2f243d36d592228304b26c27188da0d46c4d',model='Finite-series-R sinebridge,15uF initialtolerance,nonnegative switchedtriangular primaryload, net11W primaryenergytarget plus explicit499k*.979bleed; ideal switch/transformer/no clampreturn/no ESR/HFbridge',cases=len(fine),peak_A=.358522,rows=fine,convergence_max_abs=errors,worst_Ic_case=worst,wave_spectrum=dict(samples=N,dt_s=float(delta),window_s=N*delta,fft_parseval_RMS_A=float(np.sqrt(sum(power))),sample_RMS_A=float(np.sqrt(np.mean(x*x))),bands=bands),source_hashes={'model.cpp':hashlib.sha256((P/'model.cpp').read_bytes()).hexdigest(),'external_native_bulk_pdf':expected},limitations=['This is a conditional energy-scheduled pulse model, not nativeUCC28711 simulation or continuum proof.','11W primarypulse inputenergy and selectedpeak determinefrequency; no unsupported independentfrequency/powermaxima added.','Clamptobulk returncurrent, capacitorleakage/ESR, inputinductance/bridgeHF, deviceparasiticcurrents andrealauxiliary charging not modeled.','No physicalcaprating/lifetime or majorclosure.'])
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('errors',errors,'worst',worst,'spectrum',result['wave_spectrum'],flush=True)

build.cleanup()

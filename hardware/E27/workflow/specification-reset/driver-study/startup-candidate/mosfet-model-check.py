from pathlib import Path
import json,sys,hashlib
try:
 #!/usr/bin/env python3
 """Characterize a downloaded ST component model through available libngspice.
 No UCC controller/TVS/transformer model is implied. Vendor model remains reference-only.
 """
 from pathlib import Path
 import ctypes as C,ctypes.util,hashlib,json,sys,io,zipfile,urllib.request
 import numpy as np
 P=Path(__file__).resolve().parent;out=P/'mosfet-run';out.mkdir(exist_ok=True)
 archive=P/'source/stn1nk80z_spice.zip'
 if not archive.exists():
  archive.parent.mkdir(exist_ok=True);archive.write_bytes(urllib.request.urlopen('https://www.st.com/resource/en/spice_model/stn1nk80z_spice.zip',timeout=20).read())
 # Pin the actual manufacturer archive; do not silently accept a replacement.
 b=archive.read_bytes();assert hashlib.sha256(b).hexdigest()=='851813f6e812d104adaddf3e8fe062aef1235679492b9b2231b46eeaec480f42'
 native=zipfile.ZipFile(io.BytesIO(b)).read('stn1nk80z.lib')
 s=native.decode('latin1');adapted='\n'.join(x for x in s.splitlines() if 'MODTYPE=ELDO' not in x)
 # Adapt the sole POLY(2) source to an algebraically equivalent behavioral source.
 # Coefficients are P0,Px,Py,Pxx,Pxy: only Pxy=.0163 is nonzero.
 assert 'E3  8 13 POLY(2) 6 8 6 12 0 0 0 0  0.163E-01' in adapted
 adapted=adapted.replace('E3  8 13 POLY(2) 6 8 6 12 0 0 0 0  0.163E-01','BE3 8 13 V=0.0163*V(6,8)*V(6,12)')
 # No numeric device parameter changes; simulator compatibility still requires review.
 lib=C.CDLL(ctypes.util.find_library('ngspice'))
 logs=[]
 CB=C.CFUNCTYPE(C.c_int,C.c_char_p,C.c_int,C.c_void_p)
 @CB
 def send(msg,ident,user):logs.append(msg.decode(errors='replace'));return 0
 EXIT=C.CFUNCTYPE(C.c_int,C.c_int,C.c_bool,C.c_bool,C.c_int,C.c_void_p)
 @EXIT
 def quitcb(status,immediate,quitexit,ident,user):logs.append('CONTROLLED_EXIT '+str(status));return 0
 lib.ngSpice_Init.argtypes=[C.c_void_p]*7;lib.ngSpice_Init.restype=C.c_int
 assert lib.ngSpice_Init(C.cast(send,C.c_void_p),C.cast(send,C.c_void_p),C.cast(quitcb,C.c_void_p),None,None,None,None)==0
 lib.ngSpice_Command.argtypes=[C.c_char_p];lib.ngSpice_Command.restype=C.c_int
 lib.ngSpice_Circ.argtypes=[C.POINTER(C.c_char_p)];lib.ngSpice_Circ.restype=C.c_int
 
 def command(s):
  rc=lib.ngSpice_Command(s.encode())
  if rc!=0:raise RuntimeError((s,rc,logs[-8:]))
 command('version')
 reports=[]
 for ident,(bus,load,igate) in enumerate([(640,1.1,.001),(500,.345,.001)]):
  command('destroy all');command('reset') if ident else None
  net=f'''STN1NK80Z resistive-load gate-charge model witness
 Vdc rail 0 {bus}
 Rload rail d {bus/load}
 Vgate g 0 PWL(0 0 100n 0 10.1u 16)
 Xq d g 0 STN1NK80Z
 .options reltol=1e-5 abstol=1e-12 chgtol=1e-16 method=gear tnom=25
 .temp 25
 .tran 2n 12u 0 2n
 '''+adapted+'\n.end\n'
  lines=net.splitlines();arr=(C.c_char_p*(len(lines)+1))(*[x.encode('ascii',errors='replace') for x in lines],None)
  assert lib.ngSpice_Circ(arr)==0
  command('run');command('set wr_singlescale');command('set wr_vecnames')
  dest=(out/f'gate-{ident}.txt').resolve();command('wrdata '+str(dest)+' v(g) v(d) i(vgate)')
  (out/'ngspice.log').write_text('\n'.join(logs)+'\n')
  dat=np.loadtxt(dest,skiprows=1);t=dat[:,0];vg=dat[:,1];vd=dat[:,2]
  assert t[-1] >= 12e-6*.999, ('Transient aborted', logs[-10:])
  assert vg[0]<.1, ('Gate initial state invalid',vg[0])
  result={'Vbus_V':bus,'Iload_A':load,'load_type':'resistor','gate_ramp_s':10e-6,'rows':len(t),'gate_max_V':float(max(vg))}
  for v in [10,12,14,16]:
   ix=np.flatnonzero(vg>=v)
   if len(ix):
    k=int(ix[0]);tc=float(np.interp(v,[vg[k-1],vg[k]],[t[k-1],t[k]]))
    # Integrate actual current into the imposed slow gate-voltage source fixture.
    result[f'Qg_to_{v}V_C']=float(-np.trapezoid(dat[:k+1,3],t[:k+1]))
  reports.append(result)
 (out/'ngspice.log').write_text('\n'.join(logs)+'\n')
 errors=[x for x in logs if 'error' in x.lower() or 'warning' in x.lower()]
 print(json.dumps({'scope':'Adapted native ST MOSFET25C component fixture; not an IC or complete circuit simulation',
  'native_zip_SHA256':hashlib.sha256(b).hexdigest(),'native_lib_SHA256':hashlib.sha256(native).hexdigest(),
  'adapted_text_SHA256':hashlib.sha256(adapted.encode()).hexdigest(),'adapter':'Remove MODTYPE=ELDO selector lines; replace one POLY(2) source with its exact Vx*Vy expression; retain all numeric device values',
  'simulator_version_output':[x for x in logs if 'ngspice' in x.lower()][:8],
  'warnings_and_errors':errors,'fixtures':reports},indent=2))
except Exception as exc:
 p=Path(__file__).resolve().parent
 log=p/'mosfet-run/ngspice.log'
 report={'scope':'Adapted ST25C MOSFET component-model compatibility check only',
 'status':'failed_no_usable_transient','actual_gate_charge_verified':False,
 'full_controller_simulated':False,'error_type':type(exc).__name__,'error':str(exc),
 'log_SHA256':hashlib.sha256(log.read_bytes()).hexdigest() if log.exists() else None}
 print(json.dumps(report,indent=2));sys.exit(1)

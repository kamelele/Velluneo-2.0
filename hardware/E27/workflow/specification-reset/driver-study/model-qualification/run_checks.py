#!/usr/bin/env python3
"""Pinned native-POLY component evidence: RC smoke, MOSFET DC/AC and transient.
Vendor archive/codemodel are reference inputs, not redistributed. This is not a UCC simulation.
Returns exit1 if the component transient does not complete; never treat partial data as Qg.
"""
from pathlib import Path
import argparse,ctypes as C,hashlib,json,math,zipfile,io
import numpy as np
pa=argparse.ArgumentParser();pa.add_argument('--model-zip',required=True);pa.add_argument('--code-model',required=True);pa.add_argument('--out-dir',required=True);pa.add_argument('--library',default='/lib/x86_64-linux-gnu/libngspice.so.0');args=pa.parse_args()
out=Path(args.out_dir).resolve();out.mkdir(parents=True,exist_ok=True)
pins=[(args.model_zip,'851813f6e812d104adaddf3e8fe062aef1235679492b9b2231b46eeaec480f42'),(args.code_model,'3401deb0ee1cf58fac01f50d550b81b449374928e3117050a520d564072ed7f0'),(args.library,'8b24e526865425243ee57efa9dcbdde99e7220393eb77a1ab863e849a2e0d761')]
for path,digest in pins:assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,(path,'Input identity mismatch')
native=zipfile.ZipFile(io.BytesIO(Path(args.model_zip).read_bytes())).read('stn1nk80z.lib')
lines=native.decode('latin1').splitlines();assert sum('MODTYPE=ELDO' in x for x in lines)==5
model='\n'.join(x for x in lines if 'MODTYPE=ELDO' not in x)
assert 'E3  8 13 POLY(2) 6 8 6 12 0 0 0 0  0.163E-01' in model
lib=C.CDLL(args.library);logs=[]
CB=C.CFUNCTYPE(C.c_int,C.c_char_p,C.c_int,C.c_void_p)
@CB
def send(msg,i,u):logs.append(msg.decode(errors='replace'));return 0
EX=C.CFUNCTYPE(C.c_int,C.c_int,C.c_bool,C.c_bool,C.c_int,C.c_void_p)
@EX
def endcb(status,a,b,i,u):logs.append('CONTROLLED_EXIT '+str(status));return 0
lib.ngSpice_Init.argtypes=[C.c_void_p]*7;lib.ngSpice_Init.restype=C.c_int
assert lib.ngSpice_Init(C.cast(send,C.c_void_p),C.cast(send,C.c_void_p),C.cast(endcb,C.c_void_p),None,None,None,None)==0
lib.ngSpice_Command.argtypes=[C.c_char_p];lib.ngSpice_Command.restype=C.c_int
lib.ngSpice_Circ.argtypes=[C.POINTER(C.c_char_p)];lib.ngSpice_Circ.restype=C.c_int

def cmd(s):
 rc=lib.ngSpice_Command(s.encode());assert rc==0,(s,rc)
cmd('version');cmd('codemodel '+str(Path(args.code_model).resolve()));cmd('set numdgt=15')

def run(body,name,vectors,with_model=True,allow_incomplete=False):
 cmd('destroy all');start=len(logs)
 net='Component qualification experiment\n'+body+'\n.options tnom=25\n.temp 25\n'+(model if with_model else '')+'\n.end\n'
 ls=net.splitlines();arr=(C.c_char_p*(len(ls)+1))(*[x.encode('ascii',errors='replace') for x in ls],None)
 assert lib.ngSpice_Circ(arr)==0
 dest=out/(name+'.txt');dest.unlink(missing_ok=True)
 cmd('run');cmd('set wr_singlescale');cmd('set wr_vecnames');cmd('wrdata '+str(dest)+' '+vectors)
 data=np.atleast_2d(np.loadtxt(dest,skiprows=1));assert np.isfinite(data).all()
 errors=[x for x in logs[start:] if 'aborted' in x.lower() or 'error:' in x.lower()]
 if errors and not allow_incomplete:raise RuntimeError(errors)
 return data,logs[start:]
# Verify basic engine transient operation against a finite-ramp RC analytical solution.
d,_=run('Vstep in 0 PWL(0 0 1u 0 1.001u 1)\nR1 in o 1k\nC1 o 0 1n\n.tran 2n 10u 0 2n','rc-smoke','v(o)',False)
assert d[-1,0]>=10e-6*.999
sample_t=2.001e-6;measured=float(np.interp(sample_t,d[:,0],d[:,1]));expected=1-(1e-6/1e-9)*(-math.expm1(-1e-9/1e-6))*math.exp(-(sample_t-1.001e-6)/1e-6)
assert abs(measured-expected)<1e-4
rd=[]
for current in [.1,.3,.5]:
 d,_=run(f'Iload 0 d DC {current}\nVgate g 0 DC 10\nXq d g 0 STN1NK80Z\n.op','rd-'+str(current),'v(d)')
 rd.append({'I_A':current,'Rds_ohm':float(d[-1,-1]/current)})

def cvgrid(step_low,step_high,label):
 vs=np.unique(np.concatenate((np.arange(0,20+step_low/2,step_low),np.arange(20,640+step_high/2,step_high))))
 cs=[]
 for v in vs:
  d,_=run(f'Vdrain d 0 DC {v:.12g} AC 1\nVgate g 0 DC 0\nXq d g 0 STN1NK80Z\n.ac lin 1 1meg 1meg','ac-current','i(vdrain)')
  assert d.shape==(1,3) and d[0,0]==1e6
  cap=-d[0,2]/(2*math.pi*1e6);assert cap>0;cs.append(cap)
 np.savetxt(out/('cv-'+label+'.csv'),np.column_stack((vs,cs)),delimiter=',',header='Vds_V,Coss_F',comments='')
 return vs,np.array(cs),float(np.trapezoid(cs,vs))
v0,c0,q0=cvgrid(.5,5,'coarse');v,c,q=cvgrid(.25,2.5,'fine')
selected=[{'Vds_V':float(x),'Coss_F':float(c[np.flatnonzero(v==x)[0]])} for x in [0,1,4,10,25,50,100,200,400,500,640]]
# Original native POLY; only selector metadata removed, no B-source conversion.
body='''Vdc rail 0 640
Rload rail d 581.8181818181818
Vgate g 0 PWL(0 0 100n 0 10.1u 16)
Xq d g 0 STN1NK80Z
.options reltol=1e-5 abstol=1e-12 chgtol=1e-16 method=gear
.tran 2n 12u 0 2n'''
d,translog=run(body,'native-transient','v(g) v(d) i(vgate)',True,True)
complete=bool(d[-1,0]>=12e-6*.999 and not any('aborted' in x.lower() for x in translog))
(out/'native-transient.log').write_text('\n'.join(translog)+'\n');(out/'full-run.log').write_text('\n'.join(logs)+'\n')
summary={'study':'VEL-MODEL-01','date':'2026-11-16','runtime':'ngspice44.2 shared library with native spice2poly44.2','model_temperature_C':25,
 'native_model_SHA256':hashlib.sha256(native).hexdigest(),'adapter':'Remove5 MODTYPE=ELDO selector lines only; E3 POLY and every numeric parameter retained',
 'RC_smoke':{'complete':True,'sample_t_s':sample_t,'simulated_V':measured,'analytical_V':expected,'absolute_difference_V':abs(measured-expected)},
 'Rds_at_10V':rd,'Coss_1MHz':selected,'integrated_AC_charge_proxy_0_to_640V_C':q,'coarse_charge_proxy_C':q0,'charge_grid_refinement_difference_C':abs(q-q0),
 'native_datasheet_Coss25V_typ_F':26e-12,'model_to_datasheet_typ_Coss25V_ratio':selected[4]['Coss_F']/26e-12,
 'native_datasheet_Qoss_time_equivalent_typ_at640V_C':9.5e-12*640,
 'integral_is_a_quasistatic_proxy_not_validated_transient_charge':True,
 'component_transient':{'complete':complete,'rows':len(d),'last_time_s':float(d[-1,0]),'requested_end_s':12e-6,'errors':[x for x in translog if 'warning' in x.lower() or 'aborted' in x.lower() or 'timestep too small' in x.lower()]},
 'gate_charge_verified':False,'controller_or_whole_converter_simulated':False,
 'warnings':[x for x in logs if 'warning' in x.lower()]}
(out/'results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:summary[k] for k in ['RC_smoke','model_to_datasheet_typ_Coss25V_ratio','integrated_AC_charge_proxy_0_to_640V_C','component_transient']},indent=2))
raise SystemExit(0 if complete else 1)

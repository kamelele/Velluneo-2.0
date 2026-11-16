#!/usr/bin/env python3
"""Inspect official model archives; never decrypt, simulate or reinterpret stored traces."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--pspice-zip',required=True);p.add_argument('--tina-zip',required=True);p.add_argument('--out',required=True);a=p.parse_args()
def archive(path,pin):
 b=Path(path).read_bytes();assert hashlib.sha256(b).hexdigest()==pin,'Archive identity changed';return zipfile.ZipFile(path)
z=archive(a.pspice_zip,'b58a5070f5f94132cc7e7cd7d0be0e7484e3e743a80283aa0d745d4436926441')
t=archive(a.tina_zip,'b6d9f38a33a46b3b480b2d40071bda4a41b0af99ed9d1cd54b003f5845d59163')
def get(suffix):
 names=[n for n in z.namelist() if n.endswith('/'+suffix)];assert len(names)==1;return names[0],z.read(names[0])
libn,lib=get('UCC28710.lib');netn,net=get('Test_UCC28710_Low_Side.net');cirn,cir=get('TR.cir');logn,log=get('TR.out')
lt=lib.decode('latin1');nt=net.decode('latin1');ct=cir.decode('latin1');ot=log.decode('latin1')
sub=re.search(r'^\.SUBCKT\s+(\w+)\s+([^\r\n]+)',lt,re.M|re.I);assert sub
assert 'CBC funcrion is NOT modeled' in lt
assert re.search(r'X_U7\s+CS VS N686619 DRV VDD 0 P- UCC28710',nt)
assert 'PWL 0 0 600u 25 8m 12 8.5m 0' in nt
assert '.TRAN  0 10ms 0 20n' in ct
r={
 'study':'VEL-CTRL-EVIDENCE-01','date':'2026-11-16','method':'Archive/text audit only; no new simulation or decryption',
 'pspice_archive_SHA256':hashlib.sha256(Path(a.pspice_zip).read_bytes()).hexdigest(),
 'entries':[{'path':x.filename,'bytes':x.file_size} for x in z.infolist()],
 'selected_payloads':{n:{'SHA256':hashlib.sha256(b).hexdigest(),'bytes':len(b)} for n,b in [(libn,lib),(netn,net),(cirn,cir),(logn,log)]},
 'declared_model':{'name':sub.group(1),'terminals':sub.group(2).split(),'encrypted_marker_present':'$CDNENCSTART' in lt,'CBC_not_modeled_note':True,'declared_simulator':'PSpice16.2','model_date':'2015-05-26'},
 'reference_fixture':{'forced_VDD_ramp_V':25,'ramp_end_s':600e-6,'bulk_ramp_V':135,'bulk_ramp_end_s':300e-6,'VDD_cap_F':330e-9,'output_cap_F':1120e-6,'load_R_ohm':200,'upper_divider_R_ohm':121000,'lower_divider_R_ohm':30100,'switch':'Voltage-controlled ideal switch, not physical MOSFET','requested_transient_end_s':.01,'requested_max_step_s':20e-9},
 'bundled_log':{'job_aborted_marker':bool(re.search(r'JOB\s+ABORTED',ot)),'is_new_execution':False,'is_golden_success':False,'last_valid_time_determined':False},
 'tina_archive':{'native_LIBs':[{'path':n,'SHA256':hashlib.sha256(t.read(n)).hexdigest(),'encrypted_marker_present':t.read(n).startswith(b'<Encrypted Library>')} for n in t.namelist() if n.lower().endswith('.lib')]},
 'actual_UCC28711_verified':False,'controller_current_model_verified':False,'new_simulation_performed':False,'working_driver_verified':False}
assert r['bundled_log']['job_aborted_marker']
Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print('Audit complete; encrypted UCC28710 fixture and bundled abort identified. No simulation.')

"""Try an unchanged encrypted TI model with the already pinned KiCad ngspice DLL.
No decryptor, license change, simulator installation or native functional claim.
"""
from pathlib import Path
import ctypes as ct,os,json,hashlib,argparse,re
a=argparse.ArgumentParser();a.add_argument('--source-dir',type=Path,required=True);a.add_argument('--kicad-bin',type=Path,required=True);arg=a.parse_args()
D=Path(__file__).resolve().parent;arg.source_dir=arg.source_dir.resolve();arg.kicad_bin=arg.kicad_bin.resolve()
lib=arg.source_dir/'slum464/UCC28710_PSPICE_TRANS/UCC28710.lib'
native=(arg.kicad_bin/'ngspice.dll');os.add_dll_directory(str(arg.kicad_bin))
logs=[]
SEND=ct.CFUNCTYPE(ct.c_int,ct.c_char_p,ct.c_int,ct.c_void_p)
EXIT=ct.CFUNCTYPE(ct.c_int,ct.c_int,ct.c_bool,ct.c_bool,ct.c_int,ct.c_void_p)
@SEND
def char(s,i,p):
 text=s.decode('utf-8',errors='replace')
 # Never copy encrypted payload diagnostics into the product repository.
 text=re.sub(r'[0-9a-fA-F]{32,}','[encrypted payload token omitted]',text)
 if '$cdnenc' in text.lower() or (len(text)>150 and ' ' not in text):text='[encrypted token diagnostic omitted]'
 logs.append(text[:400]);return 0
@SEND
def stat(s,i,p):return 0
@EXIT
def quit(code,immediate,exitset,i,p):logs.append('ControlledExit code='+str(code));return 0
sp=ct.CDLL(str(native));sp.ngSpice_Init.argtypes=[ct.c_void_p]*7;sp.ngSpice_Init.restype=ct.c_int;sp.ngSpice_Command.argtypes=[ct.c_char_p];sp.ngSpice_Command.restype=ct.c_int
assert sp.ngSpice_Init(char,stat,quit,None,None,None,None)==0
sp.ngSpice_Command(b'version')
# Read-only external official model. No conversion/decryption is attempted.
deck='''TI encrypted UCC28710 compatibility probe\n.include "MODEL"\nVvdd vdd 0 21\nVhv hv 0 325\nRvs vs 0 10k\nRcs cs 0 1k\nRcbc cbc 0 10k\nRdrv drv 0 100k\nXic cs vs cbc drv vdd 0 hv UCC28710\n.op\n.end\n'''.replace('MODEL',lib.as_posix())
sp.ngSpice_Circ.argtypes=[ct.POINTER(ct.c_char_p)];sp.ngSpice_Circ.restype=ct.c_int
lines=deck.encode().splitlines();arr=(ct.c_char_p*(len(lines)+1))(*lines,None)
status=sp.ngSpice_Circ(arr);run_status=sp.ngSpice_Command(b'run')
record={'scope':'Compatibility probe only; no functional native-controller simulation','dll':str(native),'dll_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'official_model_sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'load_return':status,'run_return':run_status,'message_count':len(logs),'messages_first50':logs[:50],'messages_last20':logs[-20:],'model_encryption_preserved':True,'Velluneo_native_simulation_performed':False,'physical_operation':False}
(D/'native-probe.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'load_return':status,'messages':logs[:25],'functional_simulation':False},indent=2))

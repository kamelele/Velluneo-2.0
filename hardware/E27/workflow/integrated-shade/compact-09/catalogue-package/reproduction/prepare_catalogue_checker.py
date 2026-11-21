from pathlib import Path
import json,hashlib,re,shutil
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;S=HERE/'project';D=HERE/'routing';C=HERE/'checker';C.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
# Remove only current native DRC-reported dangling stub UUIDs, never disconnected wanted routes.
report=load(HERE/'routed-DRC.json');ids={i['uuid'] for v in report['violations'] if v['type']=='track_dangling' for i in v['items']};src=D/'SC09_compact.kicad_pcb';text=src.read_text()
text,n=re.subn(r'\n\t\((?:segment|via)\n.*?\n\t\)',lambda m:'' if any(f'(uuid "{u}")' in m.group() for u in ids) else m.group(),text,flags=re.S);src.write_text(text)
matrix=load(BASE/'spacing-thermal/spacing-contract.proposed.json');matrix['input_graph']['path']='intended-connectivity.CAT01.json';matrix['input_graph']['sha256']=sha(S/'intended-connectivity.CAT01.json');save(HERE/'spacing-matrix.CAT01.json',matrix)
assessment=load(BASE/'checker/root-lab-functional-assessment-v5.json');assessment['CAT_graph_sha256']=sha(S/'intended-connectivity.CAT01.json');assessment.pop('A1_graph_sha256',None);assessment['matrix_sha256']=sha(HERE/'spacing-matrix.CAT01.json');assessment['frozen_pad_geometry_source_board_sha256']=sha(src);assessment['retained_exception_scope']='SameU1/BR1/D1physicalmanufacturerlandcoordinates,floorsandfiniteregionsaspriorv5;newstockT1doesNOTgetaconcession. NoapprovalofnewCATmaporIECwaiverfabricated.';save(HERE/'package-assessment.CAT01.json',assessment)
code=(BASE/'checker/checker.py').read_text().replace('intended-connectivity.A1.json','intended-connectivity.CAT01.json').replace("ed.get('A1_graph_sha256')","ed.get('CAT_graph_sha256')").replace('A1 graph','CAT01 graph').replace('SC09 A1','SC09 CAT01')
(C/'checker.py').write_text(code);shutil.copy2(BASE/'checker/kernel_sc08.py',C/'kernel_sc08.py')
save(HERE/'routing/cleanup.json',{'kind':'NativeDRCreporteddanglingstubsonly','removed_UUIDs':sorted(ids),'current_board_sha256':sha(src),'all_other_copper_retained':True})
print('PrivateCAT01checkerusesindependent46pinmap;55targetsunchanged;removedstubs',len(ids))

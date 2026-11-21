from pathlib import Path
import math,json,hashlib,collections,re,shutil
HERE=Path(__file__).resolve().parent;S=HERE/'project';src=HERE.parent/'models/make_models.py';e={'__file__':str(src)};exec(compile(src.read_text().split('\nparts=')[0],str(src),'exec'),e);e['M']=S/'Models';g=json.loads((S/'footprint-geometry.json').read_text());e['G']=g
box,cyl,tube,roundbox,text=e['box'],e['cyl'],e['tube'],e['roundbox'],e['text'];metal=e['METAL'];black=e['BLACK'];copper=e['COPPER']
parts={}
parts['T1']=[roundbox(12,12,9.85,z=5.075,c=(.115,.125,.14),r=.65),box(10.9,10.9,.04,z=9.997,c=(.17,.18,.19))]
for y in [-4.8125,4.8125]:parts['T1'].append(box(5,2.375,.2,y=y,z=.1,c=metal))
parts['T1']+=text('COILCRAFT',-3.15,.9,10.025,.67,c=(.76,.78,.79))+text('125',-1.0,-1.5,10.025,1,c=(.78,.80,.81));parts['T1'].append(cyl(.65,.018,x=-4.4,y=-4.6,z=10.024,c=(.85,.85,.83),n=24))
parts['L1']=[cyl(8.3,1.1,z=1.05,c=(.07,.075,.08)),cyl(5.6,7.5,z=5.4,c=(.09,.09,.095)),cyl(8.3,1,z=9.95,c=(.075,.08,.085))]
for i in range(30):parts['L1'].append(cyl(7.55,.18,z=1.85+.251*i,c=copper))
for x in [-2.5019,2.5019]:parts['L1'].append(tube([(x,0,-1.7),(x,0,1.0)],.35))
parts['L1']+=text('3m3',-1.6,-.2,10.463,.7,c=(.71,.74,.75))
# Conservative coated envelope L2max7.5mm; provide2mm straightlead before R7 top bend.
parts['R7']=[cyl(2.46,7.5,z=4.25,c=(.25,.45,.57)),tube([(0,0,-1.7),(0,0,.55)],.315)]
for z,col in [(1.5,(.80,.32,.04)),(2.4,(.84,.84,.81)),(3.3,(.035,.035,.035)),(4.2,(.80,.32,.04)),(6.8,(.32,.17,.06))]:parts['R7'].append(cyl(2.5,.42,z=z,c=col))
path=[(0,0,7.95),(0,0,10)]+[(0,-1+math.cos(a),10+math.sin(a)) for a in [math.pi*j/24 for j in range(1,13)]]+[(0,-3.8,11)]+[(0,-3.8-math.sin(a),10+math.cos(a)) for a in [math.pi*j/24 for j in range(1,13)]]+[(0,-4.8,-1.7)];parts['R7'].append(tube(path,.315))
g['R7']['planned_max_above_PCB_mm']=11.5;g['R7']['design_basis']='CatalogueHVR2500003903FR500390k1%1600V/.25W;coatedL2max7.5,D2.5,leadmax.63. StandingP4.8normalmanualformingproposal:bodyseating.5,2mmstraightleadabovemaxbodybeforeR1bend,peak~11.315,maxbudget11.5. Actualformedpartinspectionrequired.'
(S/'footprint-geometry.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
info=json.loads((S/'Models/MODEL_INFO.json').read_text());records=[]
for ref,meshes in parts.items():
 for vs,fs,col in meshes:
  edges=collections.Counter(tuple(sorted((f[i],f[(i+1)%len(f)]))) for f in fs for i in range(len(f)));assert all(v==2 for v in edges.values());assert all(math.isfinite(a) for p in vs for a in p)
 e['write']('SC09_'+ref,meshes);vs=[v for part in meshes for v in part[0]];bbox=[min(v[i] for v in vs) for i in range(3)]+[max(v[i] for v in vs) for i in range(3)];assert bbox[5]<=g[ref]['planned_max_above_PCB_mm'];row=next(r for r in info['models'] if r['ref']==ref);row.update(actor='/root',revision='SC09-CAT01cataloguepackage',mesh_bbox_mm=bbox,geometry_source=g[ref],mesh_count=len(meshes),sha256={ext:hashlib.sha256((S/'Models'/('SC09_'+ref+'.'+ext)).read_bytes()).hexdigest() for ext in ['wrl','step']});records.append({'ref':ref,'bbox_mm':bbox,'closed_mesh':True,'finite_vertices':True,'part_qualified_model':False})
info['root_catalogue_change']='T1nowCoilcraft2terminalstockSMD,markerdotatmodelYnegativealignsfootprintpin1atpositiveY;L1stockWurthdrum;R7catalogueHVRconservativecoatedenvelope/2mmstraightleadforming. Other14WRLmeshesunchanged. NativeVRMLverified,STEPfacetsnotqualifiedinterchange.';info['root_current_geometry_sha256']=hashlib.sha256((S/'footprint-geometry.json').read_bytes()).hexdigest();(S/'Models/MODEL_INFO.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n');(S/'Models/catalogue-model-checks.json').write_text(json.dumps({'actor':'/root,assetauthornotindependentreviewer','models':records,'T1_dot_assignment':'BottomsideofbodyinFviewcorrespondsPad1LED_PLUS;nonpolarinductor,notanisolatingtransformer.','physical_forming_qualified':False},indent=2)+'\n')
for folder in [S/'E27SC09.pretty',HERE/'routing/E27SC09.pretty']:
 p=folder/'SC09_R7.kicad_mod';p.write_text(re.sub(r'(?<!H)VR25','HVR25',p.read_text()))
# Adopt only the verified private thermal candidate; no customer CAD mutation.
shutil.copy2(S/'.work/thermal-guards.kicad_pcb',S/'SC09_compact.kicad_pcb')
(HERE/'catalogue-model-results.json').write_text(json.dumps(records,indent=2)+'\n');print('3cataloguepackageappearancesupdated;17modelsretained;T1dotpin1andR7manualformdeclared')

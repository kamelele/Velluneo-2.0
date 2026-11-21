from pathlib import Path
import pcbnew as p,ast,math,shutil,json,hashlib
W=Path(__file__).parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'catalogue-pcb-16/design';D=P/'visualisation-18';V=D/'scene';M=V/'models';M.mkdir(parents=True,exist_ok=True)
U=1/2.54
for n in ast.parse((W/'build_render12.py').read_text()).body:
 if isinstance(n,ast.FunctionDef)and n.name in ('vec','mat','box','mesh','cylinder','lead','save'):exec(compile(ast.Module(body=[n],type_ignores=[]),'helpers','exec'))
old=P/'pcb-render-12/scene/models'
keep=['R_0603_1608Metric.wrl','R_0805_2012Metric.wrl','R_1206_3216Metric.wrl','R_2512_6332Metric.wrl','D_SMA.wrl','D_SMB.wrl','SOT-23-6.wrl','CP_Elec_6.3x5.8.wrl','radial_D10_P5_H20.wrl','ceramic_fuse.wrl','LICENSE.md']
for name in keep:shutil.copyfile(old/name,M/name)
black='.025 .028 .032';silver='.72 .73 .74';yellow='.90 .64 .08';gray='.095 .10 .105'
t=box((0,0,1.8),(26.5,22.5,2.6),black)+box((0,0,12.3),(17.5,17.5,20),yellow)
for x in(-10.5,10.5):t+=box((x,0,14.5),(5.5,13.5,24),gray)
t+=box((0,0,25.5),(26.5,13.5,2),gray)
pins={'1':[-10,7.62],'2':[-5,7.62],'3':[0,7.62],'5':[10,7.62],'6':[10,-7.62],'7':[5,-7.62],'8':[0,-7.62],'9':[-5,-7.62],'10':[-10,-7.62]}
for x,y in pins.values():t+=box((x,-y,-1.8),(.64,.64,4.4),silver,True)
save('MYRRA74032_factory_envelope',t)
# TO-3PF representative body with open mounting hole; dimensions bound to reserved envelope.
t=box((0,0,14.9),(15.7,5.7,16.8),black)
n=96;pts=[];cx,cz=0,26.5;rx,rz=7.85,3.2
for y in(-2.85,2.85):
 for ring in('outer','inner'):
  for i in range(n):
   a=2*math.pi*i/n;co,si=math.cos(a),math.sin(a);r=min(rx/max(abs(co),1e-9),rz/max(abs(si),1e-9))if ring=='outer'else 1.65;pts.append((r*co,y,cz+r*si))
faces=[]
for i in range(n):
 j=(i+1)%n;faces.extend([[i,j,n+j,n+i],[2*n+i,3*n+i,3*n+j,2*n+j],[i,2*n+i,2*n+j,j],[n+i,n+j,3*n+j,3*n+i]])
t+=mesh(pts,faces,black)
for x in(-5.45,0,5.45):t+=box((x,0,.7),(.85,1.,4.6),silver,True)+box((x,0,4.75),(2.2,1.,3.5),silver,True)
save('STFW2N105K5_straight_29p7',t)
t=box((0,0,5),(18,7.5,7.5),'.76 .75 .65')
for s in(-1,1):t+=box((s*11.35,0,.35),(4,9.3,.7),silver,True)+lead((s*9,0,4),(s*11.35,0,.7),.5)
save('AC05AT_factory_WSZ',t)
t=box((0,0,1.85),(6.5,8.51,2.9),black)
for x in(-2.605,2.605):
 for y in(-4.37,4.37):t+=box((x,y,.2),(.85,1.4,.4),silver,True)
save('SDB107_factory_SDB1',t)
t=box((0,0,.925),(4.6,5,1.8),'.57 .39 .20')
for x in(-2.45,2.45):t+=box((x,0,.925),(.8,5,1.85),silver,True)
save('ceramic_2220_1p85',t)
b=p.LoadBoard(str(S/'Velluneo_driver.kicad_pcb'));assigned=[]
for f in b.GetFootprints():
 r=f.GetReference();f.Models().clear()
 if r in('J1','J2'):continue
 m=p.FP_3DMODEL();m.m_Scale.x=m.m_Scale.y=m.m_Scale.z=1
 fp=str(f.GetFPID().GetLibItemName())
 if r.startswith('R'):
  size=next((sz for sz in('2512_6332','1206_3216','0603_1608','0805_2012')if sz[:4]in fp),'0603_1608'if r=='RT1'else'0805_2012');name='R_'+size+'Metric.wrl'
  if r=='R1':name='AC05AT_factory_WSZ.wrl'
 elif r in('D1','D2','D3','TVS1'):name='D_SMB.wrl'if r=='TVS1'else'D_SMA.wrl'
 elif r=='U1':name='SOT-23-6.wrl';m.m_Rotation.z=90
 elif r=='C4':name='CP_Elec_6.3x5.8.wrl'
 else:name={'T1':'MYRRA74032_factory_envelope','Q1':'STFW2N105K5_straight_29p7','BR1':'SDB107_factory_SDB1','C1':'radial_D10_P5_H20','C2':'ceramic_2220_1p85','C3':'ceramic_2220_1p85','F1':'ceramic_fuse'}[r]+'.wrl'
 assert (M/name).is_file(),name
 m.m_Filename='${KIPRJMOD}/models/'+name;f.Add3DModel(m)
 assigned.append(dict(ref=r,footprint=fp,model=name,kind='Package appearance / original envelope, not qualified supplier STEP'))
options=b.GetPlotOptions();selection=options.GetLayerSelection();selection.RemoveLayer(p.F_Paste);selection.RemoveLayer(p.B_Paste);options.SetLayerSelection(selection)
scene=V/'Velluneo_C16_VISUAL_ONLY.kicad_pcb';p.SaveBoard(str(scene),b)
for ext in('.kicad_pro','.kicad_dru'):shutil.copyfile(S/('Velluneo_driver'+ext),scene.with_suffix(ext))
def native(board):
 return dict(parts=sorted((f.GetReference(),f.GetValue(),f.GetFieldText('MPN'),f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),int(f.GetLayer()))for f in board.GetFootprints()),pads=sorted((f.GetReference(),x.GetNumber(),x.GetNetname(),x.GetPosition().x,x.GetPosition().y,x.GetSize().x,x.GetSize().y,x.GetDrillSize().x,x.GetDrillSize().y,tuple(x.GetLayerSet().Seq()))for f in board.GetFootprints()for x in f.Pads()),copper=sorted((x.GetNetname(),int(x.GetLayer()),x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y,x.GetWidth(p.F_Cu)if isinstance(x,p.PCB_VIA)else x.GetWidth(),x.GetDrillValue()if isinstance(x,p.PCB_VIA)else 0)for x in board.GetTracks()))
assert native(p.LoadBoard(str(S/'Velluneo_driver.kicad_pcb')))==native(p.LoadBoard(str(scene)))
assert len(assigned)==31 and len(native(b)['pads'])==80 and len(native(b)['copper'])==333
source_sha=hashlib.sha256((S/'Velluneo_driver.kicad_pcb').read_bytes()).hexdigest();assert source_sha=='3c13b9d2048a6d6b1c830c75445d27412516f0c0fb03d6c5285b8c2f69067f78'
idx=json.loads((P/'pcb-render-12/model-provenance.json').read_text())
(D/'geometry-and-models.json').write_text(json.dumps(dict(source_commit='cafb6ec53fd55275bfe92ef97a77166a58a93ed3',source_board_sha256=source_sha,scene_sha256=hashlib.sha256(scene.read_bytes()).hexdigest(),parts=33,electronic_models=31,wire_pad_pairs_without_invented_harness_models=2,pads=80,copper_objects=333,native_geometry_identical=True,assignments=assigned,T1_component_side_pins=pins,VRML_Y_is_negative_native_local_Y=True,T1_body_mm=[26.5,22.5,26.5],Q1_lowest_wide_shoulder_mm=3,Q1_height_reservation_mm=29.7,upstream_model_source_commit=idx['model_source_commit'],upstream_download_provenance=idx['downloads'],models=[dict(path=x.name,sha256=hashlib.sha256(x.read_bytes()).hexdigest())for x in sorted(M.glob('*.wrl'))],scope='Presentation-only scene. Exact PCB/pad/copper/component placements unchanged. Generic package bodies/original envelope models; details and mounting hole are representative, not supplier STEP/fit approval. No artificial product photograph, wiring/harness release or changed manufacturing data.'),indent=2)+'\n')
(D/'.gitignore').write_text('.work/\n*.kicad_prl\n')
print('Built current 31-component appearance scene; native33parts80pads333copper exact')


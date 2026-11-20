from pathlib import Path
import pcbnew as p,json,shutil,hashlib,math,ast,subprocess,struct
W=Path(__file__).resolve().parent;P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'supplier-review-13';E=D/'design';O=D/'presentation';M=O/'models';shutil.copytree(P/'pcb-render-12/scene/models',M,dirs_exist_ok=True)
# Reuse original mesh primitives only; no execution of historical scene-builder side effects.
tree=ast.parse((W/'build_render12.py').read_text());functions=[x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name in('vec','mat','box','mesh','cylinder','lead','save')];U=1/2.54;exec(compile(ast.Module(body=functions,type_ignores=[]),'original_mesh_primitives','exec'))
silver='.72 .73 .74'
# Actual AC05 dimensional maximum in the requested raised mounting interface.
n=96;pts=[(x,3.75*math.cos(i*2*math.pi/n),9.25+3.75*math.sin(i*2*math.pi/n))for x in(-9,9)for i in range(n)];faces=[list(range(n-1,-1,-1)),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n]for i in range(n)];t=mesh(pts,faces,'.28 .46 .34')
for sign in(-1,1):
 nodes=[(sign*9,0,9.25),(sign*11.2,0,9.25)]
 for i in range(1,19):
  a=math.pi/2-i*math.pi/36;nodes.append((sign*(11.2+1.5*math.cos(a)),0,7.75+1.5*math.sin(a)))
 nodes.append((sign*12.7,0,-1.4))
 for a,b in zip(nodes,nodes[1:]):t+=lead(a,b,.415)
save('ceramic_power_P25p4',t);shutil.copyfile(M/'ceramic_power_P25p4.wrl',E/'models/R1.wrl')
# SMD fuse: remove fictitious insertion leads from the old appearance model.
t=box((0,0,3.0),(15.0,5.35,5.35),'.80 .79 .73')
for sign in(-1,1):t+=box((sign*6.8,0,3.0),(.9,5.45,5.55),silver,True)
save('ceramic_fuse',t)
# C1 maximum body + mounting allocation, with visible vent. Additional2mmventzone is in drawing, not a part.
t=cylinder((0,0,11.43),5.25,21.86,'.025 .028 .032')+cylinder((0,0,22.43),5.0,.14,silver)+cylinder((0,0,.6),5,.2,'.09 .095 .10')
t+=box((0,0,22.515),(6.7,.11,.03),'.25 .26 .27')+box((0,0,22.52),(.11,6.7,.03),'.25 .26 .27')+box((5.17,0,11.5),(.14,1.5,21),'.60 .62 .61')
for x in(-2.5,2.5):t+=lead((x,0,-1.4),(x,0,1),.28)
save('radial_D10_P5_H20',t)
b=p.LoadBoard(str(E/'Velluneo_driver.kicad_pcb'));style=p.LoadBoard(str(P/'pcb-render-12/scene/Velluneo_assembled_RENDER_ONLY.kicad_pcb'));assigned=[]
for f in b.GetFootprints():
 old=next(q for q in style.GetFootprints()if q.GetReference()==f.GetReference()).Models()[0];m=p.FP_3DMODEL();m.m_Filename=old.m_Filename
 for field in('m_Scale','m_Offset','m_Rotation'):
  for axis in('x','y','z'):setattr(getattr(m,field),axis,getattr(getattr(old,field),axis))
 f.Models().clear();f.Add3DModel(m);assigned.append(dict(ref=f.GetReference(),model=m.m_Filename,sha256=hashlib.sha256((M/Path(m.m_Filename).name).read_bytes()).hexdigest()))
opts=b.GetPlotOptions();layers=opts.GetLayerSelection();layers.RemoveLayer(p.F_Paste);layers.RemoveLayer(p.B_Paste);opts.SetLayerSelection(layers)
B=O/'Velluneo_RFQ13_RENDER_ONLY.kicad_pcb';p.SaveBoard(str(B),b);shutil.copyfile(E/'Velluneo_driver.kicad_pro',B.with_suffix('.kicad_pro'))
rows=[]
for side in('top','bottom'):
 out=O/('Velluneo_RFQ13_'+side+'.png');cmd=[str(W/'kicad-10.0.6/bin/kicad-cli.exe'),'pcb','render','--width','2400','--height','1800','--side',side,'--rotate','320,0,35','--perspective','--zoom','.65','--quality','high','--background','opaque','--floor','--light-top','.8','--light-side','.6','--light-camera','.45','--output',str(out),str(B)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180);(O/(side+'-render.log')).write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr;raw=out.read_bytes();size=struct.unpack('>II',raw[16:24]);rows.append(dict(path=out.name,sha256=hashlib.sha256(raw).hexdigest(),actual_pixels=size));shutil.copyfile(out,W.parent/'outputs'/out.name);print('CurrentRFQ13render',side,size,flush=True)
(O/'provenance.json').write_text(json.dumps(dict(source_board_sha256=hashlib.sha256((E/'Velluneo_driver.kicad_pcb').read_bytes()).hexdigest(),render_board_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),models=assigned,renders=rows,source_official_package_assets='OriginalCC-BY-SAKiCadassetheaders/LICENSEretainedfromRENDER12; unchangedfiles sourceURLs/hashes inthatpacket.',corrections='Currentpartposes; SMD F1withoutfictitiousleads; cylindricalraisedR1; maxallocatedC1body. Generic/customappearance remainsillustrative, not suppliermechanicalapproval. DimensionedRFQdrawingiscontrollinginterface.'),indent=2)+'\n')

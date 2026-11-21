from pathlib import Path
import pcbnew as pcb,urllib.request,json,re,math,hashlib,shutil,concurrent.futures
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';S=R/'hardware/E27/workflow/specification-reset/pcb-toolkit-11/design';D=S.parent.parent/'pcb-render-12';M=D/'scene/models';M.mkdir(parents=True,exist_ok=True);idx=json.loads((W/'render12-model-index.json').read_text());revision=idx['sha'];inventory={x['path']:x for x in idx['tree']};sources=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def download(name):
 url='https://raw.githubusercontent.com/KiCad/kicad-packages3D/'+revision+'/'+name;data=urllib.request.urlopen(url,timeout=45).read();p=M/Path(name).name;p.write_bytes(data);return dict(path=p.name,source=url,sha256=sha(p))
names=['Resistor_SMD.3dshapes/R_'+p+'_Metric.wrl'for p in []]
names=['Resistor_SMD.3dshapes/R_'+p+'Metric.wrl'for p in ('0603_1608','0805_2012','1206_3216','2512_6332')]+['Diode_SMD.3dshapes/D_SMA.wrl','Diode_SMD.3dshapes/D_SMB.wrl','Package_TO_SOT_SMD.3dshapes/SOT-23-6.wrl','Capacitor_SMD.3dshapes/CP_Elec_6.3x5.8.wrl']
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:sources=list(pool.map(download,names))
download('LICENSE.md')
U=1/2.54
def vec(v):return' '.join('%.7f'%(x*U)for x in v)
def mat(c,metal=False):return'appearance Appearance { material Material { diffuseColor '+c+' specularColor '+('.65 .65 .65'if metal else'.12 .12 .12')+' shininess '+('.7'if metal else'.26')+' } }'
def box(pos,size,c,metal=False):return'Transform { translation '+vec(pos)+' children [ Shape { '+mat(c,metal)+' geometry Box { size '+vec(size)+' } } ] }\n'
def mesh(points,faces,c,metal=False):return'Shape { '+mat(c,metal)+' geometry IndexedFaceSet { creaseAngle .5 solid FALSE coord Coordinate { point ['+','.join(vec(p)for p in points)+'] } coordIndex ['+','.join(' '.join(map(str,f))+' -1'for f in faces)+'] } }\n'
def cylinder(pos,r,h,c,n=96):
 points=[(pos[0]+r*math.cos(i*2*math.pi/n),pos[1]+r*math.sin(i*2*math.pi/n),pos[2]+z)for z in(-h/2,h/2)for i in range(n)];faces=[list(range(n-1,-1,-1)),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n]for i in range(n)];return mesh(points,faces,c,c.startswith('.7'))
def lead(a,b,r=.28,c='.72 .73 .74',n=16):
 v=[b[i]-a[i]for i in range(3)];L=math.sqrt(sum(x*x for x in v));v=[x/L for x in v];seed=(1,0,0)if abs(v[0])<.8 else(0,1,0);u=[v[1]*seed[2]-v[2]*seed[1],v[2]*seed[0]-v[0]*seed[2],v[0]*seed[1]-v[1]*seed[0]];l=math.sqrt(sum(x*x for x in u));u=[x/l for x in u];t=[v[1]*u[2]-v[2]*u[1],v[2]*u[0]-v[0]*u[2],v[0]*u[1]-v[1]*u[0]]
 points=[tuple(end[k]+r*(u[k]*math.cos(i*2*math.pi/n)+t[k]*math.sin(i*2*math.pi/n))for k in range(3))for end in(a,b)for i in range(n)];return mesh(points,[[i,(i+1)%n,(i+1)%n+n,i+n]for i in range(n)]+[list(range(n-1,-1,-1)),list(range(n,2*n))],c,True)
def save(name,text):p=M/(name+'.wrl');p.write_text('#VRML V2.0 utf8\n# Original parametric appearance model; visualization only, not supplier qualification.\n'+text,encoding='utf-8');return p.name
gray='.09 .095 .10';silver='.72 .73 .74';yellow='.88 .59 .075';black='.025 .028 .032'
# Chip ceramic bodies have metal end terminations at the actual 2220 size.
t=box((0,0,1.05),(4.6,5.0,2.0),'.57 .39 .20')
for x in(-2.45,2.45):t+=box((x,0,1.05),(.8,5.0,2.05),silver,True)
save('ceramic_2220',t)
# Radial capacitor matches selected D10/P5/H20 form, with can, sleeve, vent and leads.
t=cylinder((0,0,10.55),5,19.7,black)+cylinder((0,0,20.43),4.77,.13,silver)+cylinder((0,0,.62),4.7,.3,gray)
t+=box((0,0,20.51),(6.4,.11,.035),'.25 .26 .27')+box((0,0,20.515),(.11,6.4,.035),'.25 .26 .27')
for x in(-2.5,2.5):t+=lead((x,0,-1.4),(x,0,1.0),.28)
# A light sleeve strip indicates polarity; it is appearance, not an assembly authority.
t+=box((4.92,0,10.5),(.14,1.5,18.8),'.60 .62 .61');save('radial_D10_P5_H20',t)
# Horizontal ceramic power resistor, leads formed to the selected P25.4mm pads.
t=box((0,0,4.15),(17.8,7.3,7.7),'.76 .75 .65')
for s in(-1,1):t+=lead((s*12.7,0,-1.0),(s*12.7,0,3.8),.35)+lead((s*12.7,0,3.8),(s*8.9,0,3.8),.35)
save('ceramic_power_P25p4',t)
# W10G-style round bridge and Schurter-style ceramic fuse, both generic appearance.
t=cylinder((0,0,6.4),4.9,5,black)
for x in(-2.75,2.75):
 for y in(-2.75,2.75):t+=lead((x,y,-1.2),(x,y,4.2),.3)
save('round_bridge_formed',t)
t=box((0,0,3.0),(15.0,5.1,5.6),'.80 .79 .73')
for s in(-1,1):t+=box((s*6.8,0,3),(.9,5.3,5.8),silver,True)+lead((s*6.875,0,-1.0),(s*6.875,0,1),.28)
save('ceramic_fuse',t)
# Fully insulated TO220F appearance with an actual open mounting hole.
t=box((0,2.3,11.8),(10.3,4.5,10.6),black);n=96;points=[]
for y in(1.35,3.25):
 for ring in('outer','inner'):
  for i in range(n):
   a=2*math.pi*i/n;co,si=math.cos(a),math.sin(a);r=min(5.15/max(abs(co),1e-9),2.8/max(abs(si),1e-9))if ring=='outer'else 1.6;points.append((r*co,y,19.8+r*si))
faces=[]
for i in range(n):
 j=(i+1)%n;faces.extend([[i,j,n+j,n+i],[2*n+i,3*n+i,3*n+j,2*n+j],[i,2*n+i,2*n+j,j],[n+i,n+j,3*n+j,3*n+i]])
t+=mesh(points,faces,black)
for x,y in[(-2.54,0),(0,-5.08),(2.54,0)]:t+=lead((x,y,-1.3),(x,y,2.2),.3)+lead((x,y,2.2),(x,2.3,6.7),.3)
save('TO220F_staggered',t)
# Custom EFD25 assembly appearance stays within the retained 30x30x18 envelope.
t=box((0,0,1.4),(28,26,1.5),black)+box((0,0,7.8),(18.5,18.6,11),yellow)
for y in(-9.8,9.8):t+=box((0,y,7.7),(23,1.2,12.0),black)
for x in(-10.7,10.7):t+=box((x,0,9.2),(4.1,10.2,14.2),gray)
t+=box((0,0,15.75),(25.5,10.2,2.4),gray)
for z in(4.1,5.1,6.1,7.1,8.1,9.1,10.1,11.1,12.1):t+=box((0,-9.36,z),(17.3,.07,.14),'.67 .36 .045')
for y in(-11.25,11.25):
 for x in(-10,-5,0,5,10):t+=lead((x,y,-1.5),(x,y,3),.32)
save('EFD25_custom_appearance',t)
for ref,colors in [('J1',['.30 .15 .065','.09 .23 .58']),('J2',['.65 .025 .025','.025 .027 .03'])]:
 t=''
 for x,c in zip((-3.81,3.81),colors):t+=lead((x,0,-1),(x,0,2.2),.35)+cylinder((x,0,6.2),.63,8,c)+cylinder((x,0,10.7),.34,1,silver)
 save(ref+'_wires',t)
board=pcb.LoadBoard(str(S/'Velluneo_driver.kicad_pcb'));assigned=[]
for f in board.GetFootprints():
 ref=f.GetReference();old=f.Models()[0]if len(f.Models())else None
 model=pcb.FP_3DMODEL();model.m_Scale.x=model.m_Scale.y=model.m_Scale.z=1
 if ref.startswith('R')and ref not in('R1','RT1'):
  size='2512_6332'if ref in('R2','R3','R10','R11','R12','R14','R15','R16','R17')else'1206_3216'if ref=='R9'else'0603_1608'if ref in('R6','R8','R13')else'0805_2012';name='R_'+size+'Metric.wrl';kind='KiCad generic package'
 elif ref=='RT1':name='R_0603_1608Metric.wrl';kind='Generic0603 appearance for NTC'
 elif ref in('D1','D2','D3','TVS1'):name='D_SMB.wrl'if ref=='TVS1'else'D_SMA.wrl';kind='KiCad generic package'
 elif ref=='U1':name='SOT-23-6.wrl';model.m_Rotation.z=90;kind='KiCad generic package, rotated90degrees'
 elif ref=='C4':name='CP_Elec_6.3x5.8.wrl';kind='KiCad generic package'
 else:
  name={'C1':'radial_D10_P5_H20','C2':'ceramic_2220','C3':'ceramic_2220','R1':'ceramic_power_P25p4','BR1':'round_bridge_formed','Q1':'TO220F_staggered','F1':'ceramic_fuse','T1':'EFD25_custom_appearance','J1':'J1_wires','J2':'J2_wires'}[ref]+'.wrl';kind='Original parametric appearance model; not supplier mechanical approval'
 model.m_Filename='${KIPRJMOD}/models/'+name;f.Models().clear();f.Add3DModel(model);assigned.append(dict(ref=ref,model=name,basis=kind))
options=board.GetPlotOptions();selection=options.GetLayerSelection();selection.RemoveLayer(pcb.F_Paste);selection.RemoveLayer(pcb.B_Paste);options.SetLayerSelection(selection)
out=D/'scene/Velluneo_assembled_RENDER_ONLY.kicad_pcb';pcb.SaveBoard(str(out),board)
for ext in('.kicad_pro','.kicad_sch','.kicad_dru'):shutil.copyfile((S/'Velluneo_driver.kicad_pcb').with_suffix(ext),out.with_suffix(ext))
shutil.copyfile(S/'BOM.csv',D/'BOM-reference.csv')
(D/'model-provenance.json').write_text(json.dumps(dict(source_board=str((S/'Velluneo_driver.kicad_pcb').relative_to(R)),source_sha256=sha(S/'Velluneo_driver.kicad_pcb'),render_sha256=sha(out),model_source_commit=revision,downloads=sources,assignments=assigned,scope='Presentation-only assembly appearance. Native component/pad/track locations unchanged. Generic package models and custom transformer/formed-part appearances are not exact supplier fit or qualified assembly. No electrical project edits.'),indent=2)+'\n',encoding='utf-8')
print('Built assembled appearance scene:',len(assigned),'placements,',len(sources),'official package models')

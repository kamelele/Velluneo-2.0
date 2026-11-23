from pathlib import Path
import json,math,hashlib,shutil,sys
import pcbnew as k
ROOT=Path.cwd();S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';O=ROOT/'outputs/SC09_zarowka_3D';H=ROOT/'work/sc09-lamp'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(S/'SC09_compact.kicad_pcb')=='a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19'
WHITE=(.83,.86,.89);METAL=(.56,.59,.63);LED=(.95,.72,.17);GREEN=(.08,.27,.17)
parts=[]
def mesh(v,fs,color,trans=0):parts.append((v,fs,color,trans))
def xyz(a,u,v):return (a-55,u,v+5.75)
def ring(a0,a1,r0,r1,color,wall=None,cut=False,trans=0,slots=False,n=128):
 # Hollow lathe wall or closed solid cylinder. Axis is lamp a (PCB x).
 rs=[r0,r1] if wall is None else [r0,r1,r1-wall,r0-wall]
 aa=[a0,a1] if wall is None else [a0,a1,a1,a0]
 vv=[xyz(a,r*math.cos(2*math.pi*i/n),r*math.sin(2*math.pi*i/n))for a,r in zip(aa,rs)for i in range(n)]
 ff=[]
 for j in range(len(rs)-1):
  for i in range(n):
   th=2*math.pi*(i+.5)/n
   if cut and math.sin(th)>.001:continue
   if slots and j in [0,2]and i%16 in [2,3,4]:continue
   ff.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 if wall is None:
  for j in [0,1]:
   ids=[j*n+i for i in range(n)if not cut or math.sin(2*math.pi*i/n)<=.001]
   ff.append(tuple(reversed(ids))if j==0 else tuple(ids))
 else:
  for i in range(n):
   th=2*math.pi*(i+.5)/n
   if cut and math.sin(th)>.001:continue
   ff.append((3*n+i,3*n+(i+1)%n,(i+1)%n,i))
 mesh(vv,ff,color,trans)
def box(a,u,v,da,du,dv,c):
 vv=[xyz(a+sa*da/2,u+su*du/2,v+sv*dv/2)for sa,su,sv in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
 mesh(vv,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],c)
def rod(p,q,r=.45,c=(.65,.08,.05),n=12):
 # small wire segment between lamp-coordinate vertices
 import numpy as np
 p,q=map(lambda x:np.array(x,dtype=float),[p,q]);d=q-p;d/=np.linalg.norm(d);t=np.cross(d,[0,0,1]);
 if np.linalg.norm(t)<.01:t=np.cross(d,[0,1,0])
 t/=np.linalg.norm(t);w=np.cross(d,t)
 vv=[xyz(*(end+r*(t*math.cos(i*2*math.pi/n)+w*math.sin(i*2*math.pi/n))))for end in [p,q]for i in range(n)]
 mesh(vv,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],c)
def build(cut=False):
 parts.clear()
 # Simplified E27 visual envelope, not thread-gauge CAD.
 ring(0,2,4,5,(.25,.26,.28));ring(2,5,10,12,(.16,.17,.18));ring(5,26,12.5,12.5,METAL)
 for a in [7,10.6,14.2,17.8,21.4,25]:ring(a,a+.8,13.5,13.5,(.68,.70,.72))
 # Structural plastic shell: 2mm wall, 30mm lowerOD to78mm upperOD.
 rad=lambda a:15+(a-26)*24/84
 for a0,a1 in [(26,29),(29,32),(32,104),(104,108),(108,110)]:ring(a0,a1,rad(a0),rad(a1),WHITE,wall=2,cut=cut,slots=a0 in [29,104])
 # Panel 72mm aluminium, LED faces toward dome. No electrical routing claim.
 ring(110,111.6,36,36,(.69,.72,.74),cut=cut)
 ring(111.6,111.7,35.8,35.8,(.91,.93,.94),cut=cut)
 for r,shift in [(22,0),(30,.5)]:
  for i in range(10):
   th=2*math.pi*(i+shift)/10;u,v=r*math.cos(th),r*math.sin(th)
   if cut and v>0:continue
   box(112.05,u,v,.7,3,3,(.95,.95,.91));box(112.43,u,v,.06,2.25,2.25,LED)
 # Continuous diffuser lathe, shared vertices for smooth surface.
 N=128;M=40;vv=[]
 for inner in [False,True]:
  for j in range(M+1):
   th=j*math.pi/(2*M);a=111.6+(30.8 if inner else 32)*math.sin(th);r=max(.01,(37.8 if inner else 39)*math.cos(th))
   for i in range(N):vv.append(xyz(a,r*math.cos(2*math.pi*i/N),r*math.sin(2*math.pi*i/N)))
 ff=[];off=(M+1)*N
 for inner in [False,True]:
  o=off if inner else 0
  for j in range(M):
   for i in range(N):
    if cut and math.sin(2*math.pi*(i+.5)/N)>.001:continue
    f=(o+j*N+i,o+j*N+(i+1)%N,o+(j+1)*N+(i+1)%N,o+(j+1)*N+i);ff.append(tuple(reversed(f))if inner else f)
 for i in range(N):
  if cut and math.sin(2*math.pi*(i+.5)/N)>.001:continue
  ff.append((i,off+i,off+(i+1)%N,(i+1)%N))
 mesh(vv,ff,(.92,.94,.96),.08)
 # Illustrative screw posts/panel support; positions outside protected board envelope.
 for u in [-30,30]:box(105.5,u,0,9,5,5,WHITE)
 # Two illustrative LED leads, no selectable connector implementation.
 for u,c in [(-9,(.65,.06,.04)),(-6,(.08,.09,.10))]:
  for p,q in [((106.2,u,-6),(108.5,u,-6)),((108.5,u,-6),(109.6,u,-3))]:rod(p,q,c=c)
 name='SC09_lamp_cutaway'if cut else'SC09_lamp_closed';lines=['#VRML V2.0 utf8','# Engineering concept, mm mapped toKiCadVRMLunits/2.54. No safety/thermal/production qualification.']
 for v,fs,c,tr in parts:
  coords=', '.join(' '.join(f'{z/2.54:.7f}'for z in p)for p in v);idx=', '.join(','.join(map(str,f))+',-1'for f in fs)
  lines.append('Shape { appearance Appearance { material Material { diffuseColor '+' '.join(map(str,c))+f' transparency {tr} specularColor .15 .15 .15 shininess .3'+' } } geometry IndexedFaceSet { solid FALSE creaseAngle .7 coord Coordinate { point [ '+coords+' ] } coordIndex [ '+idx+' ] } }')
 mp=O/(name+'.wrl');mp.write_text('\n'.join(lines))
 b=k.LoadBoard(str(S/'SC09_compact.kicad_pcb'))
 for f in b.GetFootprints():
  for m in f.Models():m.m_Filename=m.m_Filename.replace('${KIPRJMOD}',S.as_posix())
 f=k.FOOTPRINT(b);f.SetReference('CONCEPT');f.SetValue('Lamp envelope');f.SetPosition(k.VECTOR2I(k.FromMM(99.4),k.FromMM(115.9)));m=k.FP_3DMODEL();m.m_Filename=mp.as_posix();f.Add3DModel(m);b.Add(f)
 k.SaveBoard(str(O/(name+'.kicad_pcb')),b)
for cut in [False,True]:build(cut)
# Conservative box fit, independent of visual component bodies. 19.5mm includes both faces.
board={'length_axial_mm':51.2,'width_mm':33,'total_thickness_mm':19.5,'start_axial_mm':55,'end_axial_mm':106.2}
corner=math.hypot(16.5,9.75);inside=13+(55-26)*24/84
report={'revision':'SC09-LAMP-CONCEPT01','PCB_source_sha256':sha(S/'SC09_compact.kicad_pcb'),'PCB_source_unchanged':True,'dimensions_mm':{'overall_diameter':78,'overall_length':143.6,'plastic_body_length':84,'simplified_E27_length':26,'diffuser_height':32,'panel_diameter':72,'panel_thickness':1.6,'plastic_wall_nominal':2},'board':board,'fit_check':{'method':'Entire51.2x33x19.5conservative rectangularenvelope centredradially; circularlinearconeinnerwall; nogeometryfromphotosclaimedexact','corner_radius_mm':corner,'minimum_inside_radius_along_board_mm':inside,'minimum_radial_gap_mm':inside-corner,'axial_gap_board_to_panel_underside_mm':110-106.2,'ideal_envelope_pass':inside-corner>=2,'allowance_not_safety_clearance':'2mmmechanicalplanningreserve,notIEC230Vinsulationacceptance','remaining':'Actualformedleads,wires,mounting,tolerances,ventaccessibility,electricalbarriers,LEDMCPCBdesignandthermalsneedqualification.'},'visual_limits':['ActualSC09PCB/placement retained without resizing','20LED positions illustrative only; not completedLEDPCB','E27simplifiedenvelope,notmanufacturingthread','No18650orbatteryfunctions','Enclosureconceptdimensionsproposed,notreconstructedfromphotos','NativeillustrativemodelsnotcertifiedsupplierSTEP'],'temperature_or_electrical_release':False}
(O/'SC09_lamp_dimensions_and_fit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['fit_check'],indent=2))
assert sha(S/'SC09_compact.kicad_pcb')==report['PCB_source_sha256']

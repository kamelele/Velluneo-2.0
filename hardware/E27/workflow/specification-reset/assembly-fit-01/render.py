"""Deterministic envelope preview from the same calculated world geometry.
Pillow raster + equivalent SVG paths; no image generation, external CAD rendering or physical observation.
"""
from pathlib import Path
import json,math,argparse,html
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent
C=json.loads((D/'assembly-contract.json').read_text(encoding='utf-8'));R=json.loads((D/'results.json').read_text(encoding='utf-8'));LAY=json.loads((D/'packing-diagnostic.json').read_text(encoding='utf-8'))
class Canvas:
 def __init__(self):
  self.im=Image.new('RGB',(1800,1250),'#f4f7fa');self.dr=ImageDraw.Draw(self.im,'RGBA');self.svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1250" viewBox="0 0 1800 1250"><rect width="1800" height="1250" fill="#f4f7fa"/>']
 def poly(self,p,fill,stroke=None,width=1):
  if len(p)<2:return
  self.dr.polygon(p,fill=fill,outline=stroke,width=width)
  fc=fill or(0,0,0,0);ss=f' stroke="rgb{stroke[:3]}" stroke-opacity="{stroke[3]/255}" stroke-width="{width}"'if stroke else''
  self.svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}'for x,y in p)+f'" fill="rgb{fc[:3]}" fill-opacity="{fc[3]/255}"'+ss+'/>')
 def line(self,p,col=(61,79,100,255),w=2):
  self.dr.line(p,fill=col,width=w);self.svg.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}'for x,y in p)+f'" fill="none" stroke="rgb{col[:3]}" stroke-opacity="{col[3]/255}" stroke-width="{w}"/>')
 def rect(self,b,col,stroke=None,w=1):self.poly([(b[0],b[1]),(b[2],b[1]),(b[2],b[3]),(b[0],b[3])],col,stroke,w)
 def circle(self,x,y,r,col,stroke=None,w=1):self.poly([(x+r*math.cos(a*math.tau/96),y+r*math.sin(a*math.tau/96))for a in range(96)],col,stroke,w)
 def text(self,x,y,s,size=20,col=(25,44,62,255),bold=False):
  try:f=ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf'if bold else'segoeui.ttf'),size)
  except OSError:f=ImageFont.load_default(size=size)
  self.dr.text((x,y),s,font=f,fill=col);self.svg.append(f'<text x="{x}" y="{y+size*.83}" fill="rgb{col[:3]}" font-family="Segoe UI,sans-serif" font-size="{size}"'+(' font-weight="700"'if bold else'')+'>'+html.escape(s)+'</text>')
 def save(self,png,svg):
  if png:self.im.save(png)
  if svg:Path(svg).write_text(''.join(self.svg)+'</svg>\n',encoding='utf-8',newline='\n')
COL={'cup':(189,139,74,110),'metal':(123,139,155,230),'board':(34,124,110,255),'T1':(40,69,104,255),'C1':(65,131,165,255),'R1':(195,148,67,255),'small':(88,101,117,255),'panel':(76,153,129,255),'led':(244,201,86,255),'reserve':(166,127,190,125),'diffuser':(174,205,224,65)}
faces=[];obj=[]
def add(name,verts,polys,color,category='part'):
 offset=len(obj);obj.extend(verts)
 for pp in polys:faces.append({'name':name,'p':[verts[i]for i in pp],'col':color,'cat':category,'idx':[i+offset+1 for i in pp]})
def box(name,b,col,category='part'):
 x,d,z,X,E,Z=b;v=[(x,d,z),(X,d,z),(X,E,z),(x,E,z),(x,d,Z),(X,d,Z),(X,E,Z),(x,E,Z)];add(name,v,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],col,category)
def disk_ring(name,outer,inner,z0,z1,col,category='housing',n=48,inner_center=(0,0)):
 # Inner radial outline may be offset/rounded, supplied as sampled ray distances.
 v=[]
 for z in(z0,z1):
  v += [((outer[i]if isinstance(outer,list)else outer)*math.cos(i*math.tau/n),(outer[i]if isinstance(outer,list)else outer)*math.sin(i*math.tau/n),z)for i in range(n)]
  v += [(inner_center[0]+(inner[i]if isinstance(inner,list)else inner)*math.cos(i*math.tau/n),inner_center[1]+(inner[i]if isinstance(inner,list)else inner)*math.sin(i*math.tau/n),z)for i in range(n)]
 pp=[]
 for i in range(n):
  j=(i+1)%n;pp += [(i,j,j+2*n,i+2*n),(i+n,i+3*n,j+3*n,j+n),(i,j,j+n,i+n),(i+2*n,i+3*n,j+3*n,j+2*n)]
 add(name,v,pp,col,category)
def cylinder_normal(name,x,z,d0,d1,rad,col,n=32):
 v=[(x+rad*math.cos(i*math.tau/n),d,z+rad*math.sin(i*math.tau/n))for d in(d0,d1)for i in range(n)];p=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];add(name,v,p,col)
def revolve(name,profile,col,category='housing',n=48):
 v=[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z)for z,r in profile for i in range(n)];pp=[]
 for k in range(len(profile)-1):
  for i in range(n):j=(i+1)%n;pp.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 add(name,v,pp,col,category)
def rr_path(b,r,n=12):
 x,d,X,E=b;pts=[]
 for cx,cy,a in[(X-r,E-r,0),(x+r,E-r,90),(x+r,d+r,180),(X-r,d+r,270)]:
  for i in range(n+1):th=math.radians(a+i*90/n);pts.append((cx+r*math.cos(th),cy+r*math.sin(th)))
 return pts
# rr_path above starts at rightmost and walks anticlockwise in the XD plane.
def rr_sdf(x,d,b,r):
 x0,d0,x1,d1=b;qx=abs(x-(x0+x1)/2)-(x1-x0)/2+r;qy=abs(d-(d0+d1)/2)-(d1-d0)/2+r;return math.hypot(max(qx,0),max(qy,0))+min(max(qx,qy),0)-r
def radial_rr(b,r,n=48):
 out=[]
 for i in range(n):
  a=i*math.tau/n;lo,hi=0.,45.
  for _ in range(40):
   mid=(lo+hi)/2
   if rr_sdf(mid*math.cos(a),mid*math.sin(a),b,r)<=0:lo=mid
   else:hi=mid
  out.append((lo+hi)/2)
 return out
# Primary cap is a labelled procurement envelope, thread-like rings are illustrative, not IEC gauge CAD.
revolve('E27_envelope',[(0,4),(1,9),(3,13.5),(26,14),(27,14)],(123,133,145,255),'cap')
for z in(7,10.5,14,17.5,21,24.5):disk_ring('E27_illustrative_ring',14.2,13.5,z,z+.45,(95,108,123,255),'cap')
# Piece-specific split: uppercupopenbottom40; narrowjoiner/nose are installedAFTERPCBloading.
revolve('lower_flared_nose_outer',[(27,14.5),(30,20.5),(40,29.6)],COL['cup'])
disk_ring('uppercup_wide_mouth_wall',29.6,28.1,40,56,COL['cup'])
inner_upper=radial_rr(C['cup']['upper_inside_X_D_box_mm'],.5)
outer_upper=radial_rr(C['cup']['upper_outer_X_D_box_mm'],2)
disk_ring('uppercup_transition_wall',29.6,inner_upper,56,63,COL['cup'])
disk_ring('uppercup_D_wall',outer_upper,inner_upper,63,92.5,COL['cup'])
disk_ring('removable_lid',outer_upper,6.2,92.5,94,COL['cup'],inner_center=(0,3))
def sleeve_segment(name,z0,z1,ro0,ri0,ro1,ri1):
 n=48;vv=[]
 for z,rad in[(z0,ro0),(z0,ri0),(z1,ro1),(z1,ri1)]:vv +=[(rad*math.cos(i*math.tau/n),rad*math.sin(i*math.tau/n),z)for i in range(n)]
 pp=[]
 for i in range(n):
  j=(i+1)%n;pp +=[(i,j,j+2*n,i+2*n),(i+n,i+3*n,j+3*n,j+n),(i,j,j+n,i+n),(i+2*n,i+3*n,j+3*n,j+2*n)]
 add(name,vv,pp,(159,104,58,190),'housing')
sleeve_segment('removable_joiner_lower',34,40,24.14-2.05,24.14-3.55,29.6-2.05,29.6-3.55)
sleeve_segment('removable_joiner_upper',40,42,29.6-2.05,29.6-3.55,29.6-2.05,29.6-3.55)
for name,zs in[('nose',C['support']['bottom_cradle_Z_mm']),('lid',C['support']['top_cradle_Z_mm'])]:
 for xs in C['support']['bottom_left_right_X_intervals_mm']if name=='nose'else C['support']['left_right_X_intervals_mm']:
  for ds in C['support']['D_flange_intervals_mm']:box(name+'_endcradle',[xs[0],ds[0],zs[0],xs[1],ds[1],zs[1]],(177,126,69,255),'housing')
# Power board remains a 32x60 rectangle, its1.6mm thickness is normal to worldD.
box('rectangular_power_board',[-16,-.2,31,16,1.4,91],COL['board'])
for p in R['part_results']:
 ref=p['ref'];b=p['nominal_box_X_D_Z_mm'];col=COL.get(ref,COL['small'])
 if ref=='C1':cylinder_normal(ref,LAY['positions'][ref]['x_mm'],61-LAY['positions'][ref]['y_mm'],b[1],b[4],5.25,col)
 elif ref=='R1':box(ref,b,COL['R1'])
 else:box(ref,b,col)
# Complete fin rings and spines are in OBJ. Front-half housing surfaces are removed only in preview.
pocket=radial_rr([-19,-6.5,19,22.5],2.5)
for i in range(10):disk_ring('custom_fin_'+str(i),29.8,pocket,64+3*i,65+3*i,COL['metal'])
box('rear_thermal_spine',[-12,-24,63,12,-20,95],COL['metal'],'housing')
for s in(-1,1):
 x0,x1=sorted([s*21.5,s*24.5]);box('side_thermal_spine',[x0,-3,63,x1,5,95],COL['metal'],'housing')
disk_ring('thermal_plate',29,7.2,95,97,COL['metal'],inner_center=(0,3))
# Reserved central interface is offsetD+3. Its detailed connector/bushing is unselected.
disk_ring('round_LED_insert',24,6.2,97.1,98.6,COL['panel'],'panel',inner_center=(0,3))
for i in range(8):
 a=i*math.tau/8;x=16*math.cos(a);d=16*math.sin(a);box('LED_'+str(i+1),[x-1.4,d-1.75,98.6,x+1.4,d+1.75,99.5],COL['led'],'panel')
# Central reservation is shown as translucent volume, not a selected real connector.
v=[(4.8*math.cos(i*math.tau/32),3+4.8*math.sin(i*math.tau/32),z)for z in(92,105)for i in range(32)]
pp=[tuple(range(31,-1,-1)),tuple(range(32,64))]+[(i,(i+1)%32,(i+1)%32+32,i+32)for i in range(32)]
add('service_interface_reservation',v,pp,COL['reserve'],'reserve')
a=29.8;h=19.9;sr=(a*a+h*h)/(2*h);cz=118.5-sr;profile=[]
for i in range(19):
 z=98.6+(118.5-98.6)*i/18;profile.append((z,math.sqrt(max(0,sr*sr-(z-cz)**2))))
revolve('optical_dome',profile,COL['diffuser'],'diffuser')
# All full geometry is retained as non-manufacturing OBJ bounding envelopes.
def save_obj(path):
 ss=['# Conditional bounding envelopes, not watertight/manufacturing CAD or selected real parts.\n']+[f'v {x:.6f} {d:.6f} {z:.6f}\n'for x,d,z in obj];last=None
 for f in faces:
  if f['name']!=last:ss.append('g '+f['name']+'\n');last=f['name']
  ss.append('f '+' '.join(map(str,f['idx']))+'\n')
 Path(path).write_text(''.join(ss),encoding='utf-8',newline='\n')
def draw(lang,output):
 pl=lang=='pl';cv=Canvas();az=math.radians(-54);el=math.radians(16);cam=(math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el));right=(-math.sin(az),math.cos(az),0);up=(-math.sin(el)*math.cos(az),-math.sin(el)*math.sin(az),math.cos(el))
 def proj(p):
  q=(p[0],p[1],p[2]-59.25);return(500+6.8*sum(q[i]*right[i]for i in range(3)),650-6.8*sum(q[i]*up[i]for i in range(3)))
 cv.text(45,28,'Velluneo · przekrój żarówki Ø60 × 120 mm'if pl else'Velluneo · lamp section within the Ø60 × 120 mm target',34,bold=True)
 cv.text(45,80,'Prostokątny zasilacz wzdłuż osi · okrągły, wymienny wkład LED'if pl else'Longitudinal rectangular driver · round replaceable LED insert',24)
 cv.text(45,120,'Model gabarytowy — dopasowanie warunkowe, bez ścieżek'if pl else'Bounding-envelope model — conditional fit, no routing',19,(91,107,125,255))
 order=sorted(faces,key=lambda f:sum(sum(p[i]*cam[i]for i in range(3))for p in f['p'])/len(f['p']))
 for f in order:
  if f['cat']in('housing','diffuser')and sum(p[1]for p in f['p'])/len(f['p'])<0:continue
  if f['cat']=='diffuser'and sum(p[0]for p in f['p'])/len(f['p'])>0:continue
  pts=[proj(p)for p in f['p']];co=f['col'];cv.poly(pts,co,(co[0]//2,co[1]//2,co[2]//2,min(co[3],100)),1)
 # Aligned annotations outside the model with exact anchor endpoints.
 labels=[((0,0,111),'Klosz / dyfuzor'if pl else'Optical diffuser',70,190),((0,0,98),'Wkład LED Ø48 mm'if pl else'Round LED insert Ø48 mm',690,210),((23,0,82),'Radiator pierścieniowy'if pl else'Custom annular radiator',690,370),((0,1,62),'Zasilacz 32 × 60 mm'if pl else'Rectangular driver 32 × 60 mm',45,470),((-5.5,-16,49),'C1: korpus do 22 mm'if pl else'C1: body up to 22 mm',45,720),((0,0,13),'Trzonek E27'if pl else'E27 cap envelope',690,1020)]
 for anchor,text,x,y in labels:
  ap=proj(anchor);end=(x+12,y+30);cv.line([ap,end],(66,87,109,180),2);cv.text(x,y,text,22,bold=True)
 cv.text(55,1125,'Zielony prostokąt: płytka zasilacza. Wycięcie obudowy odsłania obie strony.'if pl else'Green rectangle: driver PCB. Housing cutaway exposes both populated faces.',18)
 cv.text(55,1155,'Radiator, izolator i złącze pokazano jako rezerwy konstrukcyjne.'if pl else'Cooler, insulating cup and connector are construction allocations.',18)
 cv.line([(1035,160),(1035,1190)],(195,205,217,255),2)
 # Side section in worldD/Z. The component coordinates are the calculated boundsexactly.
 cx=1330;top=185;ss=3.85
 def side(d,z):return(cx+d*ss,top+(120-z)*ss)
 cv.text(1090,155,'Widok z boku: grubość zabudowy'if pl else'Side section: populated thickness',23,bold=True)
 # Target rectangular envelope only, not a cylindrical powerboard.
 cv.line([side(-30,0),side(-30,120),side(30,120),side(30,0)],(188,198,209,160),1)
 for sg in(-1,1):
  path=[side(sg*r,z)for z,r in C['cup']['lower_outer_profile_Z_R_mm']];cv.line(path,(175,130,74,255),3)
 for p in sorted(R['part_results'],key=lambda v:v['height']):
  b=p['nominal_box_X_D_Z_mm'];aa=side(b[1],b[5]);bb=side(b[4],b[2]);cv.rect([aa[0],aa[1],bb[0],bb[1]],COL.get(p['ref'],COL['small']))
 cv.rect([side(-.2,91)[0],side(0,91)[1],side(1.4,31)[0],side(0,31)[1]],COL['board'])
 for i in range(10):
  for sg in(-1,1):
   d0,d1=sorted([sg*23.5,sg*29.8]);q0=side(d0,65+3*i);q1=side(d1,64+3*i);cv.rect([q0[0],q0[1],q1[0],q1[1]],COL['metal'])
 cv.line([side(-24,98.6),side(24,98.6)],COL['panel'],6)
 cv.line([side(-r,z)for z,r in profile]+[side(r,z)for z,r in reversed(profile)],(143,179,199,255),2)
 cv.rect([side(-14,27)[0],side(0,27)[1],side(14,1)[0],side(0,1)[1]],(132,145,160,255))
 cv.text(1480,230,'LED / klosz'if pl else'LED / diffuser',18);cv.text(1480,365,'T1: 18 mm'if pl else'T1: 18 mm',18);cv.text(1480,390,'rezerwa'if pl else'allocation',17)
 cv.text(1085,690,'Budżet wymiarów — wymagane tolerancje'if pl else'Dimension budget — required tolerances',22,bold=True)
 cv.text(1090,731,'Wysokość nominalna: 118,5 mm'if pl else'Nominal height: 118.5 mm',22)
 cv.text(1090,764,'Suma tolerancji: do 119,8 mm'if pl else'With allocated tolerance stack: 119.8 mm',22)
 cv.text(1090,797,'Największa średnica: do 59,7 mm'if pl else'Allocated finished diameter: 59.7 mm',22)
 # Two exact transverse sections with driver shown edge-on.
 for z,ccx,title in[(70,1210,'T1 / Z=70 mm'),(48.8,1590,'C1 / Z=48,8 mm'if pl else'C1 / Z=48.8 mm')]:
  ccy=1015;sc=4.5
  def xp(x,d):return(ccx+x*sc,ccy-d*sc)
  cv.text(ccx-110,850,title,20,bold=True)
  cv.circle(ccx,ccy,29.8*sc,(222,229,235,255),(148,164,180,255),1)
  if z>=63:
   op=rr_path(C['cup']['upper_outer_X_D_box_mm'],2);ip=rr_path(C['cup']['upper_inside_X_D_box_mm'],.5)
   gap=rr_path([-19,-6.5,19,22.5],2.5);cv.poly([xp(x,d)for x,d in gap],(244,247,250,255));cv.poly([xp(x,d)for x,d in op],(206,165,107,255));cv.poly([xp(x,d)for x,d in ip],(252,252,249,255))
  else:cv.circle(ccx,ccy,29.6*sc,(206,165,107,255));cv.circle(ccx,ccy,28.1*sc,(252,252,249,255))
  for p in R['part_results']:
   b=p['nominal_box_X_D_Z_mm']
   if b[2]<=z<=b[5]:
    lo=xp(b[0],b[4]);hi=xp(b[3],b[1]);cv.rect([lo[0],lo[1],hi[0],hi[1]],COL.get(p['ref'],COL['small']))
  aa=xp(-16,1.4);bb=xp(16,-.2);cv.rect([aa[0],aa[1],bb[0],bb[1]],COL['board'])
  if z<56:
   b=next(p for p in R['part_results']if p['ref']=='C1')['nominal_box_X_D_Z_mm'];a=xp(b[0],b[1]);e=xp(b[3],b[1]-2);cv.rect([a[0],a[1],e[0],e[1]],(166,127,190,80),(137,98,163,200),1)
 cv.text(1090,1170,'Przekroje obudowy; zielona płytka widziana krawędzią.'if pl else'Housing sections; green driver PCB viewed edge-on.',17)
 cv.text(45,1210,'Wymagają potwierdzenia: gotowy transformator, tolerancje montażu, materiał izolatora, złącze i chłodzenie.'if pl else'Unqualified: finished transformer, assembly tolerances, insulating material, interface and cooling.',18,(104,76,41,255))
 out=Path(output);out.mkdir(exist_ok=True,parents=True)
 if pl:cv.save(str(out/'Velluneo_assembly_cutaway.png'),None)
 else:cv.save(str(out/'assembly-preview.png'),str(out/'assembly-preview.svg'))
 return cv
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--lang',choices=['en','pl'],default='en');ap.add_argument('--output',type=Path,default=D/'.work/preview');args=ap.parse_args();draw(args.lang,args.output)
 if args.lang=='en':save_obj(args.output/'assembly-envelopes.obj')
 print(json.dumps({'language':args.lang,'geometry_faces':len(faces),'physical_driver_components':len(R['part_results']),'source':'Computed body boxes and dimensional contract; no photorealistic or finishedPCBclaim.'}))

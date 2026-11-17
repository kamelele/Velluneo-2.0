from pathlib import Path
import json, numpy as np, math, random, hashlib
D=Path(__file__).resolve().parent
inv=json.loads((D/'native-inventory.json').read_text());parts={p['ref']:p for p in inv['parts']};R=25.5
fixed={'T1':(0,-3,0,'F'),'R1':(0,18.2,0,'F'),'J1':(17.3,10,90,'F'),'J2':(17.3,-10.8,90,'F'),'C1':(-19,-4,90,'B'),'C4':(0,-21.35,0,'B'),'BR1':(-18,10.5,0,'F')}
secondary={'C4','D3','R11','R12','J2'}
def trans(x,y,c):
 a,b,ang,side=c
 if side=='B':y=-y
 if ang==90:x,y=y,-x
 return x+a,y+b

def box(ref,c,key='courtyard_bbox_mm'):
 b=parts[ref][key];xy=[trans(x,y,c)for x in (b[0],b[2])for y in(b[1],b[3])];return [min(x for x,y in xy),min(y for x,y in xy),max(x for x,y in xy),max(y for x,y in xy)]
def pads(ref,c):
 out=[]
 for p in parts[ref]['pads']:
  x,y=trans(*p['xy_mm'],c);w,h=p['size_mm']
  if c[2]==90:w,h=h,w
  out.append([x-w/2,y-h/2,x+w/2,y+h/2])
 return out
obs=[]
for ref,c in fixed.items():
 if c[3]=='B':obs.append((ref,box(ref,c)))
 for p,pad in zip(parts[ref]['pads'],pads(ref,c)):
  if p['tht']:obs.append((ref,[pad[0]-.4,pad[1]-.4,pad[2]+.4,pad[3]+.4]))
xx,yy=np.meshgrid(np.arange(-23,23.01,.5),np.arange(-23,23.01,.5));xy=np.stack((xx.ravel(),yy.ravel()),axis=1)
remaining=[r for r in parts if r not in fixed]
areas={r:(parts[r]['courtyard_bbox_mm'][2]-parts[r]['courtyard_bbox_mm'][0])*(parts[r]['courtyard_bbox_mm'][3]-parts[r]['courtyard_bbox_mm'][1])for r in remaining}
best={};bestobs=None
for seed in range(96):
 rng=random.Random(seed);order=sorted(remaining,key=lambda r:-(areas[r]*(.75+rng.random()*.5)));placed=dict(fixed);occupied=list(obs)
 for r in order:
  options=[]
  for angle in(0,90):
   b=box(r,(0,0,angle,'B'));bs=np.column_stack((xy[:,0]+b[0],xy[:,1]+b[1],xy[:,0]+b[2],xy[:,1]+b[3]));valid=np.ones(len(xy),dtype=bool)
   for a in(0,2):
    for z in(1,3):valid &= bs[:,a]**2+bs[:,z]**2<=R**2
   cb=box(r,(0,0,angle,'B'),'copper_bbox_mm')
   for ca in(0,2):
    for cz in(1,3):valid &= (xy[:,0]+cb[ca])**2+(xy[:,1]+cb[cz])**2<=(R-.5)**2
   # conservative courtyard separation from all opposite-domain metal and same-face bodies
   for rr,bb in occupied:
    gap=8 if ((r in secondary)!=(rr in secondary)) and rr!='T1' else .1
    valid &= (bs[:,2]<=bb[0]-gap)|(bs[:,0]>=bb[2]+gap)|(bs[:,3]<=bb[1]-gap)|(bs[:,1]>=bb[3]+gap)
   # T1 winding body is not on B; individual secondary/primary pads require domain-specific metal reserve
   for p,pad in zip(parts['T1']['pads'],pads('T1',fixed['T1'])):
    ps=p['pin']in('6','7','8','9','10');gap=8 if ps!=(r in secondary)else .4
    valid &= (bs[:,2]<=pad[0]-gap)|(bs[:,0]>=pad[2]+gap)|(bs[:,3]<=pad[1]-gap)|(bs[:,1]>=pad[3]+gap)
   ids=np.where(valid)[0]
   if len(ids):
    target=np.array([0,-19]if r in secondary else[0,3]);cost=((xy[ids]-target)**2).sum(axis=1)+np.random.default_rng(seed+angle+len(r)).random(len(ids))*.1;i=ids[np.argmin(cost)];options.append((cost.min(),tuple([*xy[i],angle,'B']),bs[i].tolist()))
  if options:
   _,c,b=min(options);placed[r]=c;occupied.append((r,b))
 if len(placed)>len(best):best=placed;bestobs=occupied
 if len(best)==len(parts):break
report={'scope':'Analytical candidate using exact native footprints, not KiCad board/placement/DRC. Conservative court boxes, 8mm working domain reserve is NOT an adopted normative minimum. Failed fits are retained.','inventory_sha256':hashlib.sha256((D/'native-inventory.json').read_bytes()).hexdigest(),'circle_study_diameter_mm':51,'selected_product_PCB':False,'toolkit_limitation':'Pinned spatial checker supports rectangular outline only; circular candidate cannot be adopted as a managed spatial contract without explicit tool support/qualified migration.','fixed_T1_finished_envelope_allocation_mm':[30,30,18],'T1_finished_envelope_verified':False,'placed_count':len(best),'total_count':len(parts),'missing_refs':[r for r in parts if r not in best],'positions':{r:dict(x_mm=float(c[0]),y_mm=float(c[1]),angle_deg=c[2],side=c[3],courtyard_bbox_mm=box(r,c),pads=pads(r,c))for r,c in best.items()},'coordinate_convention':'Common front/global XY for both views; B mirrors localY, then positive KiCad-angle rotation(x,y)=(y,-x) at90degrees. Verified against actual footprintFlip/Rotate in memory, not savedPCB.', 'algorithm':'96 deterministic large-first orderings on .5mm grid; both orthogonal orientations; all unfixed SMD on B; fixed BR1 onF. Not proof that other arrangements cannot fit.'}
allpads=[(r,b)for r,c in best.items()for b in pads(r,c)]
miniso=(999,None)
for r,b in allpads:
 for rr,bb in allpads:
  if (r in secondary)==(rr in secondary)or r=='T1'or rr=='T1':continue
  dx=max(0,b[0]-bb[2],bb[0]-b[2]);dy=max(0,b[1]-bb[3],bb[1]-b[3]);dist=math.hypot(dx,dy)
  if dist<miniso[0]:miniso=(dist,[r,rr])
# T1 pins use their actual domains, including unwound physical pins conservatively assigned by row.
for pp,pb in zip(parts['T1']['pads'],pads('T1',best['T1'])):
 for r,bb in allpads:
  if r=='T1'or((pp['pin']in('6','7','8','9','10'))==(r in secondary)):continue
  dx=max(0,pb[0]-bb[2],bb[0]-pb[2]);dy=max(0,pb[1]-bb[3],bb[1]-pb[3]);dist=math.hypot(dx,dy)
  if dist<miniso[0]:miniso=(dist,['T1.'+pp['pin'],r])
edge=min((R-max(math.hypot(x,y)for x in(b[0],b[2])for y in(b[1],b[3])),r)for r,b in allpads)
report['actual_saved_pad_bbox_checks']={'min_projected_PS_bbox_distance_mm':miniso[0],'PS_pair':miniso[1],'working_reserve_mm':8,'working_reserve_pass':miniso[0]>=8,'min_copper_bbox_edge_distance_mm':edge[0],'edge_ref':edge[1],'edge_working_allowance_mm':.5,'edge_working_allowance_pass':edge[0]>=.5,'scope':'Projected2D metal only, including both faces. Not winding/core/joint/3D creepage/clearance or normative check.'}
report['fixed_anchor_limitations']=['R1 rectangular courtyard overruns study circle; actual body/pad octagon proposal requires native library review.','C1 native courtyard is rectangular and overruns circle. An UNAPPLIEDD11 circularcourt proposal would fit at hypot(19,4)+5.5=24.9165mm; actual body/lands/source tolerance still need library review.','T1 finished30x30x18 allocation not verified; C4 opposite-face tolerance and heat coupling not qualified.','Unverified physical heights, formed leads, joint projections and functional loops prevent stage approval.']
(D/'packing-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k]for k in('placed_count','total_count','missing_refs')}))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="740" viewBox="0 0 1200 740"><rect width="1200" height="740" fill="#0b1422"/><g fill="#e9eff8" font-family="Arial"><text x="40" y="45" font-size="28">Velluneo · fit study Ø51 mm</text><text x="40" y="75" font-size="16">Lamp target Ø60 × 120 mm · analytical candidate; no tracks or qualified insulation</text>']
for side,cx in [('F',315),('B',885)]:
 cy=380;s=9
 svg.append(f'<text x="{cx-70}" y="120" font-size="22">Side {side}</text><circle cx="{cx}" cy="{cy}" r="{R*s}" fill="#16352f" stroke="#72c4a3" stroke-width="2"/>')
 for r,c in best.items():
  if c[3]!=side:continue
  b=box(r,c);color='#c0a2ed'if r in secondary else'#e3b461'
  if r=='T1':b=[-15,-18,15,12]
  svg.append(f'<rect x="{cx+b[0]*s}" y="{cy+b[1]*s}" width="{(b[2]-b[0])*s}" height="{(b[3]-b[1])*s}" fill="{color}" fill-opacity=".25" stroke="{color}"/><text x="{cx+c[0]*s}" y="{cy+c[1]*s+4}" font-size="12" text-anchor="middle">{r}</text>')
 for r,c in best.items():
  for p,bb in zip(parts[r]['pads'],pads(r,c)):
   if c[3]!=side and not p['tht']:continue
   x=(bb[0]+bb[2])/2;y=(bb[1]+bb[3])/2
   svg.append(f'<rect x="{cx+bb[0]*s}" y="{cy+bb[1]*s}" width="{(bb[2]-bb[0])*s}" height="{(bb[3]-bb[1])*s}" fill="#f0d178"/>')
 svg.append(f'<text x="{cx-230}" y="650" font-size="16">Purple: secondary · gold: primary</text>')
svg.append(f'<text x="40" y="705" font-size="18">Assigned {len(best)}/31; unassigned: {", ".join(report["missing_refs"]) or "—"}. Diagnostic only; not a finished PCB.</text></g></svg>')
(D/'packing-diagnostic.svg').write_text(''.join(svg),encoding='utf-8')

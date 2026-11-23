from pathlib import Path
import json,math,collections
import pcbnew as k
ROOT=Path.cwd();H=ROOT/'work/sc09-order-audit/fabrication';O=ROOT/'outputs/SC09_weryfikacja_i_kompendium/fabrication-candidate';b=k.LoadBoard(str(H/'native-copy/SC09_compact.kicad_pcb'));mm=k.ToMM;data=json.loads((H/'parsed-gerbers.json').read_text());report=json.loads((H/'gerber-drill-audit.json').read_text())
def pseg(p,a,z):
 dx,dy=z[0]-a[0],z[1]-a[1];t=((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)if dx*dx+dy*dy else 0;t=max(0,min(1,t));return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def segdist(a,z,p,q):return min(pseg(a,p,q),pseg(z,p,q),pseg(p,a,z),pseg(q,a,z))
maskweb=[]
for ext in ['gts','gbs']:
 polys=[o['points']for o in data[ext]['operations']if o['kind']=='region'];bb=[(min(x for x,y in r),min(y for x,y in r),max(x for x,y in r),max(y for x,y in r))for r in polys];best=1e9;pair=None
 for i,a in enumerate(polys):
  for j in range(i):
   r=bb[i];s=bb[j];dx=max(0,r[0]-s[2],s[0]-r[2]);dy=max(0,r[1]-s[3],s[1]-r[3])
   if math.hypot(dx,dy)>=best:continue
   p=polys[j];gap=min(segdist(a1,a2,p1,p2)for a1,a2 in zip(a,a[1:]+a[:1])for p1,p2 in zip(p,p[1:]+p[:1]))
   if gap<best:best=gap;pair=[i,j]
 maskweb.append({'layer':ext,'minimum_web_between_distinct_openings_mm':round(best,6),'region_pair':pair,'green1oz_required_mm':.1,'pass':best>=.1})
widths={ext:sorted(set(round(o['aperture']['args'][0],6)for o in data[ext]['operations']if o['kind']=='line'))for ext in ['gto','gbo']}
texts=[{'owner':'board','text':t.GetText(),'layer':b.GetLayerName(t.GetLayer()),'height_mm':mm(t.GetTextHeight()),'stroke_mm':mm(t.GetTextThickness())}for t in b.GetDrawings()if isinstance(t,k.PCB_TEXT)and t.GetLayer()in [k.F_SilkS,k.B_SilkS]]
for f in b.GetFootprints():
 for t in [f.Reference(),f.Value()]:
  if t.IsVisible()and t.GetLayer()in [k.F_SilkS,k.B_SilkS]:texts.append({'owner':f.GetReference(),'text':t.GetText(),'layer':b.GetLayerName(t.GetLayer()),'height_mm':mm(t.GetTextHeight()),'stroke_mm':mm(t.GetTextThickness())})
report['soldermask_web_geometric_check']=maskweb;report['silkscreen_plotted_line_widths_mm']=widths;report['visible_native_silkscreen_text_inventory']=texts;report['silkscreen_text_height_pass']=all(t['height_mm']>=1 for t in texts);report['silkscreen_line_width_pass']=all(w>=.15 for ws in widths.values()for w in ws);report['mask_silk_visual_review']={'reviewer':'/root/sb01_fabrication_audit actualGerber-renderinspection','images':['Gerber_mask_silk_front.png','Gerber_mask_silk_back.png'],'result':'No missinglegend,unexpectedoverlayorpadobstructionseen. Backimageis topcoordinateview soletteringismirroredbydesign; doNOTmanuallymirrorproductionfiles.','limitation':'CustomliteralGerberrenderer supports allparsedprimitives; previewnotmanufacturercamacceptance.'};report['manufacturing_geometry_pass']=report['manufacturing_geometry_pass']and all(x['pass']for x in maskweb)and report['silkscreen_text_height_pass']and report['silkscreen_line_width_pass']
for p in [H/'gerber-drill-audit.json',O/'gerber-drill-audit.json']:p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k]for k in ['soldermask_web_geometric_check','silkscreen_plotted_line_widths_mm','visible_native_silkscreen_text_inventory','manufacturing_geometry_pass']},indent=2))


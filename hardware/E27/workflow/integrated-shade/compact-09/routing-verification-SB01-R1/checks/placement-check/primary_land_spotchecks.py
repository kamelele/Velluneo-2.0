from pathlib import Path
import json,math,hashlib
import pcbnew as k
H=Path(__file__).resolve().parent;src=H.parent/'baseline/SC09_compact.kicad_pcb';b=k.LoadBoard(str(src));f={x.GetReference():x for x in b.GetFootprints()};rows=[]
def check(ref,size,pairs,basis):
 p={x.GetNumber():x for x in f[ref].Pads()};bad=[]
 for n,x in p.items():
  a=sorted([k.ToMM(x.GetSize().x),k.ToMM(x.GetSize().y)])
  if any(abs(u-v)>.000002 for u,v in zip(a,sorted(size))):bad.append({'pin':n,'size':a})
 for n,z,expected in pairs:
  a,c=p[n].GetPosition(),p[z].GetPosition();dist=math.hypot(k.ToMM(a.x-c.x),k.ToMM(a.y-c.y))
  if abs(dist-expected)>.000002:bad.append({'pins':[n,z],'actual':dist,'expected':expected})
 rows.append({'ref':ref,'basis':basis,'passed':not bad,'findings':bad})
check('BR1',[1,2.15],[('1','3',2.5),('1','2',5.35)],'Diodes DS39045 Rev3-2 p4: MBS C2.50/X1.00/Y2.15/Y1outer7.50; rowspacing7.50-2.15=5.35, independently visually read primary.')
check('D1',[2.5,1.7],[('1','2',4)],'Diodes DS16008 Rev11-2 p4 US1A-US1M SMA: pads2.5x1.7, pitch4.0, gap1.5, independently visually read primary.')
check('U1',[1.45,.6],[('1','2',1.27),('1','8',5.45),('4','5',5.45)],'PI LYTSwitch1 RevB July2016 p11 D08A solder references:1.45x.60, pitch1.27, oppositecentres5.45, independently visually read primary.')
check('T1',[5.4,2.9],[('1','2',9.9)],'Wuerth7687709152 primaryp1 landdrawing:5.4x2.9, outer12.8, pitch12.8-2.9=9.9; windingbody12.0+/-0.5square/H10.5max.')
primary=['work/compact09/capture-active/MB10S.pdf','work/compact09/capture-active/US1J.pdf','work/compact09/rdr-research/lytswitch-1_family_datasheet.pdf','work/sc09-simple/t1/7687709152-mfr-mirror.pdf']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r={'actor':'/root/sb01_refine_placement_check','board_sha256':sha(src),'scope':'Literal primary land spotchecks and pin-contact dimensions for four high-energy/compact packages; not fullassemblyqualification ornormativeinsulation approval.','primary_inputs':{p:sha(p)for p in primary},'checks':rows,'passed':all(x['passed']for x in rows)};(H/'primary-land-spotchecks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'checks':len(rows)}))

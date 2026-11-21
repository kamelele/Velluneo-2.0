from pathlib import Path
import subprocess,json,hashlib,sys,shutil
W=Path(__file__).parent;sys.path[:0]=[str(W/'python-libs'),str(W/'cam-libs')]
from PIL import Image,ImageDraw,ImageFont
R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'visualisation-18';S=P/'catalogue-pcb-16';B=D/'scene/Velluneo_C16_VISUAL_ONLY.kicad_pcb';K=W/'kicad-10.0.6/bin/kicad-cli.exe';rows=[]
for side,rot in [('top','325,0,30'),('bottom','325,0,30')]:
 out=D/f'Velluneo_C16_{side}_4K.png';cmd=[str(K),'pcb','render','--width','4096','--height','3072','--side',side,'--rotate',rot,'--perspective','--zoom','.60','--background','opaque','--quality','high','--floor','--light-top','.8','--light-bottom','.7','--light-side','.6','--light-camera','.45','--output',str(out),str(B)]
 r=subprocess.run(cmd,capture_output=True,timeout=240);(D/f'{side}-render.log').write_bytes(r.stdout+b'\n'+r.stderr);assert r.returncode==0,(side,r.stderr)
 im=Image.open(out);assert im.width>=4000 and im.height>=3000
 rows.append(dict(side=side,path=out.name,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),dimensions=list(im.size),command=cmd));print(side,'4K done',flush=True)
# Two native renders on one presentation sheet; no pixel content is synthesized.
im=Image.new('RGB',(3840,1700),'#101820');dr=ImageDraw.Draw(im);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',55);normal=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',32)
dr.text((70,40),'VELLUNEO  |  ZASILACZ 45 × 60 mm',font=bold,fill='white')
for x,side,label in [(50,'top','GÓRA — elementy'),(1940,'bottom','SPÓD — elementy')]:
 dr.text((x+25,140),label,font=normal,fill='#dce8ec');pic=Image.open(D/f'Velluneo_C16_{side}_4K.png').convert('RGB');pic.thumbnail((1840,1380),Image.Resampling.LANCZOS);im.paste(pic,(x,205))
dr.text((75,1605),'Aktualny projekt C16 / pakiet C17 • modele obudów poglądowe • bez przewodów',font=normal,fill='#c7d4dc');im.save(D/'Velluneo_C16_3D_both_sides.png')
for a,b in [('C16_both_faces.png','Velluneo_C16_outer_connections.png'),('C16_inner_layers.png','Velluneo_C16_inner_connections.png')]:shutil.copyfile(S/'preview'/a,D/b)
(D/'render-provenance.json').write_text(json.dumps(dict(renderer='KiCad10.0.6 native highquality raytracing with floor/shadows',source_board_sha256=hashlib.sha256((S/'design/Velluneo_driver.kicad_pcb').read_bytes()).hexdigest(),renders=rows,composite='Two native rendered images resized together; annotation only, no generative image content',connections='Exact current C16 saved-copper diagrams, not simulated currentflow. F.Cu/In1/In2 topview; B.Cu mirrored for physicalunderside and explicitly labeled.',limits='Appearance models not exact supplier STEP. No harness/assembly fit/electricalqualification or manufacturingchange implied.'),indent=2)+'\n')
(D/'README.md').write_text('''# VIS18 - current C16 3D and copper views

Current45x60mm four-layer C16 PCB, matching C17manufacturing data. Native KiCad10.0.6
4064x3056 highquality raytraced (requested4096x3072; native renderer crop) top/bottom views and a combined presentation image.
All31 electronicpositions have appearance models; J1/J2wirepadpairs have no invented
harness. Two copper diagrams show allfourlayers; bottom is physically mirrored.
Componentreference labels on copper diagrams are explanatory overlays, not native silk.

Production CAD/manufacturing exports are unchanged. geometry-and-models.json binds
the exact source hash and proves33positions/80pads/333copperobjects unchanged using
native comparisons. Only model references/visibility and presentation plot selections
change in scene/Velluneo_C16_VISUAL_ONLY.kicad_pcb. Do not use it for manufacture.

The eight generic KiCadpackage models are retained from exact upstream tree
b8b3cfdfad88ba66f21002b3de51dc6f7d55ba5a with original headers and LICENSE.md
(CC-BY-SA4.0 plus upstream electronic-design exception). Other bodies are original
parametric appearance models. MYRRA74032 uses its current26.5x22.5x26.5mm reserved
envelope/ninepins; Q1uses its straightlead29.7mm height reservation and3mm shoulder
standoff. T1/Q1details, mountinghole, fuse/cap bodies are representative, not approved
supplierSTEP geometry or measuredfit. No artificial part marking or product photograph.

AllC16/C17physical/process/insulation/thermal/fault/firstfit/humanreleaseholds remain.
Rendering does not qualify assembly or operation. No suppliercontact/upload/order,
payment or poweredtest. This presentation task advances no engineering approval stage.
''',encoding='utf-8')
(D/'task-contract.md').write_text('''# VIS18 presentation-only task

Owner asks for a nice3Drender and boardconnections. BaseGit cafb6ec53fd55275bfe92ef97a77166a58a93ed3.
Root is solewriter of visualisation-18 and workflowindexentry. ExactC16 productionCAD
andC17manufacturingdata are read-only. Reuse verified nativegeometry and source-bound
appearanceassets; no circuit/rules/library/placement/routing/process acceptance changes.
Acceptance: bothfaces4Krenders visibly include actualcomponentbodies; all31electronics
represented; actual33position/80pad/333copperposes unchanged; sourcehash bound; current
fourlayerconnectionpreviews included and mirroredbottomlabeled; models/provenance/
license/caveats provided. Fourread-only roles check frozenpresentationpacket. GitHub
publication remains authorized by owner's standinginstruction. No supplier/order/testing.
''',encoding='utf-8')
for n in ['build_visual18.py','render_visual18.py']:shutil.copyfile(W/n,D/n)
print('Presentation and four-layer connection views saved')


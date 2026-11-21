from pathlib import Path
import subprocess,shutil,json
from PIL import Image,ImageDraw
from pypdf import PdfReader
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/supplier-review-13';Q=D/'.work/pdf-qa';Q.mkdir(parents=True,exist_ok=True);pdf=D/'drawings/Velluneo_RFQ13_Dimensioned_Review.pdf';exe=shutil.which('pdftoppm');assert exe
r=subprocess.run([exe,'-r','110','-png',str(pdf),str(Q/'page')],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120);assert r.returncode==0,r.stderr
doc=PdfReader(pdf);assert len(doc.pages)==7
for page in doc.pages:
 text=page.extract_text();assert 'VELLUNEO' in text and len(text)>300
 assert '\ufffd'not in text
sheet=Image.new('RGB',(1500,2250),'#e5ebef');draw=ImageDraw.Draw(sheet)
for i,path in enumerate(sorted(Q.glob('page-*.png'))):
 im=Image.open(path).convert('RGB');im.thumbnail((720,515));x=20+(i%2)*750;y=25+(i//2)*560;sheet.paste(im,(x,y));draw.text((x,y+520),'Page '+str(i+1),fill='black')
sheet.save(Q/'contact-sheet.png');shutil.copyfile(Q/'page-1.png',D/'drawings/board-interfaces-preview.png');shutil.copyfile(Q/'page-1.png',W.parent/'outputs/Velluneo_RFQ13_interfaces.png')
(D/'checks/pdf-qa.json').write_text(json.dumps(dict(pages=7,poppler_exit_code=0,text_checks=True,rendered_pages=7,visual_inspection_pending=True),indent=2)+'\n');print('Sevenpages rendered withPoppler;contactsheet ready.')

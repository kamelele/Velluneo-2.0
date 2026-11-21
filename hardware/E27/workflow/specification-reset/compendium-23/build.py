"""Build the offline current E22 compendium; PyMuPDF/Pillow and KiCad10.0.6."""
from pathlib import Path
import os,json,hashlib,shutil,subprocess,zipfile,csv
from html.parser import HTMLParser
import fitz
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent;P=D.parent;E=P/'efficiency-22';C=D/'content';C.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();binding={};commands=[]
def copy(src,dst):
 b=(P/src).read_bytes();f=C/dst;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);binding[dst]={'source':src,'sha256':sha(b)}
def tree(src,dst):
 for f in sorted((P/src).rglob('*')):
  rel=f.relative_to(P/src)
  if f.is_file()and not any(x in rel.parts for x in ['.work','__pycache__','content']):copy((Path(src)/rel).as_posix(),(Path(dst)/rel).as_posix())
def text(n,s):
 f=C/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s,encoding='utf-8',newline='\n')
def native(args):
 cmd=[os.environ['KICAD_CLI'],*args];r=subprocess.run(cmd,capture_output=True,timeout=90);commands.append({'command':cmd,'exit_code':r.returncode});assert r.returncode==0,r.stderr
for side in ['top','bottom']:copy(f'efficiency-22/visual/Velluneo_E22_{side}_4K.png',f'01_Rendery/E22_{side}_4K.png')
tree('efficiency-22/visual/scene','01_Rendery/Podglad_3D_KiCad')
canvas=Image.new('RGB',(3840,1700),'#101820');dr=ImageDraw.Draw(canvas);bf=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',55);nf=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',32)
dr.text((70,40),'VELLUNEO E22 | ZASILACZ 45 × 60 mm',font=bf,fill='white')
for x,side,label in [(50,'top','GÓRA'),(1940,'bottom','SPÓD — nowa dioda SMB')]:
 dr.text((x+25,140),label,font=nf,fill='#dce8ec');im=Image.open(C/f'01_Rendery/E22_{side}_4K.png').convert('RGB');im.thumbnail((1840,1380),Image.Resampling.LANCZOS);canvas.paste(im,(x,205))
dr.text((75,1605),'Rewizja E22 • modele obudów poglądowe • stan projektu przed pomiarami',font=nf,fill='#c7d4dc');canvas.save(C/'01_Rendery/E22_obie_strony.png')
board=E/'design/Velluneo_driver.kicad_pcb';(C/'02_Warstwy').mkdir(exist_ok=True)
for name,layer,mirror in [('01_F_Cu_gora','F.Cu',False),('02_In1_Cu','In1.Cu',False),('03_In2_Cu','In2.Cu',False),('04_B_Cu_spod','B.Cu',True)]:
 f=C/'02_Warstwy'/f'{name}.svg';native(['pcb','export','svg','--layers',layer+',Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet',*(['--mirror']if mirror else[]),'--output',str(f),str(board)])
 doc=fitz.open(f);page=doc[0];page.get_pixmap(matrix=fitz.Matrix(1800/page.rect.width,1800/page.rect.width),alpha=False).save(f.with_suffix('.png'))
text('02_Warstwy/ORIENTACJA.txt','F.Cu/In1.Cu/In2.Cu: od góry. B.Cu: lustrzany widok od fizycznego spodu. Każdy SVG/PNG pokazuje miedź jednej warstwy i obrys. Aktualna E22; 333 obiekty ścieżek/przelotek pozostają bez zmiany geometrii; zmieniono pola D3/R13 i przesunięto D3 o0.3mm.\n')
copy('efficiency-22/Velluneo_E22_schematic.pdf','03_Schemat_BOM/Schemat_E22.pdf');copy('efficiency-22/manufacturing/Velluneo_E22_assembly_layers.pdf','03_Schemat_BOM/Warstwy_montazowe_E22.pdf')
tree('efficiency-22/manufacturing/assembly','03_Schemat_BOM/assembly');copy('efficiency-22/selected-bom.json','03_Schemat_BOM/Podzespoly_E22.json')
for sub in ['power','startup','diode']:tree('efficiency-22/'+sub,'04_Obliczenia/efficiency-22/'+sub)
tree('power-thermal-20','04_Obliczenia/power-thermal-20')
for n in ['native-curve-data.json','results.json','README.md','sources.json']:copy('led-compatibility-19/'+n,'04_Obliczenia/led-compatibility-19/'+n)
for n in ['calculations.json','README.md','bring-up-and-assembly.md']:copy('catalogue-pcb-16/'+n,'04_Obliczenia/catalogue-pcb-16/'+n)
source=E/'manufacturing/Velluneo_E22_KiCad_Source.zip'
with zipfile.ZipFile(source)as z:
 for n in z.namelist():
  rel=Path(n);assert not rel.is_absolute()and'..'not in rel.parts
  f=C/'05_KiCad'/rel;f.parent.mkdir(parents=True,exist_ok=True);b=z.read(n);f.write_bytes(b);binding['05_KiCad/'+rel.as_posix()]={'source_archive':'efficiency-22/manufacturing/Velluneo_E22_KiCad_Source.zip','member':n,'sha256':sha(b)}
tree('efficiency-22/manufacturing','06_Dane_E22')
for n in ['README.md','native-eco.json','part-changes.json','toolkit-doctor.json','ownership.md','open-conditions.json']:copy('efficiency-22/'+n,'07_Status_E22/'+n)
tree('efficiency-22/checks','07_Status_E22/checks')
copy('catalogue-pcb-16/open-engineering-holds.json','07_Status_E22/Historyczne_holds_C16_nadal_otwarte.json');copy('manufacturing-c17/finding-ledger.json','07_Status_E22/Warunki_procesu_C17_nadal_otwarte.json');copy('requirements-and-plan.md','07_Status_E22/Wymagania_zrodlowe.md')
for n in ['MYRRA74032.pdf','MYRRA74032-PCN.pdf']:copy('manufacturing-c17/support/'+n,'08_Transformator/'+n)
r=json.loads((E/'power/comparison.json').read_text());a=r['old_nominal'];b=r['new_nominal'];temps=json.loads((E/'power/results.json').read_text());t=next(q for q in temps['thermal_scenarios']if q['scenario']=='target_path'and q['ambient_C']==40 and q['electrical_case']=='central')
text('00_START_TUTAJ.txt','''VELLUNEO — AKTUALNE KOMPENDIUM E22 | 21.11.2026
Rozpakuj cały ZIP i otwórz 00_KOMPENDIUM.html.
ProjektKiCad:05_KiCad/design/Velluneo_driver.kicad_pro (KiCad10.0.6).

Ta rewizja zastępuje C16/C17 dla zmienionych części i footprintów.
D3=STPS2200U/SMB;R16/R17=422k;R13=TNPW84.5k0.1%25ppm.
Nie mieszaj nowegoPCB z poprzednimBOM/CPL/Gerberami C17.
01rendery /02czterywarstwy /03schemat-BOM /04obliczenia /05KiCad /
06aktualne daneE22 /07status i kontrole /08transformator.

Nominalne obliczenia:8.54W z sieci,6.54WLED,2.00W ciepła,76.6% sprawności.
Zysk względemC16 około0.41punktu procentowego, nie kilka procent.
Przy dużym upływie gorącej diody wybrane przypadki mogą być gorsze.
To prototyp do porównania laboratoryjnego, nie potwierdzenie poprawy we wszystkich warunkach.
Brak pomiarów/kwalifikacji chłodzenia, izolacji, usterek i zgody produkcyjnej.
Pełne raporty zawierają założenia oraz otwarte kwestie. Stany magazynowe są datowane, nierezerwowane.
''')
doc='''<!doctype html><html lang="pl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Velluneo E22 — kompendium</title><style>body{font:17px/1.6 system-ui;background:#eef2f5;color:#172732;margin:0}main{max-width:1120px;margin:auto;padding:36px}h1{font-size:42px;line-height:1.15}h2{margin-top:48px}a{color:#126974}img{max-width:100%;height:auto;border-radius:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}.card,section{background:white;padding:22px;border-radius:12px}.card strong{display:block;font-size:24px}.note{background:#fff1d6;border-left:5px solid #c58520;padding:20px}small{color:#526675}code{overflow-wrap:anywhere}</style><main><small>VELLUNEO · REWIZJA E22 · 21 LISTOPADA 2026</small><h1>Kompendium zasilacza</h1><p>Aktualny projekt po zmianie diody i rezystorów. ProstokątnePCB45×60mm,4warstwy,1.6mm;33pozycje. Wejście230Vac50Hz, normalnie207–253Vac. Pierwszy wkład:7szeregowo CreeH40/4000K. Normalna alokacja wyjścia19–22V/około319mAłącznie.</p><p class="note"><b>Status:</b> E22jest kandydatem do porównania laboratoryjnego. Nie wykonano pomiarów ani kwalifikacji rozruchu, usterek, izolacji i chłodzenia. Nowa dioda nie ma potwierdzonego zysku w każdych warunkach. Nie używaj poprzednich Gerberów/BOM/CPL C17 do wykonania tej rewizji.</p><div class="grid">'''
for title,value in [('Pobór — obliczenie',f"{b['input_W']:.2f} W"),('Moc LED',f"{b['LED_power_W']:.2f} W"),('Straty zasilacza',f"{b['driver_heat_W']:.2f} W"),('Sprawność do LED',f"{100*b['efficiency_to_LEDs']:.2f}%")]:doc+=f'<div class="card">{title}<strong>{value}</strong></div>'
doc+='''</div><h2>Co zmieniono</h2><ul><li>D3: STTH2R02A/SMA → <b>STPS2200U/SMB</b>, nadal200V/2A/175°C; niższe straty w przyjętym modelu, większy upływ na gorąco i pojemność wymagają sprawdzenia.</li><li>R16/R17:402k → <b>422k</b>, zachowana rodzina500V/1W.</li><li>R13:80.6k → <b>84.5k,0.1%,25ppm/K</b>; ciaśniejsza tolerancja poprawia granice rozruchu.</li><li>R1, rezystory rozładowania kondensatora głównego i wyjścia, pomiar prądu, zabezpieczenia oraz progi sterownika pozostają bez zmian. Większe polaD3/R13; D3przesunięta0.3mm. Geometria333ścieżek/przelotek zachowana.</li></ul><p>Nowe części mają zewnętrzne trasy zakupuMOQ1. DostępnośćJLCPCBA/montaż nie są potwierdzone; zrzuty dostępności nie są rezerwacją.</p><h2>Najnowsze rendery obu stron</h2><a href="01_Rendery/E22_obie_strony.png"><img src="01_Rendery/E22_obie_strony.png" alt="E22 obie strony"></a><p><a href="01_Rendery/E22_top_4K.png">Góra4K</a> · <a href="01_Rendery/E22_bottom_4K.png">Spód4K</a>. Modele obudów są poglądowe, nie zatwierdzonymi modelami producentów. Nowa dioda ma modelSMB.</p><h2>Każda warstwa osobno</h2><p>F.Cu/In1/In2 od góry; B.Cu odbite lustrzanie, od fizycznego spodu. SVG pozwala powiększać bez utraty jakości.</p><div class="grid">'''
for name,label in [('01_F_Cu_gora','F.Cu — góra'),('02_In1_Cu','In1.Cu'),('03_In2_Cu','In2.Cu'),('04_B_Cu_spod','B.Cu — spód lustrzany')]:doc+=f'<section><h3>{label}</h3><a href="02_Warstwy/{name}.png"><img src="02_Warstwy/{name}.png" alt="{label}"></a><p><a href="02_Warstwy/{name}.svg">SVG</a></p></section>'
doc+='''</div><h2>Moc, sprawność i temperatury</h2><img src="04_Obliczenia/efficiency-22/power/E22_power_overview.png" alt="Aktualne obliczeniaE22"><p>Przy tych samych założeniach centralnych:8.586→8.538W poboru;2.046→1.999W ciepła;76.17→76.58% sprawności. Zysk około0.41punktu procentowego. Model odtwarza poprzedni wynikC16.97porównanych przypadków obejmuje też pogorszenie: w skrajnym scenariuszu upływu diody przyrost ciepła do34mW. Obwód tłumiący i transformator nadal mają założony, a nie zmierzony podział strat.</p><p>Przy40°C otoczenia i <b>założonym</b> chłodzeniu3K/W z wnętrza do otoczenia,8K/W z płytki do wnętrza, bez dogrzewania od LED: dioda około66°C, tranzystor68°C, kondensator wejściowy72°C. W bardziej stratnym scenariuszu C1nadal może osiągać około99°C, powyżej roboczego celu85°C. Rzeczywiste opory cieplne i temperatury wewnętrzne nie są ustalone. Powietrze przyMYRRA musi być≤50°C; ta zmiana nie rozwiązuje chłodzenia.</p><p>Rozruch:64narożnikiDC oraz72przypadki ładowania z sieci na projekt przechodzą sprawdzenie przed włączeniem sterownika. NajdłuższeDCładowanie23V:.251660→.247664s; minimalny zapas prądu9.528→11.754µA. Nominalny przykład jest wolniejszy:.19388→.20746s, nadal poniżej celu1s. To nie jest pełna symulacja sterownika ani pomiar osiągnięcia90%światła. Ponowienia po usterce pozostają do sprawdzenia.</p><ul><li><a href="04_Obliczenia/efficiency-22/power/README.md">Pełne porównanie sprawności i temperatur</a> · <a href="04_Obliczenia/efficiency-22/power/comparison.json">97porównanych przypadków</a></li><li><a href="04_Obliczenia/efficiency-22/startup/README.md">Rozruch i rezystory</a> · <a href="04_Obliczenia/efficiency-22/diode/README.md">Dobór diody i ryzyka</a></li><li><a href="04_Obliczenia/power-thermal-20/README.md">Historyczny POWER20 — baza porównania</a></li></ul><p class="note"><b>Otwarty zapas zasilania sterownika:</b> przy19V wyjścia idealny wynik9,556V nie uwzględnia spadku naR10, uzwojeniu ani tętnień. Pozostaje tylko106mV do celu9,45V. RzeczywistegoVDD i braku pogorszenia przejęcia zasilania nie potwierdzono. <a href="07_Status_E22/open-conditions.json">Warunki kwalifikacjiE22</a>.</p><h2>Schemat, projekt i dane wykonawcze</h2><ul><li><a href="03_Schemat_BOM/Schemat_E22.pdf">Aktualny schematPDF</a> · <a href="03_Schemat_BOM/Warstwy_montazowe_E22.pdf">Aktualne warstwy montażowePDF</a></li><li><a href="03_Schemat_BOM/assembly/BOM_33_FULL.csv">BOM33pozycji</a> · <a href="03_Schemat_BOM/Podzespoly_E22.json">Dokładne części i trasy zakupu</a></li><li><code>05_KiCad/design/Velluneo_driver.kicad_pro</code> — otwórz cały katalog wKiCad10.0.6,z bibliotekami.</li><li><a href="06_Dane_E22/Velluneo_E22_Gerber_DFM.zip">Nowe GerberyE22</a> · <a href="06_Dane_E22/README.md">Warunki wykonania i montażu</a>. Zatwierdzenie procesu i produkcji pozostaje osobnym krokiem.</li><li><a href="07_Status_E22/README.md">StatusE22, kryteria i plan pomiarów</a> · <a href="07_Status_E22/Historyczne_holds_C16_nadal_otwarte.json">Zachowane otwarte kwestie</a></li><li><a href="08_Transformator/MYRRA74032.pdf">MYRRA74032</a> · <a href="08_Transformator/MYRRA74032-PCN.pdf">Aktualizacja gabarytu</a></li></ul><p><small>Źródłowa baza63c7a3f, kandydatE22. Integralność:MANIFEST_SHA256.json; pochodzenie:SOURCE_BINDING.json. Dokumentacja i obliczenia nie są pomiarami ani zatwierdzeniem bezpieczeństwa.</small></p></main></html>'''
text('00_KOMPENDIUM.html',doc)
text('SOURCE_BINDING.json',json.dumps({'base_commit':'63c7a3fed59d7807bd1b71cf9058175b04a22f4b','candidate':'E22','source_board_sha256':sha(board.read_bytes()),'copies':binding,'native_layer_exports':commands},indent=2,ensure_ascii=False)+'\n')
manifest={f.relative_to(C).as_posix():sha(f.read_bytes())for f in sorted(C.rglob('*'))if f.is_file()and f.name!='MANIFEST_SHA256.json'}
text('MANIFEST_SHA256.json',json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):self.refs.extend(v for k,v in attrs if k in ['href','src']and not v.startswith(('#','http')))
h=Links();h.feed(doc);assert all((C/n).is_file()for n in h.refs)
archive=D/'Velluneo_Kompendium_Zasilacza_E22.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for f in sorted(C.rglob('*')):
  if f.is_file():
   inf=zipfile.ZipInfo('Velluneo_Kompendium_E22/'+f.relative_to(C).as_posix(),(2026,11,21,12,0,0));inf.compress_type=zipfile.ZIP_DEFLATED;inf.external_attr=0o644<<16;z.writestr(inf,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None;assert all(sha(z.read('Velluneo_Kompendium_E22/'+n))==v for n,v in manifest.items())
textobj={'archive':archive.name,'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,'members':len(manifest)+1,'local_HTML_references':len(h.refs),'broken_references':0,'source_board_sha256':sha(board.read_bytes()),'all_member_CRC_and_hashes_pass':True,'copies_bound':len(binding),'no_C17_Gerber_or_CPL_presented_as_current':True}
(D/'archive-check.json').write_text(json.dumps(textobj,indent=2)+'\n',encoding='utf-8');print(json.dumps(textobj,indent=2))

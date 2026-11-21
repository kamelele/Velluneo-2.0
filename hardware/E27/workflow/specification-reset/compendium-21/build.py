"""Build a source-bound offline compendium. Production files are read-only.
Run with Python containing PyMuPDF; set KICAD_CLI to pinned10.0.6 binary.
"""
from pathlib import Path
import hashlib,html,json,os,shutil,subprocess,zipfile

D=Path(__file__).resolve().parent;P=D.parent;R=P.parents[3]
C=D/'content';C.mkdir(exist_ok=True)
BASE='d89fdec0a59b99eebee64de0c1493af3eb8360b3'
sha=lambda b:hashlib.sha256(b).hexdigest()
records={};commands=[]

def write(n,s):
    f=C/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s,encoding='utf-8',newline='\n')

def copy(src,dst):
    b=(P/src).read_bytes();f=C/dst;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    records[dst]={'repository_source':'hardware/E27/workflow/specification-reset/'+src,'sha256':sha(b)}

def tree(src,dst):
    for f in sorted((P/src).rglob('*')):
        rel=f.relative_to(P/src)
        if f.is_file() and not any(x in rel.parts for x in ['.work','__pycache__','.git']):
            copy((Path(src)/rel).as_posix(),(Path(dst)/rel).as_posix())

def native(args):
    k=os.environ.get('KICAD_CLI');assert k
    cmd=[k,*args];r=subprocess.run(cmd,capture_output=True,timeout=90)
    commands.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout.decode('utf-8',errors='replace'),'stderr':r.stderr.decode('utf-8',errors='replace')})
    assert r.returncode==0,commands[-1]

board=P/'catalogue-pcb-16/design/Velluneo_driver.kicad_pcb'
assert sha(board.read_bytes())=='3c13b9d2048a6d6b1c830c75445d27412516f0c0fb03d6c5285b8c2f69067f78'
for n in ['Velluneo_C16_top_4K.png','Velluneo_C16_bottom_4K.png','Velluneo_C16_3D_both_sides.png','README.md','render-provenance.json']:
    copy('visualisation-18/'+n,'01_Rendery/'+n)
for n in ['Velluneo_C16_outer_connections.png','Velluneo_C16_inner_connections.png']:
    copy('visualisation-18/'+n,'02_Warstwy/'+n)

# New plots use the saved production board, no refill or source mutation.
import fitz
for name,layer,mirror in [('01_F_Cu_gora','F.Cu',False),('02_In1_Cu','In1.Cu',False),('03_In2_Cu','In2.Cu',False),('04_B_Cu_spod','B.Cu',True)]:
    out=C/'02_Warstwy'/f'{name}.svg';out.parent.mkdir(exist_ok=True)
    native(['pcb','export','svg','--layers',layer+',Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet',*(['--mirror']if mirror else[]),'--output',str(out),str(board)])
    doc=fitz.open(out);pg=doc[0];pix=pg.get_pixmap(matrix=fitz.Matrix(1800/pg.rect.width,1800/pg.rect.width),alpha=False)
    pix.save(C/'02_Warstwy'/f'{name}.png')
write('02_Warstwy/ORIENTACJA.txt','F.Cu, In1.Cu i In2.Cu: widok od góry. B.Cu: odbicie lustrzane, widok od fizycznego spodu.\nCztery pliki SVG/PNG pokazują miedź jednej warstwy i obrys; bez nadruku innych warstw.\nZbiorcze obrazy zewnętrznych/wewnętrznych warstw mają objaśniające oznaczenia elementów.\nTo rzeczywista geometria zapisanego PCB C16, nie symulacja przepływu prądu.\n')

copy('manufacturing-c17/drawings/Velluneo_C17_schematic.pdf','03_Schemat_BOM/Schemat_C16_C17.pdf')
copy('manufacturing-c17/drawings/Velluneo_C17_Fabrication_Assembly.pdf','03_Schemat_BOM/Rysunki_montazowe.pdf')
for n in ['BOM_33_FULL.csv','BOM_28_SMT.csv','CPL_28_SMT.csv','POSITIONS_33_REFERENCE.csv','operations.csv','READ_BEFORE_ASSEMBLY.txt']:
    copy('manufacturing-c17/assembly/'+n,'03_Schemat_BOM/'+n)
copy('catalogue-pcb-16/selected-bom.json','03_Schemat_BOM/Podzespoly_trasy_zakupu_C16.json')
tree('power-thermal-20','04_Obliczenia/power-thermal-20')
for n in ['README.md','results.json','native-curve-data.json','sources.json','measurement-plan.md']:
    copy('led-compatibility-19/'+n,'04_Obliczenia/led-compatibility-19/'+n)
for n in ['calculations.json','calculate.py','engineering-change.md','bring-up-and-assembly.md']:
    copy('catalogue-pcb-16/'+n,'04_Obliczenia/catalogue-pcb-16/'+n)

# Expand the already reviewed portable source archive, retaining every member byte.
src=P/'manufacturing-c17/Velluneo_C17_KiCad_Source.zip'
with zipfile.ZipFile(src)as z:
    for info in z.infolist():
        if info.is_dir():continue
        rel=Path(info.filename);assert not rel.is_absolute() and '..'not in rel.parts
        f=C/'05_KiCad'/rel;f.parent.mkdir(parents=True,exist_ok=True);b=z.read(info);f.write_bytes(b)
        records['05_KiCad/'+rel.as_posix()]={'repository_archive':'hardware/E27/workflow/specification-reset/manufacturing-c17/Velluneo_C17_KiCad_Source.zip','archive_member':info.filename,'sha256':sha(b)}
assert sha((C/'05_KiCad/design/Velluneo_driver.kicad_pcb').read_bytes())==sha(board.read_bytes())
for n in ['Velluneo_C17_Prototype_Manufacturing_Package.zip','Velluneo_C17_Gerber_Upload.zip','START_HERE_PL.txt','quote-settings.json','JLCPCB-ENQUIRY-UNSENT.txt','stage-packet.md']:
    copy('manufacturing-c17/'+n,'06_Dane_produkcyjne_C17/'+n)
write('06_Dane_produkcyjne_C17/STATUS.txt','Dane C17 odpowiadają obecnemu PCB C16, ale nie stanowią zatwierdzenia produkcji.\nPozostają otwarte wymagania fizyczne, izolacyjne, cieplne, usterkowe i procesu montażu.\nNie wysłano zapytania ani zamówienia. Dane katalogowe/stan części mają daty źródłowe; nie są rezerwacją magazynową.\n')
for n in ['open-engineering-holds.json','calculations.json','checks/erc.json','checks/drc.json','checks/intent-comparison.json','checks/C16-netlist.xml','stage-packet.md']:
    copy('catalogue-pcb-16/'+n,'07_Status_kontrole/C16/'+n)
copy('manufacturing-c17/finding-ledger.json','07_Status_kontrole/C17_finding-ledger.json')
copy('requirements-and-plan.md','07_Status_kontrole/Wymagania_zrodlowe.md')
for n in ['MYRRA74032.pdf','MYRRA74032-PCN.pdf']:
    copy('manufacturing-c17/support/'+n,'08_Transformator/'+n)

j=json.loads((P/'power-thermal-20/results.json').read_text(encoding='utf-8'));n=j['nominal']
write('00_START_TUTAJ.txt',f'''VELLUNEO — KOMPENDIUM ZASILACZA | 21.11.2026
Rozpakuj cały ZIP i otwórz 00_KOMPENDIUM.html w przeglądarce.

Aktualny projekt: C16, dane produkcyjne C17, rendery VIS18, LED19, analiza POWER20.
PCB prostokątne45×60mm,4warstwy,1.6mm;33pozycje,31elementów elektronicznych.
Zasilanie230Vac50Hz; założony normalny zakres207–253Vac.
Wyjście stałoprądowe319mA łącznie; LED nominalnie316.94mA po rezystorach wyjściowych.
Pierwszy wkład:7szeregowo Cree JB2835BWT-G-H40GA0000-N0000001,4000K.
Punkt obliczeniowy:20.64V;6.54W LED;8.59W z sieci;2.05W ciepła;76.2% sprawności do LED.
To warunkowe obliczenia, nie pomiary. Wybrane scenariusze:1.49–3.17W ciepła.
Powietrze przy transformatorze musi pozostać<=50C. Obudowa/chłodzenie niezweryfikowane.
Aktualna analiza wykazuje C1~99C w jednym z założonych wariantów; cel zapasu85C niespełniony.

01_Rendery — natywne rendery obu stron w4K; modele obudów części są poglądowe.
02_Warstwy — każda z4warstw osobno wPNG/SVG; spód lustrzany, opis orientacji.
03_Schemat_BOM — schematPDF, rysunki, BOM, montaż, źródłowe trasy zakupu.
04_Obliczenia — najnowszy POWER20, LED19 i bieżące obliczenia elektryczne C16.
05_KiCad/design/Velluneo_driver.kicad_pro — edytowalny projekt z bibliotekami.
06_Dane_produkcyjne_C17 — istniejące daneGerber/montaż do oceny wykonawcy; nie zgoda na produkcję.
07_Status_kontrole — zapisane ERC/DRC, lista otwartych kwestii i wymagania.
08_Transformator — aktualny rysunekMYRRA74032 iPCN.

Rendery/rysunki pochodzą z tej samej bieżącej geometrii. Brak nowych zmian PCB.
Nie wykonano pomiarów, testów bezpieczeństwa, badańEMC ani zamówienia.
Źródłowy commit:{BASE}
ManifestSHA256 opisuje zawartość; SOURCE_BINDING.json wskazuje pochodzenie kopii.
''')

cards=[('PCB','45 × 60 mm · 4 warstwy'),('Wejście','230 V AC · 50 Hz'),('LED / moc','7 szeregowo · 6,54 W'),('Pobór / sprawność','8,59 W · 76,2%'),('Ciepło zasilacza','2,05 W nominalnie'),('Zakres scenariuszy','1,49–3,17 W ciepła')]
def pic(path,alt):return f'<a href="{path}"><img src="{path}" alt="{html.escape(alt)}"></a>'
doc='''<!doctype html><html lang="pl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Velluneo — kompendium zasilacza</title><style>
body{font:17px/1.6 system-ui,sans-serif;background:#eef2f5;color:#172732;margin:0}main{max-width:1120px;margin:auto;padding:36px}h1{font-size:42px;line-height:1.15}h2{margin-top:50px}a{color:#126974}img{max-width:100%;height:auto;border-radius:12px;background:white}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.card,section{background:white;padding:22px;border-radius:12px}.card strong{display:block;font-size:23px}.note{background:#fff1d6;border-left:5px solid #c58520;padding:20px}small{color:#526675}.layers img{background:#fff;border:1px solid #ddd}nav a{margin-right:18px}li{margin-bottom:8px}code{overflow-wrap:anywhere}</style><main>
<small>VELLUNEO · ZASILACZ C16 / DANE C17 · 21 LISTOPADA 2026</small><h1>Kompendium zasilacza</h1><p>Aktualne rendery, połączenia czterech warstw, schemat, części, obliczenia oraz edytowalny projekt — w jednym pakiecie działającym offline.</p>
<nav><a href="#rendery">Rendery</a><a href="#warstwy">Warstwy</a><a href="#cieplo">Moc i ciepło</a><a href="#pliki">Projekt i dokumenty</a></nav><p class="note"><b>Status:</b> istnieje kompletne trasowanie i dane C17. Pozostają pomiary, weryfikacja chłodzenia, usterkowa, izolacyjna i montażowa. Ten pakiet nie oznacza zatwierdzenia produkcji. Temperatury poniżej są scenariuszami obliczeniowymi, nie pomiarami.</p><div class="grid">'''+''.join(f'<div class="card">{a}<strong>{b}</strong></div>'for a,b in cards)+'''</div><p><small>Podane moce dotyczą nominalnego scenariusza POWER20 przy230Vac.319mA to prąd całego wyjścia; po rezystorach wyjściowych do LED trafia około316,94mA. Przyjęty punkt napięcia LED wykorzystuje referencję85°C złącza; to nie przewidywana temperatura pracy.</small></p>
<h2 id="rendery">Aktualny wygląd — obie strony</h2>'''+pic('01_Rendery/Velluneo_C16_3D_both_sides.png','Rendery góry i spodu')+'''<p><a href="01_Rendery/Velluneo_C16_top_4K.png">Góra — pełny render4K</a> · <a href="01_Rendery/Velluneo_C16_bottom_4K.png">Spód — pełny render4K</a></p><p>Rendery natywnego KiCada; obudowy elementów są modelami poglądowymi. Brak przewodów w obrazie nie oznacza ich braku w gotowym montażu. Rezerwacja wysokości największego elementu około29,7mm nad PCB.</p>
<h2 id="warstwy">Połączenia na każdej warstwie</h2><p>F.Cu, In1.Cu i In2.Cu są pokazane od góry. B.Cu jest odbite lustrzanie, czyli pokazane od fizycznego spodu. SVG pozwala powiększać bez utraty jakości. Poniżej tylko miedź danej warstwy i obrys.</p><div class="grid layers">'''
for stem,label in [('01_F_Cu_gora','1 · F.Cu — góra'),('02_In1_Cu','2 · In1.Cu — wewnętrzna'),('03_In2_Cu','3 · In2.Cu — wewnętrzna'),('04_B_Cu_spod','4 · B.Cu — spód lustrzany')]:
    doc+=f'<section><h3>{label}</h3>'+pic('02_Warstwy/'+stem+'.png',label)+f'<p><a href="02_Warstwy/{stem}.svg">Otwórz SVG</a></p></section>'
doc+='''</div><p><a href="02_Warstwy/Velluneo_C16_outer_connections.png">Zewnętrzne warstwy z oznaczeniami</a> · <a href="02_Warstwy/Velluneo_C16_inner_connections.png">Wewnętrzne warstwy z oznaczeniami</a></p>
<h2 id="cieplo">Najnowsze obliczenia mocy i temperatur</h2>'''+pic('04_Obliczenia/power-thermal-20/POWER20_overview.png','Bilans mocy i wymagania chłodzenia')+'''<p>Nominalnie8,59W z sieci,6,54W dla LED i2,05W strat.97wybranych przypadków daje pobór7,83–9,92W i straty1,49–3,17W. To zakres założeń, nie gwarantowane granice.</p><p>Przy40°C otoczenia, założonej drodze cieplnej3K/W z wnętrza do otoczenia,8K/W z płytki do wnętrza i zerowym dogrzewaniu od LED: tranzystor około68°C, dioda70°C, kondensator wejściowy73°C w scenariuszu centralnym. W wybranym scenariuszu większych strat C1 osiąga około99°C, powyżej roboczego celu zapasu85°C. Opory cieplne obudowy i części nie zostały zmierzone; wewnętrzne temperatury transformatora i kondensatorów nie są ustalone.</p><p>MYRRA74032 ma limit50°C dla otaczającego powietrza. Przy40°C na zewnątrz i maksymalnych stratach wybranych scenariuszy efektywna droga z wnętrza do otoczenia musi wynosić najwyżej3,16K/W bez dogrzewania od LED albo2,00K/W przy25% sprzężenia ich mocy jako ciepła. Nie wybrano jeszcze konkretnego radiatora, wentylacji ani zweryfikowanej obudowy.</p><ul><li><a href="04_Obliczenia/power-thermal-20/README.md">Pełny raport i tabela temperatur</a></li><li><a href="04_Obliczenia/power-thermal-20/electrical-cases.csv">Wszystkie przypadki — CSV</a> · <a href="04_Obliczenia/power-thermal-20/results.json">wynikiJSON, w tym18scenariuszy cieplnych</a></li><li><a href="04_Obliczenia/power-thermal-20/method-and-assumptions.md">Metoda i założenia</a> · <a href="04_Obliczenia/power-thermal-20/measurement-plan.md">Plan pomiarów</a></li></ul>
<h2 id="pliki">Schemat, części i projekt</h2><ul>
<li><a href="03_Schemat_BOM/Schemat_C16_C17.pdf">Schemat PDF</a> · <a href="03_Schemat_BOM/Rysunki_montazowe.pdf">rysunki wykonawcze i montażowe</a></li>
<li><a href="03_Schemat_BOM/BOM_33_FULL.csv">Pełny BOM33pozycji</a> · <a href="03_Schemat_BOM/Podzespoly_trasy_zakupu_C16.json">dokładne części i trasy zakupu</a>. Dane dostępności zachowują daty źródłowe; nie są rezerwacją ani bieżącym sprawdzeniem magazynów.</li>
<li><code>05_KiCad/design/Velluneo_driver.kicad_pro</code> — otwórz wKiCad10.0.6. Zachowaj cały katalog z bibliotekami. Projekt produkcyjny nie zawiera poglądowych modeli wizualizacji VIS18.</li>
<li><a href="06_Dane_produkcyjne_C17/Velluneo_C17_Prototype_Manufacturing_Package.zip">Oryginalny pakiet danych C17</a> · <a href="06_Dane_produkcyjne_C17/Velluneo_C17_Gerber_Upload.zip">Gerbery</a>. Ocenę wykonawcy, montażu i zgody produkcyjnej należy traktować osobno.</li>
<li><a href="07_Status_kontrole/C16/open-engineering-holds.json">Otwarte kwestie C16</a> · <a href="07_Status_kontrole/C17_finding-ledger.json">status C17</a>. Zachowane kontroleERC/DRC dotyczą ich źródłowej rewizji; brak nowej zmianyCAD.</li>
<li><a href="08_Transformator/MYRRA74032.pdf">MYRRA74032 — dokumentacja</a> · <a href="08_Transformator/MYRRA74032-PCN.pdf">PCN — aktualizacja gabarytu</a>. Transformator fabrycznie nawinięty; aktualna rezerwacja korpusu26,5×22,5×26,5mm.</li></ul>
<p><small>Źródła: commit '''+BASE+''' · C16/C17/VIS18/LED19/POWER20. SOURCE_BINDING.json iMANIFEST_SHA256.json pozwalają sprawdzić pochodzenie oraz integralność plików. Brak nowej zmiany schematu, PCB, części lub zatwierdzeń.</small></p></main></html>'''
write('00_KOMPENDIUM.html',doc)
binding={'base_commit':BASE,'source_board_sha256':sha(board.read_bytes()),'copied_files':records,'new_layer_plot_commands':commands,'scope':'Packaging and presentation only; unchanged production design, models illustrative, no new release/physical approval'}
write('SOURCE_BINDING.json',json.dumps(binding,indent=2,ensure_ascii=False)+'\n')
manifest={f.relative_to(C).as_posix():sha(f.read_bytes()) for f in sorted(C.rglob('*')) if f.is_file() and f.name!='MANIFEST_SHA256.json'}
write('MANIFEST_SHA256.json',json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
archive=D/'Velluneo_Kompendium_Zasilacza_C16_C17_POWER20.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
    for f in sorted(C.rglob('*')):
        if f.is_file():
            info=zipfile.ZipInfo('Velluneo_Kompendium/'+f.relative_to(C).as_posix(),date_time=(2026,11,21,12,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(archive)as z:
    assert z.testzip()is None
    assert len(z.namelist())==len(manifest)+1
    assert all(sha(z.read('Velluneo_Kompendium/'+n))==h for n,h in manifest.items())
assert sha(board.read_bytes())==binding['source_board_sha256']
(D/'archive-check.json').write_text(json.dumps({'base_commit':BASE,'archive':archive.name,'archive_sha256':sha(archive.read_bytes()),'archive_bytes':archive.stat().st_size,'members':len(manifest)+1,'CRC_passed':True,'all_member_hashes_verified':True,'source_board_unchanged':True,'native_layer_exports':4,'power20_body_sha256':json.loads((P/'power-thermal-20/frozen-files.json').read_text())['body_sha256']},indent=2)+'\n',encoding='utf-8')
print('Built',archive,archive.stat().st_size,'bytes;',len(manifest)+1,'members')

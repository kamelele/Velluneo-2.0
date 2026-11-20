from pathlib import Path
import json,hashlib,shutil,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Flowable
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1]/'Velluneo-2.0'
S=R/'hardware/E27/variants/integrated-shade/SC09_compact';W=R/'hardware/E27/workflow/integrated-shade/compact-09'
O=R.parent.parent/'outputs/Velluneo_SC09_kompakt';O.mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bom=load(S/'bom-proposal.json');g=load(S/'intended-connectivity.json')
digest=hashlib.sha256(json.dumps({k:v for k,v in g.items() if k!='approval'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
styles=getSampleStyleSheet()
for s in styles.byName.values():s.fontName='Arial'
styles['Normal'].fontSize=9;styles['Normal'].leading=13
styles['Heading1'].fontName='ArialBold';styles['Heading1'].fontSize=21;styles['Heading1'].textColor=colors.HexColor('#123047')
styles['Heading2'].fontName='ArialBold';styles['Heading2'].fontSize=13
small=ParagraphStyle('small',parent=styles['Normal'],fontSize=7.5,leading=10)
story=[]
def p(t,style='Normal'):return Paragraph(t,styles[style])
def add(t,style='Normal'):story.extend([p(t,style),Spacer(1,8)])
def tab(rows,widths):
 t=Table([[Paragraph(html.escape(str(c)),small) for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfedf3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#397087')),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f8')])]))
 story.extend([t,Spacer(1,10)])
placements=[('C6 + wentylacja',(.5,.5,31.5,13.5),'#6cb7b0'),('L1',(32,.5,42.8,11.3),'#d9b36c'),('RF1',(32,11.8,44,17.8),'#e6b58d'),('T1',(.5,14,10.9,24.2),'#d9b36c'),('C4',(11.4,14,24.4,20),'#7aa9d0'),('RV1',(24.9,14,30.5,23),'#b2a0d1'),('C1',(32,18.3,39.3,22.8),'#7aa9d0'),('R7',(11.4,20.5,18.9,23),'#e6b58d')]
class Packing(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=495;self.height=305
 def draw(self):
  c=self.canv;s=9.5;ox=22;oy=30
  c.setFillColor(colors.HexColor('#e9f2eb'));c.setStrokeColor(colors.HexColor('#315d4a'));c.rect(ox,oy,45*s,25*s,fill=1)
  for ref,(x1,y1,x2,y2),co in placements:
   c.setFillColor(colors.HexColor(co));c.rect(ox+x1*s,oy+(25-y2)*s,(x2-x1)*s,(y2-y1)*s,fill=1)
   c.setFillColor(colors.HexColor('#153347'));c.setFont('ArialBold',8);c.drawCentredString(ox+(x1+x2)*s/2,oy+(25-(y1+y2)/2)*s,ref)
  c.setFillColor(colors.HexColor('#e4e7e9'));c.rect(ox+26.5*s,oy+11.5*s,5*s,13*s,fill=1)
  c.setFillColor(colors.HexColor('#17364b'));c.setFont('ArialBold',10);c.drawString(ox,oy+25*s+15,'45 mm × 25 mm — wyłącznie rzut korpusów')
  c.setFont('Arial',8);c.drawString(ox,oy-15,'Elementy SMD planowane na spodzie; brak jeszcze pól lutowniczych i ścieżek.')
add('Velluneo / SC09-A','Heading1');add('Kompaktowy zasilacz do modułu LED 4000 K / CRI ≥80','Heading2')
add('Propozycja techniczna do oceny • 21 listopada 2026 • etap przed schematem KiCad')
add('Wybrany kierunek: nieizolowany buck oparty na RDR-464, około 135 mA i 60 V. Zmniejszamy liczbę części i korzystamy z funkcji sterownika. Stary projekt SC08-B 140 × 100 mm nie spełnia celu gabarytowego i nie jest dalej rozwijany do produkcji.')
tab([['Parametr','Proponowany SC09-A'],['Zasilanie','230 V AC / 50 Hz; zakres obliczeń 207–253 V'],['Wyjście','135,2 mA nominalnie; 60 V / 8,11 W; roboczo 52–68 V'],['Diody','20 szeregowo × Lumileds L128-4080CA3500001'],['Cel światła','Około 800 lm po kloszu; wynik wymaga pomiaru na gorąco'],['Gabaryty','45 × 25 × około 19 mm: studium korpusów, jeszcze nie PCB'],['Granica dalszego projektu','Proponowany maksymalny gabaryt 50 × 25 × 20 mm; przekroczenie oznacza ponowny dobór rozwiązania'],['Straty','Planistycznie 0,7–1,2 W; nie zmierzone dla SC09'],['Liczba elementów','17 pozycji elektroniki + 2 pary pól przewodowych; LED na osobnej płytce']],[135,360])
add('Najważniejsze ograniczenia','Heading2');add('LYT1603D jest aktywny, lecz producent nie zaleca go do nowych projektów. T1 wymaga wykonania pojedynczego uzwojenia według RDR-464. To ryzyka dostępności i kosztu, które trzeba uwzględnić przed zamrożeniem BOM. Dostępność pojedynczych sztuk nie oznacza gotowego zamówienia całego zestawu.')
add('Wyjście pozostaje połączone elektrycznie z siecią. Wymiana modułu tylko po odłączeniu i potwierdzonym rozładowaniu. Ten układ nie realizuje bezpiecznego podłączania LED pod napięciem. Dostępność styków i izolacja gotowej żarówki wymagają osobnego potwierdzenia konstrukcyjnego.')
story.append(PageBreak())
add('Porównanie kompletnych kierunków','Heading1')
tab([['Rozwiązanie','Rzeczywiste dane odniesienia','Ocena'],['PI RDR-464 / LYT1603D','~50,1 × 22 mm z rysunku całej płytki; przy 230 V: 8,45 W wyjścia, 9,24 W wejścia, 91,51%, straty 0,79 W.','Najprostszy z porównanych: 16 części funkcjonalnych w bazowej wersji; MOV, rezystor bezpiecznikowy, filtr EMI, funkcje awaryjne IC. Wybrany do kompaktowego prototypu.'],['PI DER-404 / LYT4322E','57,8 × 27 mm; 72 V / 115 mA; ~84,95%; straty około 1,47 W przy 8,28 W.','42 części elektryczne; dodatkowe obwody ściemniania i niestandardowa magnetyka. Większy i bardziej złożony.'],['PI DER-406 / LYT4322E','40,9 × 26,8 mm; 48 V / 120 mA, 5,76 W; ~82,3% z wykresu; straty ~1,24 W.','31 pozycji z przyłączem, dławik z dodatkowym uzwojeniem. Nie jest bezpośrednim zamiennikiem 8 W.'],['ST STEVAL-LLL003V1 / VIPER0PLD','130 mA, około 7,5 W; ~88,3% przy pełnym obciążeniu z wykresu. Niepotwierdzone wymiary PCB.','28 obsadzonych pozycji EU; katalogowe dławiki. Wyniku 2 kV z dodatkowym odniesieniem do PE nie przenosimy na dwuprzewodową żarówkę.']],[112,210,173])
add('Porównanie obejmuje zabezpieczenia i filtrację pokazane w dokumentacji producentów. Różnią się obciążenia, warunki i metody odczytu sprawności. To nie są wyniki jednego wspólnego testu. RDR-464 nie zapewnia zgodności naszego zmienionego projektu z normami.')
add('Dlaczego nie sam mostek i rezystor?','Heading2');add('Przy około 8 W takie rozwiązanie nie zapewni wymaganej regulacji prądu i rozsądnych strat w całym zakresie sieci. Nieizolowany buck usuwa transformator izolacyjny, ale nadal potrzebuje dławika, filtracji, ograniczenia prądu oraz ochrony przed przepięciami i uszkodzeniami.')
add('Koszt i montaż','Heading2');add('Do pierwszych sztuk pozostaje zatwierdzony montaż ręczny. Economic PCBA ma sens po ustaleniu części SMD dostępnych w katalogu; duże elementy przewlekane i własny dławik wymagają osobnej operacji. Standard PCBA może obsłużyć szerszy zakres, ale wymaga potwierdzenia komponentów i wyceny. Brak kompletnej oferty: nie podajemy fikcyjnej ceny końcowej ani oszczędności procentowej.')
story.append(PageBreak());add('Gabaryty: co już wiemy','Heading1');story.append(Packing())
add('Kondensator Panasonic EEUFS2A151 ma nominalnie Ø12,5 × 20 mm, maksymalnie Ø13 × 22 mm. Położenie poziome daje szansę na cienki moduł. W studium zarezerwowano 26 × 13 mm na korpus i uformowanie wyprowadzeń oraz dodatkowe 5 mm wolnej przestrzeni przy końcu kondensatora.')
add('Wysokość robocza: kondensator i podparcie 13,5 mm + PCB 1,6 mm + elementy pod spodem 2,7 mm = 17,8 mm; przyjęto rezerwę do około 19 mm. To budżet, nie zmierzony model zmontowanej płytki. Wysokość gotowego T1, luty i przewody muszą zostać zweryfikowane.')
add('Układ 45 × 25 mm zawiera wyłącznie korpusy dużych elementów. Nie zawiera ich pełnych pól, kolizji nóżek, odstępów elektrycznych, ścieżek, przewodów ani mocowania. Odstępy 0,5 mm użyte przy pakowaniu korpusów nie są regułą izolacyjną. Nie jest to zatwierdzone rozmieszczenie PCB.')
add('Przed PCB','Heading2');add('Potrzebujemy zweryfikowanych wymiarów i pinów wykonanego dławika, sposobu ułożenia kondensatora oraz rzeczywistej wolnej przestrzeni w docelowej żarówce. Maksymalny proponowany budżet modułu to 50 × 25 × 20 mm. Jeśli pełne rozmieszczenie z odstępami go przekroczy, wracamy do doboru architektury. Nie powiększamy płytki po cichu.')
story.append(PageBreak());add('Wybrane części zasilacza','Heading1')
tab([['Ref.','Dokładna część / wartość','Funkcja'],*[ [c['ref'],c['mpn']+' / '+c['value'],c['kind']] for c in bom['components']]],[42,335,118])
add('BOM jest propozycją przed zatwierdzeniem schematu. Nie jest kompletnym koszykiem zakupowym. Złącza J1/J2 oznaczają pola do przewodów, bez wybranego mechanizmu wymiany modułu. T1 to dławik z jednym uzwojeniem, nie transformator izolujący.')
story.append(PageBreak());add('Połączenia i zabezpieczenia','Heading1')
add('Tor energii: J1 → rezystor bezpiecznikowy RF1 → mostek BR1 → filtr C1/L1/C4 → buck U1/D1/T1 → C6 i J2. MOV RV1 znajduje się za RF1 pomiędzy przewodami wejściowymi. C5 zasila lokalnie sterownik, R5 || R6 ustawia prąd, R4/R7 tworzą obwód wykrywania napięcia. R8A/R8B rozładowują C6.')
tab([['Obszar','Obliczenia / środki','Co nadal wymaga sprawdzenia'],['Prąd LED','(0,279 V / (0,68 Ω || 3,65 Ω)) / 3,6 ≈ 135,2 mA.','Zakres rzeczywistego prądu, tętnień i pracy przy 207/230/253 V oraz temperaturze.'],['Odłączone LED','R4 12,4 kΩ / R7 390 kΩ: nominalny próg statyczny ~77,9 V; ekran tolerancji ~69,37–86,51 V. C6 100 V.','Progi IC podane w 25°C; dynamiczne wyłączenie i maksymalne COUT ≤90 V nie są potwierdzone pomiarowo.'],['Rozładowanie','Dwa rezystory 68 kΩ. Przy jednym przerwanym: model 90→5 V około 36,45 s; Cmax180 µF, jawne rezerwy rezystancji.','Rzeczywisty czas i dostępne styki; nie stanowi bariery dotykowej.'],['Podłączenie LED','C6 do 0,729 J przy 180 µF / 90 V.','Brak hot-plug: rozładowany moduł podłącza się wyłącznie bez zasilania. IC nie ograniczy bezpośrednio impulsu z naładowanego C6.'],['Przepięcia / awaria','MOV 275 V AC, RF1 10 Ω / 2 W, wewnętrzne funkcje IC.','Współdziałanie MOV/RF1, zwarcie MOSFET, uszkodzenia pomiaru prądu, próby udarowe i termiczne. Nie są dwoma niezależnymi kanałami ochrony.']],[80,215,200])
add('Kompletna mapa: 19 pozycji, 47 fizycznych pinów, 11 sieci i jeden jawny NC: T1.4. Pięć pozostałych nieużywanych pinów karkasu usuwa się zgodnie z recepturą producenta. Pełne połączenia znajdują się w SC09_polaczenia.csv; wartości i MPN w SC09_czesci.csv.')
add('Zamknięcie cieplne i normy','Heading2');add('Plan pomiarów obejmuje U1, D1, RF1, T1, L1, C6, R7 oraz LED w ustalonym cieplnie module. R7 ma robocze ograniczenie lokalnego otoczenia do 100°C; C4 wymaga obniżania dopuszczalnego napięcia powyżej 85°C. Wyników otwartej płytki RDR w gorącym powietrzu nie traktujemy jako temperatur naszej zamkniętej żarówki. Badania EMC, bezpieczeństwa, odporności, PstLM/SVM i strumienia gotowej lampy pozostają obowiązujące.')
story.append(PageBreak());add('Źródła i dalsza decyzja','Heading1')
for title,url in [('PI RDR-464','https://www.power.com/sites/default/files/documents/rdr464.pdf'),('LYTSwitch-1 datasheet','https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf'),('PI AN-67','https://www.power.com/sites/default/files/documents/an67.pdf'),('PI LYT1603D — status produktu','https://www.power.com/products/lytswitch/lytswitch-1/lyt1603d'),('PI DER-404','https://www.power.com/sites/default/files/documents/der404.pdf'),('PI DER-406','https://www.power.com/sites/default/files/documents/der406.pdf'),('Lumileds DS216 — 12.11.2026','https://lumileds.com/DS216-LUXEON-2835-Architectural-Datasheet')]:
 add(f'<b>{title}</b><br/><link href="{url}" color="#236b8e">{url}</link>')
add('Dokładne źródła pozostałych części, odczytane wymiary i ograniczenia znajdują się w repozytorium w bom-proposal.json i reference/. Raporty badań producentów pozostają materiałem porównawczym. Nie deklarujemy własnych pomiarów ani gotowości produkcyjnej.')
add('Decyzja przed schematem','Heading2');add('Do dalszego schematu proponujemy SC09-A: 135 mA, 20 LED, C6 100 V w bazie, wyłącznie wymiana bez zasilania, przy świadomie otwartych pomiarach i ryzykach NRND / własnego dławika. Zgodnie z PCB Agent Toolkit nowa mapa wymaga decyzji właściciela przed wygenerowaniem schematu. Akceptacja starego SC08-B nie zatwierdza nowego układu.')
add('Mapa intent_digest:<br/>'+digest)
add('Kolejne etapy po zatwierdzeniu mapy: schemat KiCad i kontrola bibliotek → pełne rozmieszczenie z odstępami, widokami obu stron i 3D → trasowanie → osobna ocena plików produkcyjnych. W tym pakiecie nie ma jeszcze nowego schematu, PCB ani Gerberów.')
def footer(c,d):
 c.setFont('Arial',8);c.setFillColor(colors.HexColor('#5b6e7a'));c.drawString(40,25,'Velluneo • SC09-A • propozycja, bez zatwierdzenia produkcji');c.drawRightString(555,25,str(d.page))
SimpleDocTemplate(str(O/'SC09_propozycja.pdf'),pagesize=(595.28,841.89),leftMargin=45,rightMargin=45,topMargin=40,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1050" viewBox="0 0 1500 1050"><rect width="1500" height="1050" fill="#f2f6f8"/><g font-family="Arial" fill="#153347"><text x="75" y="90" font-size="43" font-weight="bold">SC09-A / studium gabarytów</text><text x="75" y="140" font-size="25">45 × 25 mm — rzut korpusów, przed projektem PCB</text>']
sx=28;ox=100;oy=205
svg.append(f'<rect x="{ox}" y="{oy}" width="{45*sx}" height="{25*sx}" rx="10" fill="#e4eee6" stroke="#34604c" stroke-width="3"/>')
for ref,(a,b,c,d),co in placements:
 svg.append(f'<rect x="{ox+a*sx}" y="{oy+b*sx}" width="{(c-a)*sx}" height="{(d-b)*sx}" fill="{co}" stroke="#31566a" stroke-width="2"/><text x="{ox+(a+c)*sx/2}" y="{oy+(b+d)*sx/2}" text-anchor="middle" font-size="24" font-weight="bold">{ref}</text>')
svg.append(f'<rect x="{ox+26.5*sx}" y="{oy+.5*sx}" width="{5*sx}" height="{13*sx}" fill="#d8dce0" opacity=".9"/>')
svg.append('<text x="75" y="970" font-size="23">Brak pól, ścieżek i zweryfikowanych odstępów. Wysokość robocza około 19 mm.</text><text x="75" y="1010" font-size="23">To nie jest gotowe rozmieszczenie ani potwierdzenie dopasowania do żarówki.</text></g></svg>')
(O/'SC09_gabaryty.svg').write_text(''.join(svg),encoding='utf-8')
for name in ['SC09_propozycja.pdf','SC09_gabaryty.svg','SC09_czesci.csv','SC09_polaczenia.csv']:shutil.copy2(O/name,W/name)
save(W/'packet-identity.json',{'kind':'pre-CAD proposal, not a complete CAD snapshot','intent_digest':digest,'actual_schematic_exists':False,'actual_board_exists':False,'approval':None,'date':'2026-11-21','artifacts':{n:sha(W/n) for n in ['SC09_propozycja.pdf','SC09_gabaryty.svg','SC09_czesci.csv','SC09_polaczenia.csv']}})
print(json.dumps({'pdf':str(O/'SC09_propozycja.pdf'),'intent_digest':digest}))

import csv, json
from pathlib import Path

out=Path('outputs')
def write(path,head,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(head)
        writer.writerows(rows)
def money(n):
    return f'{n:.5f}'.rstrip('0').rstrip('.') if n is not None else ''

ledurls={
 '2700':'https://www.digikey.com/en/products/detail/cree-led/JE2835BWT-N-H27EA0000-N0000001/21727032',
 '4000':'https://www.digikey.com/es/products/detail/cree-led/JE2835BWT-N-H40EA0000-N0000001/16182099',
 '6500':'https://www.digikey.com/en/products/detail/cree-led/JE2835BWT-N-H65EA0000-N0000001/16182111'}
ledstock={'2700':'Katalog aktywny, widoczne 18 638', '4000':'Katalog aktywny, widoczne 14 615', '6500':'Katalog aktywny, widoczne 55 949'}
ledalt={'2700':'L128-2780CA3500001','4000':'L128-4080CA3500001','6500':'L128-6580CA35000T1'}
head=['Zespół / wariant','Oznaczenie','Nazwa i funkcja','Parametry','Producent','MPN','Obudowa / footprint',
      'JLCPCB / LCSC','Dystrybutor alternatywny','USD/szt. 1 lub MOQ','Próg mały [części]','USD/szt. większy próg',
      'Próg duży [części]','Ilość na płytce / zespole','Koszt pozycji USD przy progu małym','Koszt pozycji USD przy progu dużym',
      'Dostępność i cykl życia','Zamiennik do weryfikacji','Uwagi montażowe','Źródło']
def row(group,ref,fn,val,maker,part,fp,code,dist,q,stock,alt,notes,src,pricing=None):
    lo,nlo,hi,nhi=pricing if pricing else (None,'',None,'')
    return [group,ref,fn,val,maker,part,fp,code,dist,money(lo),nlo,money(hi),nhi,q,
         money(lo*q) if lo is not None else '',money(hi*q) if hi is not None else '',stock,alt,notes,src]

designs=json.loads(Path('work/catalog.json').read_text(encoding='utf-8'))
by_mp={
 'US1M-13-F':('LCSC C99333','LCSC / DigiKey','Ofertę LCSC i stan zweryfikowano. Stan montażowy JLCPCB do potwierdzenia.','ES1M-13-F po IFSM i EMC','https://www.lcsc.com/product-image/C99333.html',(.062,10,.0324,10000)),
 'MMBT5551LT1G':('LCSC C41095','LCSC / Mouser','Ofertę LCSC i stan zweryfikowano. Stan montażowy JLCPCB do potwierdzenia.','MMBT5551-7-F po weryfikacji pinów i SOA','https://www.lcsc.com/product-detail/Bipolar-BJT_onsemi-MMBT5551LT1G_C41095.html',(.0258,20,.0108,9000)),
 'GRM21BR71H104KA01L':('JLCPCB i LCSC C77082','LCSC / DigiKey','Karta JLCPCB Extended, montaż SMT Economy/Standard. Zapas i ceny JLC po wycenie.','Samsung CL21B104KBCNNNC, LCSC C1711, potwierdzić DC bias','https://jlcpcb.com/partdetail/MurataElectronics-GRM21BR71H104KA01L/C77082',None),
 'AL5812MP-13':('Niepotwierdzony','DigiKey','Karta dystrybutora. Zapas w dniu zakupu do potwierdzenia.','AL5812FF-7, wymaga innego footprintu','https://www.digikey.com/en/products/detail/diodes-incorporated/AL5812MP-13/3678196',(.76,1,.34656,2500)),
 'LYT6073C-TL':('Niepotwierdzony','DigiKey / Farnell','Aktywny według DigiKey, obserwowano dostępność. Ceny USD do aktualnej wyceny.','LYT6063C-TL po przeprojektowaniu zacisku i kwalifikacji dostępności','https://www.digikey.ca/en/products/detail/power-integrations/LYT6073C-TL/8346132',None),
 'TPS26600PWPR':('Niepotwierdzony','TI / DigiKey / Mouser','Aktywny u producenta. W USA mały zapas w sprawdzonej ofercie, w UE wymagana aktualizacja dostępności.','TPS26600PWPT, ta sama obudowa i mniejsza taśma','https://www.digikey.com/en/products/detail/texas-instruments/TPS26600PWPR/6199305',(4.02,1,2.06184,2000)),
 'C3225X7T2J104KT000N':('LCSC C342668','LCSC / Mouser','Karta LCSC. Stan, cena i montaż JLCPCB do potwierdzenia.','1210 100 nF 630 V po sprawdzeniu charakterystyki DC','https://www.lcsc.com/product-detail/C342668.html',None),
 '36911000000':('Niepotwierdzony','DigiKey','Aktywny według DigiKey. 50 A zdolności wyłączania, do stanowiska o ograniczonej energii.','Wersja docelowa zależnie od spodziewanego prądu zwarciowego','https://www.digikey.com/en/products/detail/littelfuse-inc/36911000000/1986930',(.93,1,.36159,1400)),
 'EEU-FR1H471':('Niepotwierdzony','DigiKey','Aktywny w katalogu. Sprawdzić ceny i bieżący zapas.','EEU-FR1H331 tylko po sprawdzeniu tętnień i opóźnień','https://www.digikey.com/en/products/detail/panasonic-industry/EEU-FR1H471/2433595',None),
 'TMOV14RP275E':('Niepotwierdzony','Littelfuse / DigiKey','MPN producenta, cena i zapas do RFQ.','iTMOV14RP275M z adaptacją footprintu i badaniem','https://www.littelfuse.com/assetdocs/tmov-itmov?assetguid=bd475732-1071-4352-b8aa-f78b0007eb05',None),
 '440LD22-R':('Niepotwierdzony','Vishay / Mouser','MPN producenta, cena i zapas do RFQ.','Vishay VY1 2,2 nF Y1 z odpowiednim rozstawem i aprobatami','https://www.vishay.com/docs/23102/440lseries.pdf',None),
 'SRR1005-102K':('Niepotwierdzony','Bourns / Mouser','Katalog producenta, cena i zapas do RFQ.','Inny 1 mH o wyższym Isat i zweryfikowanej izolacji','https://bourns.com/docs/Product-Datasheets/SRR1005.pdf',None),
}
rows=[]
for d in designs:
    group='Zasilacz 75 × 40 mm'
    part=d['part']
    fp=d['footprint']
    source=by_mp.get(part)
    if not source:
        if part:
            alt='Element równoważny po sprawdzeniu wartości, obudowy, temperatury i parametrów impulsowych'
            source=('Niepotwierdzony','DigiKey / Mouser, wyszukiwanie po MPN','MPN kandydacki. Dostępność, cena i cykl życia niepotwierdzone.',alt,'',None)
        else:
            source=('', 'Wycena dostawcy / RFQ','Do wyboru po zatwierdzeniu wymagań i rysunku.','','',None)
    code,dist,stock,alt,src,pricing=source
    mount='SMT do potwierdzenia w JLCPCB po importowaniu BOM.'
    if 'THT' in fp or d['ref'] in ('J1','J2','J3','T1','CY1','F1','RV1'):
        mount='THT / wiązka. Uzgodnić oddzielny montaż.'
    rows.append(row(group,d['ref'],d['function'],d['val'],d['maker'],part,fp,code,dist,1,stock,alt,
                    (mount+' '+d['notes']).strip(),src,pricing))
ledrefs=' '.join('D'+str(i) for i in range(1,17))
for cct in ledurls:
    mp='JE2835BWT-N-H'+cct[:2]+'EA0000-N0000001'
    rows.append(row('Wkład '+cct+' K',ledrefs,'LED biała 3 V N Class',f'{cct} K / CRI ≥80 / 2,86 V typ. @150 mA / 11 K/W',
              'Cree LED',mp,'E27:Cree_JE2835B','Niepotwierdzony','DigiKey',16,ledstock[cct],ledalt[cct]+' po rekwalifikacji',
              'SMT, polaryzacja katoda na większym padzie 1. Kupić zakwalifikowany bin. Consignment po akceptacji JLCPCB.',ledurls[cct],(.10,1,.03959,4000)))
items=[
 ('Wkład','PCB1','Aluminiowa MCPCB','Ø30 mm ze ścięciem, 1,6 mm, F.Cu 35 µm','JLCPCB / dostawca IMS',1,'HASL do prób. Produkcyjne powierzchnie styku z powłoką odporną na zużycie.'),
 ('Wkład','J1 J2 J3','Pola kontaktowe','2,4 × 1,6 mm bez pasty','W ramach PCB1',3,'Wycenić wykończenie w ramach PCB, brak elementów do PnP.'),
 ('Wkład','M1','Obrzeże z uchwytami','Izolacyjne, odporne cieplnie','RFQ mechanika',1,'Zatrzask stały względem wkładu.'),
 ('Wkład','M2','Sucha przekładka TIM','0,20–0,30 mm, ≥3 W/mK','RFQ TIM',1,'Zamocowana fabrycznie, sprężysty powtarzalny docisk.'),
 ('Korpus','M3','Radiator','Al 48–54 mm, żebra ~30 mm','RFQ radiator',1,'Sprawdzić dostęp palcem i powtarzalny docisk.'),
 ('Korpus','M4','Głowica styków','3 × styk sprężynowy','RFQ styki',3,'Wymagany pomiar siły, rezystancji i trwałości.'),
 ('Korpus','M5','Klosz opalowy','Cel transmisji 0,87, A60','RFQ dyfuzor',1,'Wymagana fotometria kompletnego zespołu.'),
 ('Korpus','M6','Stała przegroda, bagnet, przesłona','Tworzywo izolacyjne termiczne','RFQ mechanika',1,'Wymagane badania dostępu, pozycjonowania i odporności na temperaturę.'),
 ('Korpus','S1','Mikroprzełącznik NO sygnału','Pozłacany, mały prąd','RFQ przełącznik',1,'Oddzielna krzywka.'),
 ('Korpus','S2','Mikroprzełącznik NO zasilania','≥30 V DC, zweryfikowany udar','RFQ przełącznik',1,'Oddzielna krzywka. Otwieranie pod obciążeniem w pojedynczej awarii.'),
 ('Korpus','TH1','Termostat NC','Początkowo 85–90 °C do prób','RFQ termostat',1,'Temperaturę doboru ustalić pomiarem.'),
 ('Korpus','J4','Cokół E27 i przewody','Kwalifikowany zespół, zaciskany','RFQ trzonek',1,'Mechanika IEC 60061, izolacja i odciążenie.'),
 ('Korpus','W1','Wiązka J2','Gniazdo XH 4p, terminale i przewody','JST / wykonawca wiązki',1,'S1 + TH1 i S2 według schematu.'),
 ('Korpus','W2','Wiązka J3','Gniazdo XH 3p, terminale i przewody','JST / wykonawca wiązki',1,'A+, KA, KB.'),
]
for g,ref,fn,val,dist,qty,notes in items:
    rows.append(row(g,ref,fn,val,'','','','',dist,qty,'Do uzgodnienia','','Montaż poza SMT. '+notes,''))
write(out/'BOM_E27_RevA.csv',head,rows)

def cost(g,fn,a,b,c,note): return [g,fn,*a,*b,*c,note]
costs=[
 cost('Zasilacz','PCB FR-4', (1.8,3.2),(.55,1.05),(.30,.60),'2 warstwy. Wycena po panelizacji.'),
 cost('Zasilacz','Transformator wzmocniony', (3.0,7.0),(1.4,2.8),(.75,1.55),'Custom, RFQ.'),
 cost('Zasilacz','Elementy strony pierwotnej i U1', (3.1,6.3),(2.2,4.0),(1.55,3.0),'Sterownik, diody, L1, bezpiecznik, MOV, pojemności HV.'),
 cost('Zasilacz','Strona wtórna z eFuse i 2 × CC', (3.6,6.6),(2.8,4.6),(2.25,3.8),'Elementy pasywne, ochrony i 2 kanały.'),
 cost('Zasilacz','SMT, THT i test elektryczny', (3.2,6.0),(1.1,2.3),(.62,1.4),'Zależy od montażu obu stron i kwalifikacji transformatora.'),
 cost('Wkład','16 LED Cree', (.66,.88),(.55,.73),(.51,.67),'Katalogowe progi, górna granica z założonym kosztem selekcji.'),
 cost('Wkład','MCPCB z przygotowanymi padami', (.9,2.4),(.45,1.0),(.24,.65),'Wykończenie do prób i wariant kontaktowy.'),
 cost('Wkład','Montaż SMT LED', (1.0,2.8),(.45,.92),(.26,.58),'Zależy od panelizacji, przygotowania taśmy i binów.'),
 cost('Wkład','TIM i uchwyt', (.7,2.1),(.33,.82),(.19,.52),'Bez formy i narzędzi.'),
 cost('Wkład','Kontrola i opakowanie wkładu', (.35,.85),(.22,.52),(.12,.32),'Próba optyczna i identyfikacja barwy.'),
 cost('Korpus','Radiator aluminiowy', (1.7,4.3),(.77,1.75),(.45,1.05),'Cena zależna od wytłoczenia/odlewu, bez narzędzi.'),
 cost('Korpus','Styki sprężynowe, wtyki, wiązki', (1.4,3.5),(.72,1.7),(.42,1.0),'Po kwalifikacji powłoki i wiązki.'),
 cost('Korpus','S1, S2, termostat', (2.0,4.0),(1.2,2.6),(.79,1.75),'Zakup zewnętrzny po testach mechanicznych.'),
 cost('Korpus','Dyfuzor, E27, przegroda, bagnet', (2.7,5.6),(1.22,2.85),(.75,1.6),'Bez kosztu form.'),
 cost('Korpus','Montaż końcowy, test, opakowanie', (1.6,3.8),(.83,2.0),(.52,1.1),'Osobna linia.'),
]
def subtotal(group,label):
    rr=[r for r in costs if r[0]==group]
    return ['Suma',label,*[round(sum(r[i] for r in rr),2) for i in range(2,8)],'Budżet netto USD / szt.']
subtotal_rows=[subtotal(g,fn) for g,fn in [('Zasilacz','Zasilacz z testem'),('Wkład','Pojedynczy wymienny wkład'),('Korpus','Korpus bez zasilacza i wkładu')]]
total=['Suma','Kompletna żarówka z jednym wkładem',*[round(sum(r[i] for r in subtotal_rows),2) for i in range(2,8)],
       'Bez VAT, transportu, form, badań zgodności i marży.']
write(out/'Koszt_produkcji_RevA.csv',['Zespół','Pozycja','100 szt. min USD/szt.','100 szt. max USD/szt.',
           '1000 szt. min USD/szt.','1000 szt. max USD/szt.','10000 szt. min USD/szt.','10000 szt. max USD/szt.','Podstawa estymacji'],
       costs+subtotal_rows+[total])
print(subtotal_rows[1])
print(total)

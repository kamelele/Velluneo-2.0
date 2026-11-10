# Wycena montażu · moc Rev H i sterowanie Rev G

W plikach mocy są **32** pozycje do importu SMT. Na sterowaniu jest **45**. BOM i CPL każdej płytki zawierają ten sam zestaw oznaczeń. C16 i R23 są zapisane jako DNP także w schemacie i na PCB, więc do ręcznych prób są dostępne pady bez nadruku pasty.

## Zmiany w dostępności

- D6 zachowuje DFLU1200-7 z identyfikatorem C154734. C2 zachowuje Rubycon 450BXW10MEFR10X16, C473172. C2 to THT, więc jego kod pomaga przy zaopatrzeniu i ręcznym montażu. [D6 w LCSC](https://www.lcsc.com/product-detail/C154734.html) · [C2 w LCSC](https://www.lcsc.com/product-detail/C473172.html)
- R8 pozostaje 47 Ω w 0805. Do BOM wpisano YAGEO RC0805FR-0747RL o tolerancji ±1% i mocy 0,125 W. R9 pozostaje 0,11 Ω ±1%. Panasonic ERJ-6DSFR11V ma moc 0,5 W przy 70°C oraz zakres TCR od 0 do +150 ppm/K. Po zmianie potwierdzić próg ograniczenia na płytce. [R8 YAGEO](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-0747RL) · [R8 LCSC](https://www.lcsc.com/product-detail/C114541.html) · [R9 Panasonic](https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/AOA0000C314.pdf) · [R9 LCSC](https://www.lcsc.com/product-detail/C4000855.html)
- C7 zastąpiono Murata GQM1875C2E680GB12D, 68 pF, 250 V, C0G ±2% w 0603. C9 to TDK C3216X7R1E225K160AE, 2,2 µF ±10%, 25 V, X7R w 1206. Na próbie sprawdzić efektywną pojemność i przebieg na BPS, bo wpływają na start przetwornicy. [C7 JLCPCB](https://jlcpcb.com/partdetail/2271248-GQM1875C2E680GB12D/C2179181) · [C9 TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X7R1E225K160AE) · [C9 LCSC](https://www.lcsc.com/product-detail/C508852.html)

## Przekazanie do wyceny

1. Złożyć osobne zapytania o montaż Standard mocy i sterowania. Uzyskać propozycję panelu z szynami i fiducjalami dla obu małych obrysów. Kody C ułatwiają import, a stany, ceny i dopuszczenie części potwierdza aktualna oferta montażu. [Wymiary i obsługiwany montaż JLCPCB](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)
2. W podglądzie montażu sprawdzić w szczególności T1 poza listą SMT, biegunowość mostka, D5–D9 i kondensatorów, pin 1 U1 oraz położenia części na spodzie. Uzgodnić montaż F1 i rezystora bezpiecznikowego R1 oraz siedmiu pozycji przewlekanych, w tym przyłączy przewodów.
3. Zamknąć decyzję o T1 po otrzymaniu danych konstrukcji, pomiarów Llk i rysunku. Złącza J101/J102 mają wspólne oznaczenie przewodów S_RAW/S_RTN. Pakiet jest przeznaczony do wyceny technologicznej i przygotowania prototypu po przeglądzie wykonawcy.

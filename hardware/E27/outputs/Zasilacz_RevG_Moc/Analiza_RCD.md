# Ogranicznik RCD · porównanie Rev F i Rev G

## Wniosek projektowy

Przy 5 µH rozproszenia transformatora model Rev F daje **239 V na C3** w punkcie nominalnym i do **271 V** w obwiedni. C3 i R4 mają po 200 V znamionowo. Już obwiednia dla 3 µH przekracza 200 V. To przyczyna zmiany części przed zleceniem zmontowanego zasilacza. [Wyniki liczbowe](Model_RCD.csv)

Rev G zachowuje ten sam obrys PCB i zwiększa zapas elementów.

- C3 to TDK C3216C0G2J222JT000N, 2,2 nF ±5%, C0G, 630 V, 1206. C0G zmniejsza wpływ napięcia polaryzacji na pojemność. [TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216C0G2J222J115AA) · [JLCPCB C342846](https://jlcpcb.com/partdetail/TDK-C3216C0G2J222JT000N/C342846)
- R4 i R22 to dwa YAGEO SR1206JR-7W82KL szeregowo, po 82 kΩ ±5%, 0,5 W przy 70°C i maks. 200 V napięcia pracy według rodziny SR. Podział napięcia i strat zależy od tolerancji. Spadek dopuszczalnej mocy wraz z temperaturą oraz ograniczenia montażowe dotyczą każdego rezystora osobno. [Karta YAGEO](https://www.tti.com/content/dam/tti-commons/supplier/yageo/doc/yageo-sr-anti-surge-chip-resistors-datasheet-and-specifications.pdf) · [JLCPCB C7319643](https://jlcpcb.com/partdetail/YAGEO-SR1206JR7W82KL/C7319643)
- D5 to Diodes Inc. US1M-13-F, SMA, VRRM 1000 V. Przy 10 µH model daje ok. 546 V napięcia zaporowego bez przepięcia indukowanego pasożytniczo. Odzyskiwanie zaporowe i prąd impulsowy wymagają pomiaru. [Karta Diodes Inc.](https://www.diodes.com/datasheet/download/US1M.pdf) · [JLCPCB C99333](https://jlcpcb.com/partdetail/DiodesIncorporated-US1M_13F/C99333)

## Założenia i metoda

Przyjęto niezależne zakresy Lm = 1,104–1,296 mH, napięcie odbite 95–101 V, moc magnesowania 7,5–9,2 W, częstotliwość 35–80 kHz oraz szczyt szyny 357,8 V przy 253 VAC. Kondensator Rev F jest oceniany dla 0,75–1,65 nF po uwzględnieniu założonego spadku efektywnej pojemności X7R. Kondensator Rev G sprawdzono dla 2,07–2,33 nF. Zakresy służą do oceny wrażliwości i wymagają potwierdzenia przebiegami. Każdy wynik obwiedni łączy ekstrema poszczególnych kolumn z różnych kombinacji.

W DCM moc związana z rozproszeniem przed uwzględnieniem napięcia odbitego jest równa Pmag × Llk/Lm. W modelu okresowym kondensator ładuje się w krótkim impulsie, a między impulsami rozładowuje przez rezystory. Model bilansuje energię rozproszenia z całką C × (Vcl − Vref) dV. Różnica między napięciem zacisku i napięciem odbitym wpływa na czas przewodzenia D5 i na energię odprowadzaną przez rezystory. Szczyt drenu oszacowano jako szczyt szyny plus szczyt zacisku i **20 V założonej rezerwy** na spadek D5 i dzwonienie. Rezerwa jest parametrem modelu. [TI o ograniczniku flyback](https://www.ti.com/document-viewer/lit/html/SSZTCV6) · [Power Integrations AN-75](https://www.power.com/sites/default/files/documents/an-75_lytswitch-6_design_guide.pdf)

- Przy **10 µH** obwiednia Rev G daje do **565,6 V** na drenie, **187,8 V** na C3 i **0,197 W** łącznie na rezystorach, z maks. **0,102 W** na pojedynczym rezystorze. Cel projektowy to do **580 V** na drenie, czyli 80% wartości 725 V z karty LYT6073C. Cel cieplny obliczeń to maks. 0,15 W na jeden rezystor. [Karta LYTSwitch-6](https://www.power.com/sites/default/files/documents/lytswitch-6_family_datasheet.pdf)
- Przy **12 µH** model daje do **576,6 V** i 0,220 W w rezystorach. Przy **15 µH** daje **591,7 V**. Do specyfikacji próbek wpisano **maks. 10 µH**, aby zachować dodatkowy margines wobec celu 580 V.
- Przy 5 µH nowa sieć rozprasza w obwiedni do **0,136 W**, wobec **0,069 W** w pierwotnej sieci pracującej powyżej napięcia znamionowego. Większą stratę trzeba uwzględnić w pomiarach cieplnych małej płytki. Pętlę impulsową pozostawiono na spodzie obok transformatora.
- Model obejmuje stan okresowy DCM ze stałą częstotliwością. Przy rozruchu, pracy nieciągłymi paczkami, zwarciu, regulacji w CCM i udarach trzeba ocenić rzeczywiste przebiegi, łącznie z odzyskiwaniem D5 i sprzężeniem pojemnościowym. Kryterium modelu Vmin > Vref dotyczy rozpatrywanego cyklu.

## Kryteria próby prototypu

1. Zmierzyć rozproszenie T1 ze zwartym uzwojeniem wtórnym i otwartym pomocniczym. Zapisać także wynik z pomocniczym zwartym osobno i metodę pomiaru. Do porównania używać wspólnego ustawienia miernika i kompensacji przewodów.
2. W laboratorium na zabezpieczonym stanowisku dla strony sieciowej rejestrować VDS i napięcie na C3 właściwymi sondami wysokonapięciowymi. Sprawdzić 207, 230 i 253 VAC przy starcie, ustalonym obciążeniu, biegu jałowym, dołączaniu i odłączaniu obciążenia, zwarciu, powrocie po zapadzie oraz w stanie nagrzanym. Dokumentować amplitudę, częstotliwość, temperaturę otoczenia i numer próbki.
3. Dla prób bez udaru przyjąć cel VDS ≤580 V i nie dopuszczać do przekroczenia limitów D5, C3 ani klucza. Porównać C3 z modelem, mierzyć temperaturę obu rezystorów i sąsiednich elementów do stanu ustalonego. Próby odporności na udary, izolacji i EMC rozliczyć oddzielnie według wymagań kompletnej lampy.

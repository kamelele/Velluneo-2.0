# Velluneo E27 · Rev F · płytka mocy

Płytka mocy przetwarza napięcie sieciowe na nominalne 26 V DC dla [sterowania Rev F](../Zasilacz_RevF_Sterowanie/README.md). J101 i J102 mają to samo przypisanie. Pin 1 to S_RAW, pin 2 to S_RTN. Prostowanie i filtracja wyjścia pozostają przy transformatorze na płytce mocy.

[Projekt KiCad](Zasilacz_RevF_Moc.kicad_pro) · [Schemat](Zasilacz_RevF_Moc.kicad_sch) · [PCB](Zasilacz_RevF_Moc.kicad_pcb) · [BOM](BOM_RevF.csv) · [Widok schematu](Podglady/Zasilacz_RevF_Moc.svg) · [Podgląd 3D](Podglady/RevF_3D.png)

- PCB ma **55,5 × 34 mm**, dwie warstwy i 40 pozycji. Strona sieciowa zachowuje rozmieszczenie, 452 segmenty i przelotki oraz pola miedzi P_0 z [Rev D](../Zasilacz_RevD_JLCPCB/README.md). Najwęższy pas między projekcjami miedzi stron w osi X ma **8,2 mm**. To wymiar z modelu PCB. Odstępy w kompletnym zespole zależą też od elementów, transformatora i montażu.
- Kontrola KiCad daje **0 naruszeń ERC i DRC oraz 0 brakujących połączeń**. Odczyt niezależnie porównał 99 przypisań pin–sieć. [Weryfikacja Rev F](Weryfikacja_RevF.md)
- [Pakiet do wyceny technologicznej JLCPCB](JLCPCB_DO_WYCENY) zawiera Gerbery, wiercenia oraz dopasowane BOM/CPL. Poza_importem.csv obejmuje pozycje do oddzielnej wyceny, w tym transformator. Obie płytki mają format poniżej 70 × 70 mm, więc przy wycenie usługi montażu Standard trzeba ustalić panel z szynami i znacznikami. Przed zleceniem montażu trzeba też sprawdzić orientacje, dostępność i sposób obsadzenia pozycji spoza importu. [Wymagania montażu JLCPCB](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)

## Warunek zwolnienia projektu

Analiza wykazała ryzyko przekroczenia napięcia znamionowego C3 i R4. Kolejnym wariantem do prób jest [Rev G z przebudowanym RCD](../Zasilacz_RevG_Moc/README.md). Pozytywny DRC obejmuje geometrię i zgodność połączeń, a prób napięciowych i cieplnych Rev F jeszcze nie wykonano.

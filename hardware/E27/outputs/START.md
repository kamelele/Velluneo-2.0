# E27 z wymiennym wkładem · Rev A

Otwórz plik `.kicad_pro` z wybranego katalogu w KiCad 10. Rozpakuj całość, aby zachować lokalne biblioteki symboli, footprintów i modeli.

- [Raport konstrukcyjny](Raport_E27_RevA.md) zawiera wybór architektury, obliczenia, warunki RFQ transformatora, analizę bezpieczeństwa i plan badań.
- [Wkład LED](Wklad_LED/Wklad_LED.kicad_pro) to MCPCB Ø30 mm z 16 LED, dwiema gałęziami i trzema stykami. Dla każdej barwy obowiązuje ten sam schemat i PCB. Wybierz odpowiedni wiersz LED w [BOM](BOM_E27_RevA.csv).
- [Zasilacz laboratoryjny](Zasilacz_RevA/Zasilacz_RevA.kicad_pro) to dwustronne PCB 75 × 40 mm. Zawiera flyback, dwa źródła prądowe i układ odcięcia.
- [Przekrój mechanizmu](Mechanizm_E27_RevA.svg) pokazuje układ docisku, izolacji, radiatora i blokad w docelowym korpusie.
- [Koszty](Koszt_produkcji_RevA.csv) obejmują zasilacz, wkład i całą lampę dla 100, 1 000 i 10 000 szt.
- [Weryfikacja](Weryfikacja_KiCad.md) i pliki `ERC.rpt` oraz `DRC.rpt` opisują wyniki kontroli CAD.

Katalogi `Produkcja_DO_PRZEGLADU` zawierają Gerbery, pliki wierceń i pozycje SMT. Wkład ma pusty plik Excellon, ponieważ projekt nie przewiduje wierceń. Pozycje SMD są podane w mm w formacie KiCad.

**Status zasilacza**  
Przed zamówieniem i uruchomieniem części sieciowej wymagane są kwalifikacja transformatora i części bezpieczeństwa, sprawdzenie pinoutów z rzeczywistymi próbkami oraz przegląd projektu sieciowego i stanowiska. Na etapie Rev A testy wkładu można rozpocząć z osobnymi, izolowanymi źródłami prądu w laboratorium.

# Weryfikacja plików KiCad 10.0.8

- Wkład LED. Zgodność niezależnie zapisanych połączeń pin po pinie ze schematem i PCB. Sprawdzono 35 styków elektrycznych, 16 pozycji SMT oraz brak otworów, przelotek i tras na B.Cu.
- Zasilacz. Porównano 156 połączeń pin–sieć pomiędzy założeniami, listą sieci wyeksportowaną przez KiCad i odczytem padów PCB.
- Minimalna szerokość pustego pasa między obwiedniami miedzi P/S w rzucie na oś x wynosi 8.200 mm w tym pliku, przy x końca obwiedni strony P = 102.900 mm i x początku strony S = 111.100 mm. Sprawdzono obie warstwy, pady, ścieżki i przelotki. To test geometrii pliku. Ocenie izolacji podlega gotowy zespół.
- ERC, DRC i porównanie schematu z PCB zakończyły się zerem naruszeń dla obu projektów. Wydzielone raporty zachowują listę reguł domyślnie wyłączonych przez KiCad.
- Gerbery, pliki wierceń oraz pliki pozycji są eksportem tych samych rewizji. Wkład nie ma punktów wiercenia. Dla zasilacza sprawdzić obie strony montażu w podglądzie dostawcy.
- Próby sprzętowe, pomiary izolacji, parametry fotometryczne i pomiary EMC pozostają do wykonania.

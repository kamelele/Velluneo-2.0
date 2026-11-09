# Weryfikacja KiCad 10.0.8 · Rev B

- Sprawdzono 66 × 34 mm na warstwie Edge.Cuts oraz wszystkie 152 przypisania pin–sieć na podstawie założeń, listy połączeń ze schematu i odczytu PCB. Osobno sprawdzono kolejność zabezpieczeń przed mostkiem, pinout BR1 oraz J2/J3.
- Zmierzony odstęp między skrajnymi obwiedniami miedzi sieci P i S w rzucie na oś x wynosi **8.200 mm**. Odczyt uwzględnia obie warstwy, pady, ścieżki i przelotki. Geometria PCB jest częścią oceny izolacji zmontowanego zespołu.
- ERC oraz DRC z porównaniem PCB do schematu zakończyły się bez naruszeń. Listy reguł pominiętych przez konfigurację są w raportach KiCad.
- Zgodność 57 pozycji elektrycznych BOM z PCB i 49 pozycji SMD w eksporcie montażowym sprawdzono osobno. Pliki Gerber, wierceń i montażowe są przeznaczone do przeglądu przez wykonawcę. Potwierdzenia wymagają kierunki, niestandardowe footprinty oraz montaż dwustronny.
- Pomiary na fizycznym prototypie i badania bezpieczeństwa są do wykonania według planu prób.

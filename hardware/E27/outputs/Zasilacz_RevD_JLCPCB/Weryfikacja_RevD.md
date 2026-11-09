# Weryfikacja projektu i plików Rev D

- ERC i DRC z porównaniem PCB ze schematem przeszły bez naruszeń. Zero niepołączonych padów i rozbieżności. Raporty KiCad zawierają wykaz pominiętych reguł.
- Skrypt porównał 248 przypisań pin–sieć w źródłach B1/B2, schemacie Rev D i PCB Rev D. Sprawdził też zachowanie położeń i obrotów elementów B1.
- Obrys z Gerbera i PCB ma 96 × 34 mm. Dwie warstwy, laminat 1,6 mm. Najwęższa ścieżka 0.210 mm. Najmniejszy otwór przelotki 0.300 mm, najmniejszy pierścień przelotki 0.140 mm i padu THT 0.375 mm. Są to wartości nominalne projektu.
- Cztery wypełnienia termiczne. Po uwzględnieniu padów, ścieżek, przelotek i wypełnionej miedzi prosty pas między sieciami pierwotnymi i wtórnymi ma 8.200 mm w rzucie na oś X. Izolacja kompletnego zasilacza pozostaje do weryfikacji.
- Wspólny początek Gerbera, wierceń i CPL znajduje się w lewym dolnym rogu płytki. Zweryfikowano współrzędne 144 przelotek z plikiem wierceń oraz wszystkich 79 pozycji SMD (góra 41, dół 38) z projektem. Współrzędne strony dolnej mają tę samą orientację X/Y. Obroty części należy zatwierdzić w podglądzie JLCPCB.
- Pełny BOM ma 87 pozycji montażowych. Pakiet do importu ma 70 pozycji (49 grup MPN), z tym samym zestawem oznaczeń w BOM i CPL. Pozostałe 17 pozycji wykazano oddzielnie. Sześć gołych pól TP101–TP106 służy do prób i nie wchodzi do BOM.

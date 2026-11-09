# Kontrola projektu KiCad · zasilacz E27 Rev B1

- ERC i DRC z porównaniem PCB ze schematem. Zero naruszeń, niepołączonych padów i rozbieżności. Zestaw reguł pominiętych przez konfigurację zapisano w raportach KiCad.
- Odczyt projektu potwierdził 152 przypisań pin–sieć zgodnych ze schematem. Położenia, rozmiary i sieci padów oraz wszystkie ścieżki i przelotki odziedziczone z Rev B porównano parami.
- Dodano 12 przelotek termicznych o padzie Ø0,60 mm i otworze Ø0,30 mm. Cztery są na P_0, a osiem na S_RTN. Każda przecina wypełnioną miedź swojej sieci na obu warstwach. Wypełnienie styka się z padami SOURCE 16–19 układu U1 oraz z padami 5 i 9 obu regulatorów U3/U4. Pola S_RTN pozostają poza obszarem rezystora pomiarowego R9.
- Rzeczywista powierzchnia poligonów po wypełnieniu P_0 wynosi **84.6 mm² na F.Cu** i **41.6 mm² na B.Cu**. Dla S_RTN wynosi **99.0 mm² na F.Cu** i **117.9 mm² na B.Cu**. Odczyt dotyczy miedzi w strefach, z odjętymi wycięciami, przed uwzględnieniem otworów wierconych. Powierzchnia geometryczna nie określa temperatury elementu.
- Najmniejszy pas pomiędzy skrajnymi obwiedniami miedzi P i S w rzucie na oś X ma **8.200 mm**, także po uwzględnieniu wypełnień i nowych przelotek. Ocena izolacji kompletnego zespołu wymaga pomiarów i przeglądu.
- Obrys PCB 66 × 34 mm, laminat 1,6 mm, 49 pozycji SMD w eksporcie KiCad. Dokumentacja montażowa ma status do przeglądu przed wykonaniem.

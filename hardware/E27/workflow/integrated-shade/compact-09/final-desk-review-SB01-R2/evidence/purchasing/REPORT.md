# Zakupy do prototypu zasilacza SB01 R2

Stan sprawdzenia: 24 listopada 2026. Wykonał `/root/r2_purchasing`; kandydat do przeglądu koordynatora, bez złożenia zamówień. Dotyczy wyłącznie zasilacza: 17 elementów elektronicznych, 16 różnych numerów producenta. Panel LED, PCB z JLCPCB i materiały montażowe są osobno. Nie zmieniono źródeł projektu ani doboru części.

## Co kupić

Otwórz `purchase-bom.csv`: podaje dokładne MPN, oznaczenia na płytce, liczbę montowanych sztuk, minimum zakupu, dostawcę, link, opakowanie, cenę i jakość dowodu dostępności. `purchase-plan.json` zawiera te same dane do dalszego przeliczenia. Ceny z TME odczytano dzisiaj bezpośrednio. Ceny i magazyn DigiKey pochodzą obecnie z indeksowanych stron oficjalnego dostawcy; datę indeksowania zapisano jawnie. Dostępność w indeksie nie jest dzisiejszą rezerwacją.

**TME:** RV1, BR1, C1, U1, R4, R6, D1, R8/R9. Wszystkie osiem dzisiejszych odpowiedzi HTTP 200 potwierdza dodatni stan magazynu. Minimum zakupu R6 to 100 sztuk, montowana jest jedna; pozostałe 99 stanowią zapas. U1 i R6 mają informację o sprzedaży do wyczerpania magazynu. U1 pozostaje LYT1603D w SO8; nie zmieniono sterownika.

**DigiKey:** RF1, rezystor w pozycji L1, C4, C5, R5, T1, C6, R7. Wszystkie dokładne MPN występują w oficjalnym katalogu z dodatnim stanem w zaindeksowanej obserwacji. R8/R9 potwierdzono dodatkowo w TME, minimum 1 sztuka; przeniesiono zakup do TME, zachowując dokładny MPN. Nie kupować pełnych szpul zamiast małych ilości. Nie wybierać Digi-Reel, który dolicza opłatę za przewinięcie.

**Ważne dla R2:** w pozycji oznaczonej nadal **L1** montuje się **PR02FS0201000KR500, 100 Ω ±10%, 2 W**. Nie kupować poprzedniego dławika 768772332. T1 pozostaje gotowym fabrycznym **Würth 7687709152**, 1,5 mH, 520 mA; nie wymaga zamawiania indywidualnego uzwojenia. RF1 pozostaje osobnym rezystorem bezpiecznikowym **FW20A47R0JA, 47 Ω**. Te dwa rezystory nie są zamienne.

TME podaje R4 jako ERJ6ENF1242V, z jawnym alternatywnym zapisem ERJ-6ENF1242V. To ten sam numer producenta z inną interpunkcją. Analogicznie zapis EEU-FS2A151 na stronie DigiKey odpowiada EEUFS2A151 w BOM. Porównanie stron producenta potwierdziło, że EEUFS2A151B różni się pakowaniem w taśmę ammo, zachowując wymiary korpusu 12,5 × 20 mm, raster 5 mm i parametry elektryczne. To dopuszczalna opcja pakowania po prawidłowym przycięciu i uformowaniu wyprowadzeń, ale jej nie wybrano: także nie ma jej obecnie w magazynie TME. Warianty L/LB mają inny korpus i parametry; nie są zamiennikami w tym pakiecie.

## Koszt i dostawy

Minimum części TME kosztuje **19,99 zł netto / około 24,59 zł brutto**; w tej kwocie jest całe 100 sztuk R6. Oficjalny [cennik TME](https://www.tme.eu/pl/how-to-buy/7428/Sposob-i-koszty-transportu/) podaje dla opłaconej przesyłki krajowej Pocztex **12,18 zł brutto**, a Standard **17,10 zł brutto**. TME z najtańszą z tych dostaw daje **około 36,77 zł brutto**. R6 w danych publicznej strony ma dokładniejszą cenę 0,095 zł netto, wyświetlaną po zaokrągleniu jako 0,10 zł. VAT i ceny brutto są tu obliczeniem budżetowym; rozliczenie i zaokrąglenia koszyka mogą nieznacznie się różnić. Warunki Pocztex: poniżej 25 kg i wartości 10 000 zł; bez pobrania.

Siedem wycenionych w PLN pozycji DigiKey daje **25,66 zł netto**, a C6 ma potwierdzoną tylko indeksowaną cenę **1,89 USD netto**. Dlatego nie przedstawiam pełnej kwoty w PLN jako aktualnej oferty. Oficjalna [polityka DigiKey](https://www.digikey.pl/pl/help-support/delivery-information/delivery-time-and-cost) podaje **80 zł** za wysyłkę zamówienia poniżej 300 zł; nie rozstrzyga na tej stronie jednoznacznie, czy podana opłata zawiera VAT. Ostrożny budżet wysyłki wynosi zatem **98,40 zł przy założeniu 23% VAT**, do potwierdzenia w końcowym podsumowaniu dostawcy. UPS/FedEx z opłaconym transportem opisano jako DDP; pozycje Marketplace i warianty CPT mogą mieć inne koszty.

Suma znanych pozycji w PLN z VAT i przesyłkami wynosi **148,33–166,73 zł plus polska cena brutto C6**. Dolna granica traktuje publikowane 80 zł jako koszt końcowy; górna dolicza do niego 23% VAT. To koszt minimalnych zakupów do jednej płytki, nie sama wartość elementów faktycznie wlutowanych. Kwota wymaga odświeżenia cen DigiKey oraz uzupełnienia ceny C6. Nie należy automatycznie zwiększać zamówienia do progu bezpłatnej wysyłki: dopłata za zbędne części może przewyższyć 80 zł.

Opcjonalny zapas do pierwszych prób: kupić łącznie po 3 sztuki RF1, L1, U1, BR1 i D1; kolumna `optional_spares_add` pokazuje po 2 dodatkowe sztuki. To osobny wydatek i osobna decyzja zakupowa; nie wliczono go do minimum. R6 ma już 99 sztuk zapasu wynikającego z minimum. Nie potrzeba dodatkowego T1 ani C6 do złożenia jednej płytki.

### Pełny budżet wraz z C6

Do planowania zakupów przyjmuję **około 180 zł brutto za wszystkie części do jednej płytki wraz z dwiema przesyłkami**. To szacunek, a nie bieżąca oferta dostawcy. Obejmuje zakup całych 100 sztuk R6 i dokładnie wybranego C6 z DigiKey. Nie obejmuje samej PCB, diod LED, materiałów montażowych ani robocizny.

Obliczenie zapisano w `cost-estimate.json`. Przy czysto budżetowym założeniu 1 USD = 4,50 zł, C6 za 1,89 USD daje około 10,46 zł brutto; komplet części daje około **66,61 zł brutto**, a komplet z dostawami około **158,79–177,19 zł brutto**. Rozpiętość dotyczy niejasnego VAT w publikowanej opłacie 80 zł za wysyłkę DigiKey. Założenie 4,00–5,00 zł/USD daje łącznie około **157,63–178,35 zł brutto**. Nie jest to deklaracja aktualnego kursu walut ani polskiej ceny C6, a przeliczenie nie zastępuje oferty w PLN. Ceny DigiKey z indeksu mogą się zmienić.

Dzisiejszy bezpośredni odczyt TME dla dokładnego **EEUFS2A151 potwierdził 0 sztuk, MOQ 200**; dla **EEUFS2A151B: 0 sztuk, MOQ 250**. Dlatego pozorna obecność części w katalogu TME nie została potraktowana jako możliwość zakupu jednej dostępnej sztuki. Pozostaje dokładny wariant bez sufiksu w koszyku planowanym w DigiKey, bez trzeciego dostawcy.

## Połączenia i materiały montażowe

J1/J2 są polami do lutowania izolowanych przewodów, a nie pozycjami złączy. Nie dodano do zakupów przypadkowych listew ani wtyczek. Przewody o izolacji odpowiedniej do przewidzianych napięć i temperatur, osłony izolacyjne, lut i topnik są materiałami montażowymi; ich długość oraz pakiety zakupowe zależą od stanowiska i posiadanych zapasów. Nie wliczono nieistniejącej wyceny tych materiałów. Zasilacz jest nieizolowany; wyjście LED nie jest obwodem bezpiecznego napięcia dostępnego dla dotyku.

Przy zamawianiu samej PCB w JLCPCB korzystać z pakietu produkcyjnego zatwierdzonego przez koordynatora; ta lista zakupów nie jest dodatkowym zatwierdzeniem elektrycznym ani produkcyjnym. Pozostaje laboratoryjna weryfikacja parametrów po zmontowaniu. Dostępność elementu nie dowodzi, że urządzenie zostało już pomierzone.

## Ślad dowodowy i ograniczenia

`acquisition.json`, `retry-tme.json` i `r4-retry.json` zapisują czas odpowiedzi, status, cenę i magazyn; odpowiadają im surowe HTML oraz tekst. `indexed-evidence.json` odróżnia wyniki wyszukiwania od bezpośredniej obserwacji. Zachowano też nieudane próby dostępu. Błędy 403/429 lub zerwane połączenie oznaczają brak odczytu, a nie zerowy stan magazynu. Po zwykłej przerwie ponowiono trzy odczyty TME kolejno; wszystkie osiem części TME ostatecznie potwierdzono.

Przed uznaniem całej listy za bieżącą ofertę pozostaje odczyt aktualnych stron DigiKey, potwierdzenie C6 w PLN oraz ostatecznego VAT i dostawy. Nie użyto starych cen z projektu jako dzisiejszych. Nie złożono zamówienia, nie dodano nic do koszyka ani nie wysłano zapytań dostawcom.

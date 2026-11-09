# Plan prób laboratoryjnych E27 Rev B

Wynik każdej próby zapisać razem z identyfikatorem płytki, partią elementów, temperaturą, ustawieniami i plikami przebiegów. Wartości liczbowe poniżej są celami rozwojowymi projektu.

Przed próbami z zamkniętą pętlą S1 skorygować poziom SHDN zgodnie z [instrukcją Rev B1](https://github.com/kamelele/Velluneo-2.0/blob/main/hardware/E27/outputs/Zasilacz_RevB1/README.md#4-próba-porównawcza-rev-b-i-b1). Zalecany przez TI zakres pinu wynosi 0–4 V.

## Część wtórna z izolowanego zasilacza laboratoryjnego

1. **Prądy kanałów.** Podać nominalne 26 V na S_RAW przy odłączonej stronie pierwotnej. Zmierzyć oddzielnie K1 i K2 przy dwóch obciążeniach, po otwarciu każdego kanału i z trzema wkładami. Sprawdzić około 127 mA na kanał, brak podwojenia prądu czynnego szeregu po przerwaniu drugiego oraz utrzymanie regulacji przy zimnym Vf. Powtórzyć po nagrzaniu. Udokumentować minimum napięcia S_RAW potrzebne do regulacji obu kanałów.
2. **Blokady i termostat.** Otwierać klosz szybko i wolno, rejestrując S_EN (SHDN), S_FUSED oraz napięcia między dostępnymi stykami i względem radiatora. W każdej osobnej próbie zasymulować sklejenie jednego przełącznika. Potwierdzić, że tor niezależny wyłącza napięcie zanim styki staną się dostępne. Sprawdzić zachowanie po otwarciu TH1, rozłączeniu i ponownym załączeniu wkładu.
3. **OVP.** Podać na S_RAW powolną rampę z około 26 V i zapisać wyłączenie oraz ponowne załączenie TPS26600. Powtórzyć dla krótkich skoków i różnych obciążeń, przy zimnej i gorącej płytce. Porównać statyczny próg z budżetem 27,43–29,10 V i rejestrować maksymalne napięcie dostępne na A+ względem K1/K2. Cel rozwojowy wynosi ≤30 V, także podczas odcięcia i ponowień. Oddzielnie sprawdzić zadziałanie zabezpieczenia pierwotnego po symulowanej utracie regulacji, na stanowisku z warunkami następnego etapu.

## Kompletny zasilacz po przeglądzie izolacji i stanowiska

4. **Warunki dopuszczenia do prób 230 V.** Zatwierdzić T1, sprawdzić elementy przekraczające barierę izolacyjną oraz odstępy całego zespołu. Potwierdzić footprinty i montaż F1/R1/C6, polaryzację mostka, bezpieczny przyrząd i zgodność układu z planem pomiarów. Zakres prób sieciowych i wymagania izolacyjne ustala prowadzący je projektant lub laboratorium.
5. **Rozruch i regulacja.** Przy 207, 230 i 253 VAC rejestrować prąd wejścia, napięcie C2, VDS i S_RAW podczas startu przy różnych fazach, w stanie zimnym i gorącym. Objąć próbami obciążenie zastępcze, odłączenie wkładu i zwarcie. Obliczyć I²t z przebiegu, sprawdzić powtarzalność udaru i czas rozładowania C2 po odłączeniu. Pomiary porównać z warunkami katalogowymi oraz analizą tolerancji i deratingiem.
6. **Koordynacja wejścia i EMC.** W laboratorium ustalić spodziewany prąd zwarciowy, zbadać uszkodzenia F1/R1/RV1 i zachowanie po udarze, przeciążeniu oraz przepięciu długotrwałym. Zarejestrować emisję i odporność, PF, pobór mocy i tętnienia prądu obu kanałów. Przed próbami niszczącymi zabezpieczyć stanowisko i ustalić kryteria uszkodzenia bezpiecznego.
7. **Termika i światło.** Po stabilizacji zmierzyć temperatury T1, U1, F1/R1, BR1, L1, C2/C6, obu regulatorów i punktów lutowniczych LED. Zbadać strumień po kloszu dla 2700, 4000 i 6500 K. Powtórzyć dla orientacji i warunków opisanych w Rev A. Próby wymiany wkładu w docelowym korpusie przeprowadzić po kwalifikacji przegrody, styków i odciążenia wiązek.

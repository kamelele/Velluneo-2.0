# E27 · zasilacz Rev B1

**Rewizja laboratoryjna PCB z polami odprowadzania ciepła.** Punkt odniesienia stanowi [zasilacz Rev B](../Zasilacz_RevB). Obrys 66 × 34 mm i nastawy elektryczne pozostają takie same, żeby porównać temperatury obu rewizji w identycznych warunkach. W tym etapie obciążeniem testowym jest stanowiskowy odpowiednik dwóch kanałów.

## 1. Identyfikacja dróg odprowadzania ciepła

U1, LYT6073C, oddaje ciepło głównie przez piny SOURCE. Są one w sieci P_0 po stronie sieciowej. Po stronie wtórnej główną drogą dla U3 i U4, AL5812, są pola odsłonięte pod obudowami. Oba pola są połączone z pinami GND we wspólnej sieci S_RTN. Powrót prostownika S_GND i powrót obciążenia S_RTN są rozdzielone rezystorem pomiarowym R9. [Power Integrations LYTSwitch-6, zalecenia PCB](https://www.power.com/sites/default/files/documents/lytswitch-6_family_datasheet.pdf?language=en) · [Diodes AL5812, opis wyprowadzeń](https://www.diodes.com/datasheet/download/AL5812.pdf)

## 2. Zmiana na PCB

- **P_0** otrzymała lokalne pole miedzi na każdej warstwie i cztery nowe przelotki przy U1. Dodatkowa reguła narzuca 1,5 mm między polem P_0 a sieciami wejścia AC. Nadal obowiązują reguły odstępów dla węzłów wysokiego napięcia oraz dla bariery P–S. W próbie sieciowej porównać zakłócenia i tętnienia z Rev B, ponieważ rozkład miedzi może zmienić rozkład prądu w powrocie.
- **S_RTN** otrzymała po jednym polu na stronę i po cztery nowe przelotki w sąsiedztwie U3 i U4. Pola obejmują odsłonięte pady oraz pady GND 5. Przelotki są poza padami lutowniczymi, z tentowaniem obu stron. Część pomiarowa przy R9 znajduje się poza nowymi polami.
- Przelotki mają średnicę pola 0,60 mm i otworu 0,30 mm. Przed zamówieniem uzgodnić metalizację, tentowanie i stos warstw z wykonawcą. Do porównania termiki Rev B i B1 użyć takiej samej grubości miedzi i tego samego stosu laminatu.

![F.Cu · pola termiczne i ścieżki](Podglady/Zasilacz_RevB1-F_Cu.svg)

[Dolna miedź](Podglady/Zasilacz_RevB1-B_Cu.svg) · [Render od góry](Podglady/Zasilacz_RevB1_gora_3D.png) · [Render od dołu](Podglady/Zasilacz_RevB1_dol_3D.png)

## 3. Weryfikacja i pliki

[Weryfikacja KiCad i zmierzone pola miedzi](Weryfikacja_KiCad_RevB1.md) · [Projekt KiCad](Zasilacz_RevB1.kicad_pro) · [Schemat](Zasilacz_RevB1.kicad_sch) · [PCB](Zasilacz_RevB1.kicad_pcb) · [Gerbery, wiercenia i pozycje](Produkcja_DO_PRZEGLADU) · [BOM zasilacza](../BOM_Zasilacz_RevB.csv)

## 4. Próba porównawcza Rev B i B1

1. Zacząć od części wtórnej z odłączonym wejściem sieciowym. Zasilić S_RAW względem S_RTN z izolowanego zasilacza laboratoryjnego z ograniczeniem prądu. Użyć dwóch obciążeń zastępczych dobranych do około 20, 22 i 24 V przy 127 mA. Dla pomiaru bazowego ustawić 26 V i ten sam stan blokad na obu płytkach.
2. Dla każdego kanału zapisać prąd oraz napięcie bezpośrednio pomiędzy pinem LED i GND regulatora. Przy 26 V oraz spadkach na obciążeniu 20, 22 i 24 V model daje odpowiednio **0,78 W, 0,52 W i 0,27 W na regulator**. Model mnoży napięcie na regulatorze przez 127 mA i dodaje 13 mW poboru własnego przy 0,5 mA. Faktyczne straty policzyć z pomiarów. Katalogowe 90°C/W dotyczy określonej płytki testowej producenta. Temperatury tego PCB trzeba zmierzyć. [Diodes AL5812, dane termiczne](https://www.diodes.com/datasheet/download/AL5812.pdf)
3. Osobno zbadać obciążenie jednego i dwóch kanałów. Przy 25°C i 40°C porównać temperaturę otoczenia, obudów U3/U4 oraz miedzi po obu stronach przy nowych przelotkach. Zapisywać temperaturę po stabilizacji, przyjętej tu jako zmiana poniżej 1°C przez 10 minut przy stałej temperaturze otoczenia. Za kryterium porównania przyjąć mniejszy przyrost temperatury gorętszego regulatora przy tej samej mocy strat oraz brak ograniczania prądu w normalnej pracy. Oszacowanie temperatury złącza wymaga właściwego modelu termicznego i znanej lokalizacji pomiaru.
4. Szczególnie sprawdzić zwarcie obciążenia jednego kanału. Przy początkowych 26 V i 127 mA model daje około **3,3 W** na jego regulatorze. Prąd może nadal pozostawać poniżej progu eFuse. Próba z ograniczoną energią ma ustalić reakcję zabezpieczenia i temperaturę, także przy powtarzaniu. Wewnętrzne wyłączenie termiczne AL5812 jest ostatnią ochroną układu. [Diodes AL5812](https://www.diodes.com/datasheet/download/AL5812.pdf) · [TI TPS26600](https://www.ti.com/lit/ds/symlink/tps2660.pdf)
5. Do prób sieciowych przejść po przeglądzie T1, izolacji, zabezpieczeń i stanowiska opisanym w [planie Rev B](../Plan_prob_RevB.md). W kontrolowanym stanowisku porównać Rev B/B1 przy 207, 230 i 253 VAC. Rejestrować temperatury U1, U3/U4, T1, D7, R1, C2 i C6 oraz prąd, tętnienia i pobór mocy. Power Integrations przy pełnym obciążeniu i najniższym napięciu wejściowym podaje 110°C jako granicę zalecaną przy doborze pola SOURCE. Sposób bezpiecznego pomiaru po stronie pierwotnej ustala prowadzący laboratorium. [Power Integrations LYTSwitch-6, termika](https://www.power.com/sites/default/files/documents/lytswitch-6_family_datasheet.pdf?language=en)

**Stan.** Model strat i kontrole plików wykonano. Brakuje pomiarów termicznych, badań EMC i kwalifikacji bezpieczeństwa. Spadku temperatury po zmianie miedzi jeszcze nie potwierdzono.

## Odtworzenie etapu

Z katalogu `hardware/E27` uruchomić `work/revb1_thermal.py outline` w Pythonie KiCad. Wypełnić pola przez `kicad-cli pcb drc --refill-zones --save-board --schematic-parity`, potem wykonać `work/revb1_thermal.py stitch` i ponowić wypełnienie. Na końcu uruchomić `work/export_b1.ps1`, który zapisuje raporty, widoki i pliki do przeglądu.

# Velluneo E27

Żarówka E27 230 V z wymiennym wkładem Ø30 mm. Trzy wersje barwy (2700 K, 4000 K i 6500 K) korzystają z tego samego interfejsu i mechanizmu.

- [Rewizja B zasilacza i wyniki weryfikacji](outputs/Raport_E27_RevB.md) · [projekt KiCad](outputs/Zasilacz_RevB) · [BOM](outputs/BOM_Zasilacz_RevB.csv)
- [Projekt wkładu LED](outputs/Wklad_LED) · [mechanizm wymiany](outputs/Mechanizm_E27_RevA.svg)
- [Pakiet KiCad Rev B](outputs/E27_RevB_pakiet_KiCad.zip) · [plan prób](outputs/Plan_prob_RevB.md)
- [Dokumentacja rewizji A](outputs/Raport_E27_RevA.md) · [pakiet Rev A](outputs/E27_RevA_pakiet_KiCad.zip)

Pliki obu rewizji są dokumentacją rozwojową. Pliki oznaczone `Produkcja_DO_PRZEGLADU` służą do przeglądu technologicznego. Przed próbami z siecią konieczny jest przegląd transformatora, ochrony, izolacji kompletnego zespołu oraz stanowiska.

Skrypty w katalogu [work](work) uruchamia się z katalogu `hardware/E27` z KiCad 10.0.8. Regeneracja zmienia pliki w `outputs`. Na Windows skrypty zakładają standardową ścieżkę instalacji KiCad.

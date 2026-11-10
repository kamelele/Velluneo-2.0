# Velluneo E27

Żarówka E27 230 V z wymiennym wkładem Ø30 mm. Trzy wersje barwy (2700 K, 4000 K i 6500 K) korzystają z tego samego interfejsu i mechanizmu.

- **Zasilacz dzielony Rev F** · [płytka mocy 55,5 × 34 mm](outputs/Zasilacz_RevF_Moc/README.md) · [sterowanie 30 × 25 mm](outputs/Zasilacz_RevF_Sterowanie/README.md) · pliki do wyceny technologicznej JLCPCB
- [Zasilacz Rev E · mniejsza płytka, wariant dzielony i podglądy 3D](outputs/Studium_RevE/README.md)
- [Zasilacz Rev D · jedna płytka do wyceny w JLCPCB](outputs/Zasilacz_RevD_JLCPCB/README.md)
- [Zasilacz Rev B1 · odprowadzanie ciepła przez PCB](outputs/Zasilacz_RevB1/README.md) · [weryfikacja KiCad](outputs/Zasilacz_RevB1/Weryfikacja_KiCad_RevB1.md)
- [Zasilacz Rev B2 · moduł prób ochrony zwarciowej](outputs/Zasilacz_RevB2_Ochrona/README.md) · [wyniki modelu](outputs/Zasilacz_RevB2_Ochrona/Model_RevB2_przypadki.csv)
- [Rewizja B zasilacza i wyniki weryfikacji](outputs/Raport_E27_RevB.md) · [projekt KiCad](outputs/Zasilacz_RevB) · [BOM](outputs/BOM_Zasilacz_RevB.csv)
- [Projekt wkładu LED](outputs/Wklad_LED) · [mechanizm wymiany](outputs/Mechanizm_E27_RevA.svg)
- [Pakiet KiCad Rev B](outputs/E27_RevB_pakiet_KiCad.zip) · [plan prób](outputs/Plan_prob_RevB.md)
- [Dokumentacja rewizji A](outputs/Raport_E27_RevA.md) · [pakiet Rev A](outputs/E27_RevA_pakiet_KiCad.zip)
- [Studium Rev C](outputs/Studium_RevC/README.md) · [model mechaniczny KiCad](outputs/Studium_RevC/E27_RevC_Gabaryty.kicad_pcb) · [specyfikacja próbek transformatora EFD20](outputs/Studium_RevC/RFQ_T1_EFD20.md)

Rewizje zasilacza są dokumentacją rozwojową. Pliki oznaczone `Produkcja_DO_PRZEGLADU` służą do przeglądu technologicznego. Przed próbami z siecią konieczny jest przegląd transformatora, ochrony, izolacji kompletnego zespołu oraz stanowiska.

Skrypty w katalogu [work](work) uruchamia się z katalogu `hardware/E27` z KiCad 10.0.8. Regeneracja zmienia pliki w `outputs`. Na Windows skrypty zakładają standardową ścieżkę instalacji KiCad.

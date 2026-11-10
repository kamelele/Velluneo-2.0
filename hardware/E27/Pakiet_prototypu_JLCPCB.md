# Pakiet prototypu JLCPCB · Velluneo E27

Aktualna para prototypowa to **moc Rev K i sterowanie Rev H**. Dla każdej płytki osobno użyć paczki Gerber ZIP oraz odpowiadających jej plików BOM i CPL z tego samego katalogu. [Podgląd obu płytek](outputs/Zasilacz_RevK_Moc/Podglady/Zasilacz_RevK_RevH_razem.png)

## Płytka mocy Rev K

- Obrys 55,5 × 34 mm, 2 warstwy, grubość projektu 1,60 mm. Najwęższa ścieżka ma 0,21 mm. Najmniejszy otwór przelotki ma 0,30 mm, a najmniejsze pole przelotki Ø0,58 mm.
- ZIP zawiera 2 warstwy miedzi, obrys, obie strony maski, pasty i opisów oraz metryczne wiercenia PTH. Zweryfikowano 32 pozycje wspólne BOM i CPL, w tym 11 na górze i 21 na dole.
- Na podglądzie montażu sprawdzić pin 1 BR1, oznaczenie polaryzacji D5–D9 i C2 oraz orientację U1. C16 i R23 pozostają nieobsadzone. [Gerber ZIP, BOM, CPL i części poza importem](outputs/Zasilacz_RevK_Moc/JLCPCB_DO_WYCENY)
- SHA-256 paczki Gerber: `859a5b12afcc732f5eac7c90a6f54d32d9ffb8487ca7e357425f000ee1852e38`.

## Płytka sterowania Rev H

- Obrys 30 × 25 mm, 4 warstwy, grubość projektu 1,60 mm. Najwęższa ścieżka ma 0,18 mm. Najmniejszy otwór przelotki ma 0,20 mm, a najmniejsze pole przelotki Ø0,45 mm.
- ZIP zawiera 4 warstwy miedzi i pozostałe warstwy produkcyjne oraz metryczne wiercenia PTH. Zweryfikowano 45 pozycji wspólnych BOM i CPL, w tym 29 na górze i 16 na dole.
- Na podglądzie montażu sprawdzić przede wszystkim orientację U2/U3/U4 i Q101/Q102. Złącza J102, J2 i J3 są przyłączami wiązek. [Gerber ZIP, BOM, CPL i części poza importem](outputs/Zasilacz_RevH_Sterowanie/JLCPCB_DO_WYCENY)
- SHA-256 paczki Gerber: `25e6a57bf88e17533835b37c32a8b9ae18020bca5160e2f77ea7c07130671a82`.

## Przed wysłaniem do produkcji

1. W podglądzie JLCPCB potwierdzić obrys, liczbę warstw i poprawne przypisanie wierceń. Dla obustronnego montażu wybrać Standard PCBA oraz uzgodnić z wykonawcą panel dla każdej płytki. JLCPCB podaje minimum 70 × 70 mm dla tej usługi i wymaga szyn oraz fiducjali. [Parametry PCB](https://jlcpcb.com/capabilities/pcb-capabilities/) · [Parametry PCBA](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)
2. Dla pełnego montażu ustalić dostawę T1 i wykonanie pozycji poza importem, w szczególności F1, R1, elementów przewlekanych i wiązek. Zatwierdzić podgląd obu stron oraz dokładne MPN przed zleceniem montażu. [RFQ transformatora](outputs/Zasilacz_RevG_Moc/RFQ_T1_EE16.md)
3. Kwalifikację elektryczną i cieplną wykonać na pierwszych egzemplarzach. [Zakres prób przed serią](outputs/Zasilacz_RevK_Moc/README.md#kwalifikacja-przed-serią)

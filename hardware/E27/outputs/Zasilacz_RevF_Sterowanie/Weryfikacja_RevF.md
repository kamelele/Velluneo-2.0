# Kontrola Rev F

- KiCad ERC wykazał zero naruszeń. Porównano niezależnie 148 przypisań pin–sieć w schemacie i PCB. Potwierdzono przypisanie wyprowadzeń Q101/Q102 oraz zgodność obwodów eFuse, blokad i obu regulatorów prądu z Rev D.
- Obrys 30 × 25 mm, cztery warstwy, 48 części i trzy pola pomiarowe. Interfejs J102 ma wyłącznie S_RAW i S_RTN. Warstwa In1.Cu ma jedno połączone wypełnienie S_RTN o powierzchni 573.7 mm² i lokalne odcinki REF o łącznej długości 9.3 mm. Cała sieć REF na czterech warstwach ma 25.4 mm ścieżek.
- Raport DRC z porównaniem schematu zawiera 0 naruszeń reguł i 0 niepołączonych padów. [Szczegóły](DRC.rpt)
- Model i kontrola plików stanowią weryfikację projektu. Próby fizyczne wymagają prototypu.

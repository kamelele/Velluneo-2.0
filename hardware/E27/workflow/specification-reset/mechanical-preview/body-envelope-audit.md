# MECH-PREVIEW-01 body-envelope audit

2026-11-17. Read device-repo/AGENTS.md and installed implementer instructions at manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822. Read-only native-source support by/root/support_design. No shared CAD edits, actual PCB geometry, placement-stage approval or fit/safety result.

## Body versus diagram reservation

| Part | Verified native body/terminal reference | What the concept may reserve/show |
|---|---|---|
| F1UMT-H3403.0268.23 | Manufacturer family form factor **5.3×16mm**; native drawing includes15.4 and5.35mm dimensions. This is not a fully tolerance-qualified land/courtyard envelope. | Use **16×5.35mm approximate body reference**, with a visibly separate larger unverified reservation. Do not call that rectangle the accepted footprint or give an unverified mountedheight. |
| RINAC05 | **Lmax18.0mm,diameterDmax7.5mm** in the native axialbodytable. | Body18×7.5mm ifhorizontal. Axialleadbends/holes/pads need MORElength; a26–28mmlong diagramreservation may be an engineeringplaceholder only, not a qualified footprint. Verticalstand-off and hotspot/thermalspacing remain undefined. |
| CBULKRubycon450BXW15MEFR10X20 | Nominal10×20mmcan. NativeD+0.5max⇒**diameter10.5mmmax**. L+αmax,α2⇒**bodylength22mmmax**. Nominal5mmpitch/.6mmwire. | CircleD10.5max for upright body. Label22mm as BODYlength, not an automatically complete mountedheight: leadforming/stand-off/ventspace and actuallandpattern add requirements. Sleeve is not an established safety barrier. |
| T1rawTDKB66422W1010D001 | Native coil-former plan **25±.2 by26−.3mm**, hence maximumrawplan **25.2×26.0mm**. Native **12.9mmmax** is the RAWcoil-former heightdimension; pinsproject belowtheflange. | Show rawbobbin25.2×26outline inside a separately marked transformerassemblyreservation. **Finishedcore pair,2yokes,winding/tape,leadouts/insulation and mounting envelope are not bounded by that rawbobbinbox.** No claim that a30×30placeholder bounds the wholetransformer. |
| COUTPanasonicEEHZA1J100P | StandardDcase:canD6.3±.5⇒**Dmax6.8mm**;baseA/B6.6±.2⇒**6.8×6.8mmmax**;nativeL5.8±.3⇒**Lmax6.1mm**. NativeH7.8max is overall PLANleadspan, NOTheight. | Physicalbody+terminalreference **7.8×6.8mmplan**,L6.1max. Actualsolderlands/courtyard may be larger; keep reservation distinct. This is **SMDV-chip**, never a radialfootprint. |

Dimensions are component references, not added clearance values. Do not infer creepage, cooling, soldering access, enclosurewall thickness, usablebulbvolume or opposite-side interference by simply arranging these rectangles.

## Sources actually inspected

- Vishay native28730Rev05Dec2024,PDFp10 axialdimensiontable:input-stage/source/resistor-ac.pdf SHA256`ebd3c714bb6b8c267c4cee006f5c72f105ee79c47d43ca680eb7e65929051f51`.
- RubyconBXW nativePDFp2dimensions andp4exact450V15uF10×20row:input-stage/source/bulk-bxw.pdf SHA256`9fb3a22e969e8244e135b7204aa46baa7b8a99d68803a6408fca20c3d8fd5fa6`.
- TDKEFD25 native10/22 PDFp3rawbobbin/yoke drawing, visuallyinspected:component-study/source/efd25.pdf SHA256`f4b6084fa9171a0157c3744663e146da6b3a738171dab4dfd3e137c125f6f06e`.
- Panasonic nativeexactZA-18 attechnicalPDFp19, visuallyinspected:component-study/source/panasonic-za-data.pdf SHA256`877d35869a3a68b69c8e70f4898c77fbbc0742337383e3bc0b9641d6522b4de2`; newerfamilycatalog concurs standardDdimensions.
- SCHURTER official UMT-H page/PDF:https://www.schurter.com/en/datasheet/UMT-H andhttps://www.schurter.com/en/datasheet/typ_UMT-H.pdf. Officialwebtext checked;localPDF/image download403, so no localhash or full tolerance/height qualification is claimed.

## Recommended honest visual

A partial **green-outline** diagram is suitable only with a prominent title **“Koncepcja gabarytów — nie jest to projekt PCB”**, and a short **“Brak ścieżek; rozmieszczenie i wymiary niezatwierdzone”** note. Use flat componentbody outlines and differently styled dashed reservationboxes. Label the transformerbox as unfinishedassemblyreservation and the remainingelectronics as reservedarea.

No coppertraces,pads,DRCbadges,soldermasktexture or render styling implying an actual routedboard. Any outerdimensions are proposeddiagramspace, not a releasedboardoutline. No numerical safety gap should be invented; a functional primary/secondary divider, if shown, must explicitly not represent a qualified physicalclearance. The concept demonstrates packagingpressure only; it does not establish E27fit, electricalsafety, finalfootprints or an actualPCB.

# Unchanged selected-basis main design

MainCAD is byte-identical to CONTROL05; the current RETURN06 route development is in ../studies/sense. Read ../README.md and its current study-result/verification/native reports. This main board still has zero tracks; the separate study has48segments/5vias/39unconnected. The preserved pre-CAD map and owner decision remain the selected basis, not technical-stage acceptance.

## Final transition refinement

The final study has48tracksegments/5actualvias and native0violations/39unconnected/0parity. VDD, DRV andNTC transitiontransactions includebothactualcopperlayers andvias; NTCground also routes at the retained0.3mmglobalminimum. Failed preliminarysingle-layerattempts remain in the recipe but are superseded by successfultransactions. Via placement is natively checked onbothfaces; one initiallytoo-closeDRVvia was rejected and moved beforethisresult. Transactionrollback usesstable nativeobjectidentity, not SWIGwrapper stringrepresentations. Allnon-powerGNDbranches excludeR9.2andthepowerstrap outsideC1contact. No completed operating/noise/fault/insulation claim follows: thelongICreturn, newcoupling, via/landassembly and currentloop stresses stillneedverification.

Finalconstructionrefinement: T1wellID2.90±.05mm, wall.50±.025mm andmetalzone≤2.70mm with≤.025mmcentreerror give.050mm conditionalradialfitclearance; outside≤4.00mm, planenvelopeX±12/Z9.25..13.25fits30mmallocation. These are proposedunconfirmedtolerances, notnormativeinsulation/material/heightqualification. The native trackexport now records8segment-to-oppositeHVpad projectedapproaches acrossallquietnets; they requirecoupling/solidinsulationassessment, not a DRCwaiver.

# Current RETURN06-r2 routing intent

The main33-component design is unchanged. The separate study now contains48tracksegments/fivevias, native0violations/39unconnected/0parity. Original failedsinglelayerattempts are preserved as history; successful VDD/DRV/NTC transitions and NTCground now establish actual continuity.

DedicatedF-SENSE is25.197855mm, with a separate B-side pulldown branch. CS1.931mm andR9-C1powerstrap2.7mm remain. ICtrunk37.445127mm plus1.25mmneck and allnonpowerGNDbranches must avoidR9.2/powerstrap exceptC1contactregion. Same-net topology and actualimpedance/noise require verification beyond DRC.

Fiveactualvias serve ground, VDD, DRV andNTC transitions. They are not all at C2. The ground andVDD transitions have C2land interaction; other transitions need their own RT1/R7/body/assembly inspection. No viafill/tent/solderwicking process is qualified. Allfive are electrically checked against bothcopperfaces by nativeDRC.

Eightsegment-to-oppositeHVpad projectedapproaches are reported acrossquietnets; they are unresolvedcoupling/solid-insulation interactions, not nativecommon-layer clearances waived by the author. Driver/powerloop completion and source-supported error/fault/thermal assessment remain open. R6 isRLCcompensation, not anexternalRCfilter. Preserve3/10mm andstrictglobalrules. No acceptedrouting ormanufacturing qualification is claimed.

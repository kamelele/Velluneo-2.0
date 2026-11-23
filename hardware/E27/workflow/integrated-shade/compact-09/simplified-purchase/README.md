# SC09-SB01 simplified procurement candidate

Original saved as "przed uproszczonym zakupem" at74c3ff1565e8b207d3f05fcc10beb0b67e1f659c, before CAD changes. Same concept/integrated-shade-nonisolated-buck branch; main unchanged. SC10 remains onhold.

Six electrical MPN changes: T1Wurth7687709152 catalogue1.5mH400V; C1KEMET47nF1000V; RV1TDK275VAC; R6Royalohm3.65ohm; RF1Bourns47ohm fusible; D1Diodes1000V. U1tube/reel packaging only. Five necessary placements changed. Same19references/46pins/11nets,2layers,51.2x33mm outline. No sensitive BP/M or Kelvin sense copper beneath T1.

Procurement:16unique MPN,17fitted electronic positions. Seven MPN fromTME,nine fromDigiKey. All had positive23Nov2026 stock observations, not reserved. Minimum purchase quantities72.71PLNgross; consumedparts60.54PLNgross; two-deliverybudget115.50PLN; total188.21PLNgross. Budget190PLN. PublishedDigiKey80PLNshipping conservativelybudgeted98.40including23%VAT; actualcheckoutVAT/currency/stockmaydiffer. Excludes barePCB/itsdelivery,manualassembly,LEDpanel,wires,enclosure andtestequipment. R6minimum100 includes99spares. Seeprocurement-final.json andcostHTML.

Native ERC/DRC/unconnected/schematicparity0; independent pinpartition unchanged. Full conservative strict-spacing remainsFAIL23, exactlysame intrinsicpackage/shortescape numericalsignatures asbaseline; no new longexternalroute findings. This is not an IECwaiver. Four independent scopedreviews are source-bound toreview-inputs.json. Toolkitworkcheck remainsFAIL forunresolved requirements/exactstage approvals/interface/spatialevidence. No approval wasfabricated or inherited.

RF147ohm linearcorner screen C1peak706.30V,C4peak588.70V,L1differential324.45V; not a nonlinearstartup/fuse/surge bound. T1thermal58–107C conditionalmodel doesNOTpass retained90Ctarget. Current/ripple/OVP/hotbias/surge/fault tests remain due. NonisolatedLEDoutput is hazardousrelative toearth; nohotplug. No physicaltest ororderperformed. This is an engineering/procurement candidate, NOT an order-readyrelease. Previous release-candidate Gerbers are historical and must not be used withSB01BOM.

Nativeviews in candidate-views. Replacement3Dmodels are illustrative maximumbodyenvelopes, not certifiedvendorSTEP. Exactsource andcheckhashes in review-inputs.json; final reviewreports are lifecycleoutputs outside thatmanifest.

# SC09-SB01 fresh bare-PCB fabrication candidate - NOT RELEASED

This package was freshly exported from a read-only copy of PCB SHA256 a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19 using KiCad10.0.6. The electrical source was not edited. Source functional intent is 19references/46pins/11nets. Native ERC/DRC/schematicparity/unconnected findings are zero after copy-only refill. The independent physical pinpartition matches intent and the PCB. All143 Gerbersegments,60 nativepadflashes across bothfaces and26drillhits match native geometry (Excellon1umcoordinatequantization allowed; maxdeviation0.1um).

## Proposed bare-PCB order settings
FR-4,2layers,51.2x33mm nominal outline,1.6mm thickness,1oz copper,lead-freeHASL,greenmask,whitelegendbothfaces,singleCNC-routedboard. Manualassembly; noJLCPCBA/stencil/CPLorder is implied. Minimumtrace0.3mm,viahole0.3mm,viapad0.75mm,viaannular0.225mm,minimumcomponentPTHannular0.5mm,minimumcopperedgegap1.05mm. FreshDRCuses0.3mmdifferent-netmanufacturingfloor and1.0mmedgefloor. These dimensions exceed the cited JLCPCB fabrication minimums; this is not a safetyclearance assessment.

## Candidate upload archive
SC09_SB01_Gerber_Drill_CANDIDATE_NOT_RELEASED.zip contains sevenGerbers (F/Bcopper,F/Bmask,F/Bsilk,EdgeCuts) and the PTHExcellon26holes. The emptyNPTHfile is retained underdrills for audit only; there are noNPTH/slots. Drillmaps/reports and previews are outside the uploadZIP. All layers use absolute consistentcoordinates; Bside plotted files must NOT be manually mirrored.

Optional nativeGerberjob is deliberately excluded from this uploadZIP. Its rawFinish=None and bbox51.25x33.05 include historical/defaultmetadata and the50umoutlineplotstroke; it is preserved as raw-native.gbrjob in the audit directory. The actualrouted centerlineoutline is51.2x33.0. Use explicitorderprofile and verify actualcheckoutsettings; never infer finishfromtherawjob. Copper/outline/drillgeometry is not changed to hide the metadata issue.

## Limits / stop status
This is NOT a released fabrication package. Full strict functionalspacing still has23knownintrinsicpackage/shortescape findings, not waivedbyfabDRC. Updatedexactsource acceptance, outstandingstage/interface/spatialevidence and allphysicaloperating/current/thermal/startup/surge/faulttests remain open. The previousSC09-ROUTE05 fabrication acceptance does NOT automaticallycover the changedSB01 source. Root finalintegration/reviews decide whether this exactcandidate can be presented forbarelaboratoryPCBacceptance. No order orpoweredtest hasbeenperformed.

The old release-candidate Gerbers elsewhere in the project are historical and must not be combined with SB01BOM. J1.1=AC_L,J1.2=AC_N; J2.1=LED_PLUS,J2.2=DC_RETURN. LEDoutputismainsreferenced,notSELV. The earlier lampconcept's illustrative panelwires are not a validatedharness: nativeJ2is atlowX,oppositethehighXinputJ1.

## Official capability reference
https://jlcpcb.com/capabilities/pcb-capabilities, read23Nov2026. 2L1oz track/space0.10/0.10mm; adopteddesignfloor0.3mm. Routedcopperedge0.2mmfabminimum; designfloor1mm. PTHannularabsolute0.18mm,recommended0.25mm; actualcomponentPTH0.5mm. Via0.30/0.75mm exceedsstandardpreferredviahole0.2mm anddiameterdifference0.15mm. Whitelegendheight1.0mm/stroke0.15mm matchespublishedminima.

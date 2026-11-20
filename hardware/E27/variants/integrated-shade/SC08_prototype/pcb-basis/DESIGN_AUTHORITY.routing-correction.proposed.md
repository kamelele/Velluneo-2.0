# Proposed SC08-B routing correction authority

NOT ACTIVE; owner decision pending. Existing hardware.json continues to select spatial-constraints.proposed.json and the original PCB08-ROUTE-1 basis.

If explicitly accepted, spatial-constraints-routing-correction.proposed.json selects routing-and-isolation-route2.proposed.json. The ONLY numerical scope change is U1 pin2(SENSE_FB)/pin4(DRAIN_BLOCKED), F.Cu pad/track exception: courtyard escape1.0 to1.5mm. Local1.9mm floor, generic4mm, DRAIN0.6mm hard minimum, all other21 package exceptions, no via/zone concession,47parts/112pins/30nets/1NC,140x100mm outline, all8 areas and fabrication profile remain unchanged.

This is a laboratory bare-board routing input decision. It does not approve complete routing, release, order, energized tests, standards compliance, temperatures or the finished lamp. Physical measurements and remaining64 connections remain open. SOURCE copper is re-clipped at the unchanged full4mm target plus0.10mm planning margin around added DRAIN copper; it receives no package concession.

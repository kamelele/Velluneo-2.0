# SB01 R3 — independent U1-short protection, WORKING DRAFT

**Not for ordering or powered testing. Routing is incomplete.** Canonical SB01 R2 and its existing files are preserved. The main branch is unchanged.

This directory publishes the current independent connectivity intent, exact BOM, electrical calculation report, specifications and laboratory assembly conditions. It is a design checkpoint, not a new fabrication packet. The local full CAD archive hash is recorded in STATUS.json for traceability; the archive is not included here. The saved partial CAD has35 unconnected items; later routing studies are still being integrated.

The added dual voltage/current comparator and SCR crowbar are independent of U1 control. Required external F1 is SIBA7000740.0,25,FF250mA400VAC5x20 in Eaton HHT holder before J1 LINE. Exact fuse stock is not confirmed. Conditional timing/thermal bounds require actual prototype qualification.

Outline51.2×33mm and existing converter retained. Planned assembly height22.0mm nominal/22.16mm at maximum PCB thickness, excluding external holder/cables. R2 Gerbers omit this protection and must not be represented as R3 files. No final four-role release review or powered measurement is asserted.

# ECO-01 — independently prepared physical-pin proposal

Status: **UNAPPROVED proposal, not applied to CAD or the canonical approved intent.** Date2026-11-17. Parent remote commit bb28f9c81f902f3e9de92dfab5ac17fce0e75fb4; accepted graph digest b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57.

## Exact requested design delta

1. Replace existing RB1 and RB2 with499kohm CRCW2512499KFKEG, two-terminal local passive contract1/2; keep their series connections BULK_POS→BLEED_MID→PRIMARY_GND. The package changes1206→2512; pad assignment must be updated after actual intent approval. Proposed numeric references R2/R3.
2. Add another independent identical series pair R14/R15: BULK_POS→R14.1, R14.2→BLEED_MID_B→R15.1, R15.2→PRIMARY_GND. No shared resistor/midpoint with the first branch. All four use the exact same499kohm2512 candidate. A PCB trace or common-point failure is outside the one-resistor-fault calculation and must be assessed during layout/safety review.
3. Add R13 CRCW06031M00FKEA1Mohm across VDD(R13.1) and PRIMARY_GND(R13.2). It discharges only the bias capacitor subcircuit and adds explicitly budgeted bias current; it does not establish a user-safe waiting time.
4. Rename existing references according to reference-aliases.json so all ordinary R/C/D references have numeric suffixes. No electrical value or pin membership changes through these aliases. Keep U1,Q1,T1,J1,J2,F1,BR1,TVS1,RT1 unchanged. This is the proposed remedy for SCH-ANN-001, not a report that the native annotation warning is already gone.

The revised proposal is31components,79physical terminals,22nets,4explicit transformer NC pins. It is constructed from the previously independently prepared requirements/datasheet graph and the above pin contract, **not exported from the KiCad schematic**. All seven original basis documents remain applicable for unchanged components. The new passive terminal convention is inherited from schematic-intent/local-terminal-contract.md;1/2 is a local nonpolar convention, not a polarity statement from Vishay.

## Native source and conditional acceptance

Vishay document20035D/CRCW e3,14Apr2026, https://www.vishay.com/docs/20035/dcrcwe3.pdf, SHA256773514dbb68319dd7a3b8d381a81798f8bb0a82cf65ecf440ec201dad810e7c5:1206 working200V,2512 working500V,0603 working75V;2512 P70=1W, linear derating toward155°C. At assumed125°C local ambient, the simple derated2512 allowance is.35294W, contingent on permitted film temperature and actual board heat flow. The source's separate insulation-test voltage is not a working-voltage rating or a primary/secondary barrier certification.

Existing single open removes the dedicated passive path; a single short leaves one1206 above200V at nominal high-line crest357.796V. Proposed branches retain a passive path after one resistor opens. Conditional worst passive-only357.796→5V time is78.3267s at18uF and +2.1% resistance; one short gives max.26205W at highline (.32752W at400V screen) in the remaining resistor, below the stated125°C screen. Actual values are in results.json. This does not test other faults, transient surge, aging, safety-standard discharge limits or accessible parts. The envelope assumes the additional125°C screen and ±2.1% initial/TCR allowance; long-term drift is not thereby qualified.

This correction doubles healthy bulk bleed from998kohm nominal to499kohm nominal, adding~.128W at the high-line crest. The averaged input sweep includes this increased load. Do not describe the improvement as free efficiency or thermal margin. Exact purchasable packing codes, JLCPCB availability and mounted thermal acceptance remain unconfirmed candidates; manufacturer family/order grammar is not stock evidence.

Bulk capacitance15uF, controller/sense/clamp values, winding turns and active devices are unchanged. A22uF bulk or sense-value retune is not part of this proposal. No approved specification acceptance threshold is changed.

## Decision boundary

Only Kamil Stępak can approve this exact intent for subsequent CAD capture; agent reviews do not approve it. Approval would authorize implementing these changes and rerunning native checks, not accept the schematic stage, PCB, fabrication or safety. Existing physical graph and editable schematic remain at the previous accepted revision until that decision.

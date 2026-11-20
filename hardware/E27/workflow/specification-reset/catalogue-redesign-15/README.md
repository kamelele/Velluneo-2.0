# CAT15 — orderable-component selection,20 November2026

**Selected transformer: MYRRA74215, factory-wound and sold complete. No custom winding.**
See [selected BOM](selected-bom.json), [JLCPCB dated stock](evidence/jlcpcb-stock.json),
[engineering change](engineering-change.md) and [transformer pin intent](interfaces/transformer-pin-intent.json).

Every one of33 baseline positions has a purchase route:31 electronic positions and
two wire-pad pairs with bought wire material. This is a component procurement
selection, not a completed harness or a qualified new assembled PCB. JLCPCB stock,
preorders and external stock are distinguished. No stock has been reserved.

R1/BR1/Q1 use factory SMD packages. R4/R6/R9 adapt the circuit to stock T1; U1
packing and TVS maker are explicit choices. The old transformer footprint does not
fit. Q1 package clearance, T1 abnormal current/leakage, startup/faults and insulation
remain concrete engineering holds, explained in engineering-change.md and checks.

**RFQ13/JLC14 archives are historical and must not be ordered for this new variant.**
Native product schematic/PCB, rules and old checks are unchanged. No proposed
part is represented as a validated drop-in; no new native/CAM pass is claimed.
No supplier was contacted, no upload/order/payment or physical test was performed.
Toolkit manifest remains b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.

Review scope: exact sourcing/ECO proposal only. The next implementation must resolve
the identified current/clearance holds, capture the new pin map, validate libraries,
redo affected placement/routing and produce freshly matched manufacturing files.
The owner and independent review gates remain distinct from catalogue availability.

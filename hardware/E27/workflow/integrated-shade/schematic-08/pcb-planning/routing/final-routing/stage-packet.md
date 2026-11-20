# SC08-B complete laboratory routing — human review

**Status: awaiting Kamil routing-stage decision.** The actual earlier "zatwierdzam" accepted only the concrete e229one-pair routing-input correction at701f616. This later fully routed result has not yet been accepted. No release/order/powered test is authorized.

Open the active SC08_prototype.kicad_pro. Native saved board bddb0838b0b27a542cdc509b4d621220da3febf53ecc31e799c87fca87a34dad; exact review manifest93dbb5532b8c981c5ae01aff364d88c095d259902e4ad86c6a5cf0b24b299832; Toolkit source snapshotcbe355b1c1a1cbfc71e25ef5ec321e3ced2043793a77ca2dda316c52a3966204.

140x100mm laboratory board,2L/1oz/1.6mm/leadfreeHASL/manual assembly,47unchanged parts/112pins/30nets/1NC.957segments,54vias,6filled copper zones and8unchanged managed areas. Preserved schematic/MPNs/pad mapping/physical placement/native project+rules. Main/quiet DCreturn star atC5negative verified by actual copper graph; compact C3bypass, separate PhotoMOS clamp paths, ten U3thermalvias. The one accepted local U1.2/U1.4 escape is1.5mm; remaining rules/21exceptions/zone-via restrictions retained.

Fresh integrated Toolkit work/routing PASS;10LAB routing criteria pass,2release criteria later. Native ERC0/DRC0violations0unconnected0parity after native refill/save, exactsavedcoppermatrixPASS382861facepairs. Two pre-existing ignored geometry checks remain disclosed unchanged. Qualified helper sources/tests/independent tool review and direct CAD checks are included. See integrated-toolkit-check.json and active routing-verification/ reports.

Four separate read-only review actors inspected one exact frozen candidate; actual reports, coverage and doc-only targeted closure at revised manifest are in reviews.json. No unresolved major routing finding remains. Two minor documentation issues were corrected, prior bytes/reports preserved, and each role independently confirmed closure/freshness. Optional short-segment cleanup is deferred without changing checked CAD.

Thermal geometry is not measured performance. U3F/BactualDCcopper346.66/399.978mm2,10thermalvias; thetaJA85K/W is conditional. Operative lab-board-boundaries requires vertical openboard, leftedgeuppermost,25mm clear air beyond OUTERcomponent/solder envelope on BOTHfaces. No enclosed fixture/lamp rating follows. Qualified guarded fixture/wires/probes/instruments and actual current,temperature,hotshutdown,PhotoMOSfault,startup/LEDconnectionimpulse/surge and optical/EMC checks remain later work. FaultCOUT145V/1.89225J bound and all17original product obligations remain controlling; none is claimed physically qualified.

Requested decision: accept this exact unpowered laboratory routing as basis for preparing production exports and their separate release review. This is not order/release/energized-test approval. The project's AGENTS.md requires the actual stage decision before advancing. Root will record the actual answer against this manifest and commit, preserving main.

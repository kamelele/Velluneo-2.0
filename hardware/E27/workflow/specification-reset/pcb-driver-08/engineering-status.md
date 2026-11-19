# Engineering scope and residual qualification

One4layer CAD selected under the owner's explicit delegated choice; routing complete. See exact native reports and selected process. This is not a claim of functional completion of a certified mains lamp.

## Current paths and sensing

TI SLUSB41A UCC2870x datasheet https://www.ti.com/lit/ds/symlink/ucc28700.pdf §11.1 p24 joins IC and power grounds at bulk capacitor return; §8.3.1.2 p10 requires local VDD bypass, §8.3.1.4–5 p11 describes DRV and RLC; GND is gate-driver return as well as analog reference. Keep bridge/aux/main shunt currents off the IC-return branch. TI SLUA783 https://www.ti.com/lit/an/slua783/slua783.pdf §2.6.1 p6 discusses CS spikes/RLC placement and CC effects; §2.7.2 p7–8 VS susceptibility. Primary documents checked19Nov2026. Their guidance supports the topology, not a measured error margin. No requirement for a fabricated negative-Kelvin topology is attributed to TI.

Wider bulk/drain and1.8mm shunt return reduce geometric conductor resistance but no current rating follows without operating RMS/pulse current, actual copper tolerance/temperature and thermal boundary. Inner copper is15.2µm, not35µm. Native plan lengths exclude via barrels, pads and component internal leads. No closed-loop area or inductance is inferred from one branch length. No ground pour was added that would short the intentional C1 star branches. Native cuts are conditional topology diagnostics, not impedance isolation. The CS/SENSE corridor is a conservative additional projection screen, not electric/magnetic field simulation or primary/secondary insulation proof.

## Remaining physical evidence on this selected board

Verify cold/hot start, VDD charge and auxiliary handover, line/load extremes, brownout/reset/retry, output-open/short/no-panel/partial-contact, sensor open/short, clamp drain peak/energy, shunt pulse/RLC error and actual gate Vgs/ringing at suitable isolated test facilities. Retain the C05/C06 electrical/transformer calculation assumptions; no new waveform closes them. Transformer core/gap/winding wire, termination forming, creepage through winding/finished joints, dielectric/hipot and thermal endurance require actual qualified construction evidence.3/10mm PCB rules and nominal FR4 do not establish full IEC/EN60598/61347 compliance. Tg155 does not establish CTI, RTI or a continuous service temperature.

Selected fab process includes filled/capped through-vias; confirm precise stackup/material, mask, copper tolerance, hole filling/capping and assembly with the vendor before order. Component PTH/NPTH holes stay open. Whole-lamp thermal design and Ø60×120 fit remain outside this driver-only CAD completion. No standard clauses/tables not accessible were invented. No physical qualification, supplier response, release or human approval is asserted.

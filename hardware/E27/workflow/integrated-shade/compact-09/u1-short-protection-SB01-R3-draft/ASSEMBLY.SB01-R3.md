# SB01 R3 laboratory assembly contract

Status: design candidate, incomplete routing. Manual assembly only. No order or powered test is authorized by this document.

The schematic has45 positions:44 onboard positions including the two bare-wire ports, and one external F1. There are42 onboard electrical components excluding ports. The separate HHT holder is an assembly purchase, not a schematic part. The authoritative MPNs and quantities are in `bom-build.csv`.

## External protective assembly

Fit SIBA7000740.0,25,250mAFF400VAC5×20 in Eaton HHT300VAC holder. Connect incoming LINE through F1 to J1.1, then the existing RF1. Connect incoming NEUTRAL to J1.2. Mechanically restrain and insulate the holder and leads; do not expose them through vents. Keep holder local ambient<=80°C. The holder does not inherit the fuse400VAC/10kA rating. A short before RF1 is not limited by its47ohm resistance. Exact supplier stock is unconfirmed; substitution requires a new coordination review.

## R24 and package fit

AC01000002008JA100 is fitted upright to the dedicated P4 lands. Incoming inspection must find a longer lead>=25.5mm. Use two90° bends with1mm centreline radius and2mm straight top; maintain>=0.5mm coating clearance and>=0.5mm solder tail. Fixture acceptance: front height<=17.5mm. This is a drawing/lead-length screen; an actual forming trial has not occurred. Planned complete height22.0mm nominal/22.16mm maximum PCB thickness, excluding holder and wires.

Q1 MCR12DSNT4G has a live trimmed central anode lead in addition to its tab. The generic TO252-2 model omits this metal. Placement/copper review must use the manufacturer package drawing, not an apparent empty gap in the model. Do not put C8 between cathode and gate solely on the generic render. D3 pin2 is deliberately NC. U3 pin3 is explicitly tied to anode/return as permitted by its data sheet.

## Assembly and test boundaries

Check every polarity, pin mapping and the F1 connection before bring-up. Confirm C6 orientation and free vent space, C7 effective>=70nF and C10 total node capacitance<=130pF. Keep R24 Kelvin sense and quiet return separate from power/fault current until their specified physical star pads. Verify actual R24 positive sense and negative quiet-return paths after final routing.

Normal operation requires the specified compatible20-series LED load,4000K/CRI>=80. Disconnect power and verify discharge before LED replacement. Output is not isolated from mains. No sealed-enclosure qualification exists. Stop conditions and conditional transient/current/thermal limits are enumerated in `prototype-gates.SB01.json`; they are a test plan, not measurements.
